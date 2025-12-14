from app.core.config import settings
import duckdb
import os
from typing import Generator
from contextlib import contextmanager
import threading

duckdb_conn = None
db_lock = threading.Lock()

#disgusting logic for handling duckdb conn
def get_duckdb():
    global duckdb_conn
    if duckdb_conn is None:
        with db_lock:
            if duckdb_conn is None:  # Double-check locking
                os.makedirs(os.path.dirname(settings.DUCKDB_PATH), exist_ok=True)
                # Connect in read-write mode
                duckdb_conn = duckdb.connect(settings.DUCKDB_PATH, read_only=False)
    return duckdb_conn


@contextmanager
def get_db() -> Generator[duckdb.DuckDBPyConnection, None, None]:
    # Use the shared connection with thread safety
    db = get_duckdb()
    try:
        yield db
    except Exception as e:
        raise e


def init_db(drop_existing: bool = False):
    """
    Initialize the database schema.
    
    Args:
        drop_existing: If True, drop all existing tables before creating new ones.
                      Default is False to preserve data on application restart.
    """
    db = get_duckdb()
    
    if drop_existing:
        db.execute("DROP TABLE IF EXISTS yokai")
        db.execute("DROP TABLE IF EXISTS attacks")
        db.execute("DROP TABLE IF EXISTS techniques")
        db.execute("DROP TABLE IF EXISTS soultimate")
        db.execute("DROP TABLE IF EXISTS inspirit")
        db.execute("DROP TABLE IF EXISTS skills")
        db.execute("DROP TABLE IF EXISTS attitudes")
        db.execute("DROP TABLE IF EXISTS equipment")
        db.execute("DROP TABLE IF EXISTS soul_gems")

    db.execute("""
        CREATE TABLE IF NOT EXISTS yokai (
            id VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            image VARCHAR,
            bs_a_hp INTEGER,
            bs_a_str INTEGER,
            bs_a_spr INTEGER,
            bs_a_def INTEGER,
            bs_a_spd INTEGER,
            bs_b_hp INTEGER,
            bs_b_str INTEGER,
            bs_b_spr INTEGER,
            bs_b_def INTEGER,
            bs_b_spd INTEGER,
            fire_res FLOAT DEFAULT 1.0,
            water_res FLOAT DEFAULT 1.0,
            electric_res FLOAT DEFAULT 1.0,
            earth_res FLOAT DEFAULT 1.0,
            wind_res FLOAT DEFAULT 1.0,
            ice_res FLOAT DEFAULT 1.0,
            equipment_slots INTEGER DEFAULT 1,
            attack_prob FLOAT DEFAULT 0.5,
            attack_id VARCHAR,
            technique_prob FLOAT DEFAULT 0.2,
            technique_id VARCHAR,
            inspirit_prob FLOAT DEFAULT 0.1,
            inspirit_id VARCHAR,
            guard_prob FLOAT DEFAULT 0.05,
            soultimate_id VARCHAR,
            skill_id INTEGER,
            rank VARCHAR,
            tribe VARCHAR,
            artwork_image VARCHAR,
            tier VARCHAR,
            extra VARCHAR
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id VARCHAR PRIMARY KEY,
            command VARCHAR NOT NULL,
            lv1_power INTEGER,
            lv10_power INTEGER,
            n_hits INTEGER DEFAULT 1,
            element VARCHAR,
            extra VARCHAR
        )
    """)
    
    # Techniques table
    db.execute("""
        CREATE TABLE IF NOT EXISTS techniques (
            id VARCHAR PRIMARY KEY,
            command VARCHAR NOT NULL,
            lv1_power INTEGER,
            lv10_power INTEGER,
            n_hits INTEGER DEFAULT 1,
            element VARCHAR,
            extra VARCHAR
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            description VARCHAR NOT NULL
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS inspirit (
            id VARCHAR PRIMARY KEY,
            command VARCHAR NOT NULL,
            effects JSON,
            image VARCHAR
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS soultimate (
            id VARCHAR PRIMARY KEY,
            command VARCHAR NOT NULL,
            lv1_power INTEGER,
            lv10_power INTEGER,
            lv1_soul_charge INTEGER,
            lv10_soul_charge INTEGER,
            n_hits INTEGER DEFAULT 1,
            element VARCHAR,
            extra VARCHAR
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS attitudes (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            boost_hp INTEGER DEFAULT 0,
            boost_str INTEGER DEFAULT 0,
            boost_spr INTEGER DEFAULT 0,
            boost_def INTEGER DEFAULT 0,
            boost_spd INTEGER DEFAULT 0
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            description VARCHAR,
            str_bonus VARCHAR,
            spr_bonus VARCHAR,
            def_bonus VARCHAR,
            spd_bonus VARCHAR,
            image VARCHAR
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS soul_gems (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            description VARCHAR,
            image VARCHAR
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username VARCHAR UNIQUE NOT NULL,
            email VARCHAR UNIQUE,
            hashed_password VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_battles INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            owner_id INTEGER NOT NULL,
            yokai_ids VARCHAR NOT NULL,
            tier VARCHAR DEFAULT 'OU',
            is_public INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users(id)
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS battles (
            id INTEGER PRIMARY KEY,
            player1_id INTEGER NOT NULL,
            player2_id INTEGER NOT NULL,
            team1_id INTEGER NOT NULL,
            team2_id INTEGER NOT NULL,
            winner_id INTEGER,
            battle_log VARCHAR,
            duration INTEGER,
            turns INTEGER DEFAULT 0,
            status VARCHAR DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            ended_at TIMESTAMP,
            FOREIGN KEY (player1_id) REFERENCES users(id),
            FOREIGN KEY (player2_id) REFERENCES users(id),
            FOREIGN KEY (team1_id) REFERENCES teams(id),
            FOREIGN KEY (team2_id) REFERENCES teams(id)
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS battle_logs (
            id INTEGER PRIMARY KEY,
            battle_id VARCHAR,
            player1_id VARCHAR,
            player2_id VARCHAR,
            winner_id VARCHAR,
            duration INTEGER,
            turns INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    db.execute("""
        CREATE TABLE IF NOT EXISTS player_stats (
            player_id VARCHAR PRIMARY KEY,
            total_battles INTEGER,
            wins INTEGER,
            losses INTEGER,
            total_damage_dealt INTEGER,
            total_damage_received INTEGER,
            favorite_yokai VARCHAR,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

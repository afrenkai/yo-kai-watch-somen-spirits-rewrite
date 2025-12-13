from app.core.config import settings
import duckdb
import os
from typing import Generator
from contextlib import contextmanager

duckdb_conn = None


def get_duckdb():
    global duckdb_conn
    if duckdb_conn is None:
        os.makedirs(os.path.dirname(settings.DUCKDB_PATH), exist_ok=True)
        duckdb_conn = duckdb.connect(settings.DUCKDB_PATH)
    return duckdb_conn


@contextmanager
def get_db() -> Generator[duckdb.DuckDBPyConnection, None, None]:
    db = get_duckdb()
    try:
        yield db
    except Exception as e:
        raise e


def init_db():
    db = get_duckdb()
    
    db.execute("DROP TABLE IF EXISTS yokai")
    db.execute("DROP TABLE IF EXISTS attacks")
    db.execute("DROP TABLE IF EXISTS techniques")
    db.execute("DROP TABLE IF EXISTS soultimate")
    db.execute("DROP TABLE IF EXISTS inspirit")
    db.execute("DROP TABLE IF EXISTS skills")
    
    db.execute("""
        CREATE TABLE yokai (
            id INTEGER,
            code VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            rank VARCHAR NOT NULL,
            tribe VARCHAR NOT NULL,
            attribute VARCHAR NOT NULL,
            hp INTEGER NOT NULL,
            str_stat INTEGER NOT NULL,
            spr_stat INTEGER NOT NULL,
            def_stat INTEGER NOT NULL,
            spd_stat INTEGER NOT NULL,
            attack_id INTEGER NOT NULL,
            technique_id INTEGER,
            inspirit_id INTEGER,
            soultimate_id INTEGER NOT NULL,
            skill_id INTEGER,
            tier VARCHAR,
            fire_res FLOAT DEFAULT 1.0,
            water_res FLOAT DEFAULT 1.0,
            lightning_res FLOAT DEFAULT 1.0,
            earth_res FLOAT DEFAULT 1.0,
            wind_res FLOAT DEFAULT 1.0,
            ice_res FLOAT DEFAULT 1.0,
            prob_attack FLOAT DEFAULT 0.5,
            prob_technique FLOAT DEFAULT 0.2,
            prob_inspirit FLOAT DEFAULT 0.15,
            prob_guard FLOAT DEFAULT 0.1,
            prob_loaf FLOAT DEFAULT 0.05
        )
    """)
    
    db.execute("""
        CREATE TABLE attacks (
            id INTEGER PRIMARY KEY,
            code VARCHAR UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            bp INTEGER NOT NULL,
            hits INTEGER NOT NULL,
            targets VARCHAR NOT NULL,
            attribute VARCHAR NOT NULL
        )
    """)
    
    db.execute("""
        CREATE TABLE techniques (
            id INTEGER PRIMARY KEY,
            code VARCHAR UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            bp INTEGER NOT NULL,
            hits INTEGER NOT NULL,
            targets VARCHAR NOT NULL,
            attribute VARCHAR NOT NULL,
            move_type VARCHAR NOT NULL
        )
    """)
    
    db.execute("""
        CREATE TABLE skills (
            id INTEGER PRIMARY KEY,
            code VARCHAR UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            description VARCHAR NOT NULL
        )
    """)
    
    db.execute("""
        CREATE TABLE inspirit (
            id INTEGER PRIMARY KEY,
            code VARCHAR UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            tags VARCHAR NOT NULL,
            effect_type VARCHAR NOT NULL
        )
    """)
    
    db.execute("""
        CREATE TABLE soultimate (
            id INTEGER PRIMARY KEY,
            code VARCHAR UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            bp INTEGER NOT NULL,
            hits INTEGER NOT NULL,
            targets VARCHAR NOT NULL,
            attribute VARCHAR NOT NULL,
            move_type VARCHAR NOT NULL,
            inspirit_effect VARCHAR
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

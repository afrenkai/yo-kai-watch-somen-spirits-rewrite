
import sys
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
import argparse

from app.core.database import get_duckdb, init_db


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('seed_database.log')
    ]
)
logger = logging.getLogger(__name__)


class SeedingError(Exception):
    pass


def load_json_data(file_path: Path) -> List[Dict[str, Any]]:
    """
    Load and parse JSON data from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as a list of dictionaries
        
    Raises:
        SeedingError: If file cannot be read or parsed
    """
    try:
        if not file_path.exists():
            raise SeedingError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise SeedingError(f"Not a file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            raise SeedingError(f"Expected list in {file_path}, got {type(data).__name__}")
            
        logger.debug(f"Loaded {len(data)} records from {file_path.name}")
        return data
        
    except json.JSONDecodeError as e:
        raise SeedingError(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise SeedingError(f"Error reading {file_path}: {e}")


def migrate_yokai(data_dir: Path) -> int:
    """
    Migrate Yokai data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating Yokai data...")
    
    try:
        data = load_json_data(data_dir / "yokai.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, yokai in enumerate(data, start=1):
            try:
                db.execute("""
                    INSERT INTO yokai (
                        id, name, image, 
                        bs_a_hp, bs_a_str, bs_a_spr, bs_a_def, bs_a_spd,
                        bs_b_hp, bs_b_str, bs_b_spr, bs_b_def, bs_b_spd,
                        fire_res, water_res, electric_res, earth_res, wind_res, ice_res,
                        equipment_slots, attack_prob, attack_id, technique_prob, technique_id,
                        inspirit_prob, inspirit_id, guard_prob, soultimate_id, skill_id,
                        rank, tribe, artwork_image, tier, extra
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    yokai.get('ID'),
                    yokai.get('name'),
                    yokai.get('image'),
                    yokai.get('BS_A_HP'),
                    yokai.get('BS_A_Str'),
                    yokai.get('BS_A_Spr'),
                    yokai.get('BS_A_Def'),
                    yokai.get('BS_A_Spd'),
                    yokai.get('BS_B_HP'),
                    yokai.get('BS_B_Str'),
                    yokai.get('BS_B_Spr'),
                    yokai.get('BS_B_Def'),
                    yokai.get('BS_B_Spd'),
                    yokai.get('Fire', 1.0),
                    yokai.get('Water', 1.0),
                    yokai.get('Electric', 1.0),
                    yokai.get('Earth', 1.0),
                    yokai.get('Wind', 1.0),
                    yokai.get('Ice', 1.0),
                    yokai.get('Equipment', 1),
                    yokai.get('AttackProb', 0.5),
                    yokai.get('attack'),
                    yokai.get('techniqueProb', 0.2),
                    yokai.get('technique'),
                    yokai.get('inspiritProb', 0.1),
                    yokai.get('inspirit'),
                    yokai.get('GuardProb', 0.05),
                    yokai.get('soultimate'),
                    yokai.get('skill'),
                    yokai.get('rank'),
                    yokai.get('tribe'),
                    yokai.get('artwork_image'),
                    yokai.get('tier'),
                    yokai.get('Extra', '')
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate yokai at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} Yokai")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate yokai: {e}")


def migrate_attacks(data_dir: Path) -> int:
    """
    Migrate attacks data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating attacks data...")
    
    try:
        data = load_json_data(data_dir / "attacks.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, attack in enumerate(data, start=1):
            try:
                db.execute("""
                    INSERT INTO attacks (
                        id, command, lv1_power, lv10_power, n_hits, element, extra
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, [
                    attack.get('ID'),
                    attack.get('Command'),
                    int(attack.get('Lv1_power', 0)) if attack.get('Lv1_power') else None,
                    int(attack.get('Lv10_power', 0)) if attack.get('Lv10_power') else None,
                    int(attack.get('N_Hits', 1)) if attack.get('N_Hits') else 1,
                    attack.get('Element'),
                    attack.get('Extra', '')
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate attack at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} attacks")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate attacks: {e}")


def migrate_techniques(data_dir: Path) -> int:
    """
    Migrate techniques data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating techniques data...")
    
    try:
        data = load_json_data(data_dir / "techniques.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, technique in enumerate(data, start=1):
            try:
                db.execute("""
                    INSERT INTO techniques (
                        id, command, lv1_power, lv10_power, n_hits, element, extra
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, [
                    technique.get('ID'),
                    technique.get('Command'),
                    int(technique.get('Lv1_power', 0)) if technique.get('Lv1_power') else None,
                    int(technique.get('Lv10_power', 0)) if technique.get('Lv10_power') else None,
                    int(technique.get('N_Hits', 1)) if technique.get('N_Hits') else 1,
                    technique.get('Element'),
                    technique.get('Extra', '')
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate technique at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} techniques")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate techniques: {e}")


def migrate_soultimate(data_dir: Path) -> int:
    """
    Migrate soultimate data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating soultimate data...")
    
    try:
        data = load_json_data(data_dir / "soultimates.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, soultimate in enumerate(data, start=1):
            try:
                db.execute("""
                    INSERT INTO soultimate (
                        id, command, lv1_power, lv10_power, lv1_soul_charge, lv10_soul_charge, n_hits, element, extra
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    soultimate.get('ID'),
                    soultimate.get('Command'),
                    int(soultimate.get('Lv1_power', 0)) if soultimate.get('Lv1_power') else None,
                    int(soultimate.get('Lv10_power', 0)) if soultimate.get('Lv10_power') else None,
                    int(soultimate.get('Lv1_soul_charge', 0)) if soultimate.get('Lv1_soul_charge') else None,
                    int(soultimate.get('Lv10_soul_charge', 0)) if soultimate.get('Lv10_soul_charge') else None,
                    int(soultimate.get('N_Hits', 1)) if soultimate.get('N_Hits') else 1,
                    soultimate.get('Element'),
                    soultimate.get('Extra', '')
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate soultimate at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} soultimates")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate soultimates: {e}")


def migrate_inspirit(data_dir: Path) -> int:
    """
    Migrate inspirit data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating inspirit data...")
    
    try:
        data = load_json_data(data_dir / "inspirits.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, inspirit in enumerate(data, start=1):
            try:
                # Convert effects array to JSON string
                effects_json = json.dumps(inspirit.get('Effect', []))
                
                db.execute("""
                    INSERT INTO inspirit (
                        id, command, effects, image
                    ) VALUES (?, ?, ?, ?)
                """, [
                    inspirit.get('ID'),
                    inspirit.get('Command'),
                    effects_json,
                    inspirit.get('image')
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate inspirit at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} inspirits")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate inspirits: {e}")


def migrate_skills(data_dir: Path) -> int:
    """
    Migrate skills data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating skills data...")
    
    try:
        data = load_json_data(data_dir / "skills.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, skill in enumerate(data, start=1):
            try:
                db.execute("""
                    INSERT INTO skills (
                        id, name, description
                    ) VALUES (?, ?, ?)
                """, [
                    skill.get('ID'),
                    skill.get('name'),
                    skill.get('description')
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate skill at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} skills")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate skills: {e}")


def migrate_attitudes(data_dir: Path) -> int:
    """
    Migrate attitudes data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating attitudes data...")
    
    try:
        data = load_json_data(data_dir / "attitudes.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, attitude in enumerate(data, start=1):
            try:
                boost = attitude.get('boost', [0, 0, 0, 0, 0])
                db.execute("""
                    INSERT INTO attitudes (
                        id, name, boost_hp, boost_str, boost_spr, boost_def, boost_spd
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, [
                    idx,
                    attitude.get('name'),
                    boost[0] if len(boost) > 0 else 0,
                    boost[1] if len(boost) > 1 else 0,
                    boost[2] if len(boost) > 2 else 0,
                    boost[3] if len(boost) > 3 else 0,
                    boost[4] if len(boost) > 4 else 0,
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate attitude at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} attitudes")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate attitudes: {e}")


def migrate_equipment(data_dir: Path) -> int:
    """
    Migrate equipment data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating equipment data...")
    
    try:
        data = load_json_data(data_dir / "equipment.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, equipment in enumerate(data, start=1):
            try:
                db.execute("""
                    INSERT INTO equipment (
                        id, name, description, str_bonus, spr_bonus, def_bonus, spd_bonus, image
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    idx,
                    equipment.get('name'),
                    equipment.get('description'),
                    equipment.get('STR', ''),
                    equipment.get('SPR', ''),
                    equipment.get('DEF', ''),
                    equipment.get('SPD', ''),
                    equipment.get('image')
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate equipment at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} equipment items")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate equipment: {e}")


def migrate_soul_gems(data_dir: Path) -> int:
    """
    Migrate soul gems data from JSON to database.
    
    Args:
        data_dir: Directory containing seed data files
        
    Returns:
        Number of records migrated
        
    Raises:
        SeedingError: If migration fails
    """
    logger.info("Migrating soul gems data...")
    
    try:
        data = load_json_data(data_dir / "soul_gems.json")
        db = get_duckdb()
        
        migrated = 0
        for idx, gem in enumerate(data, start=1):
            try:
                db.execute("""
                    INSERT INTO soul_gems (
                        id, name, description, image
                    ) VALUES (?, ?, ?, ?)
                """, [
                    idx,
                    gem.get('name'),
                    gem.get('description'),
                    gem.get('image')
                ])
                migrated += 1
            except Exception as e:
                logger.warning(f"Failed to migrate soul gem at index {idx}: {e}")
                continue
        
        logger.info(f"Migrated {migrated}/{len(data)} soul gems")
        return migrated
        
    except SeedingError:
        raise
    except Exception as e:
        raise SeedingError(f"Failed to migrate soul gems: {e}")


def validate_seed_directory(data_dir: Path) -> None:
    """
    Validate that the seed directory exists and contains required files.
    
    Args:
        data_dir: Directory to validate
        
    Raises:
        SeedingError: If validation fails
    """
    if not data_dir.exists():
        raise SeedingError(f"Seed directory does not exist: {data_dir}")
    
    if not data_dir.is_dir():
        raise SeedingError(f"Seed path is not a directory: {data_dir}")
    
    required_files = [
        "yokai.json",
        "attacks.json",
        "techniques.json",
        "soultimates.json",
        "inspirits.json",
        "skills.json",
        "attitudes.json",
        "equipment.json",
        "soul_gems.json"
    ]
    
    missing_files = []
    for filename in required_files:
        file_path = data_dir / filename
        if not file_path.exists():
            missing_files.append(filename)
    
    if missing_files:
        raise SeedingError(
            f"Missing required files in {data_dir}:\n  " + 
            "\n  ".join(missing_files)
        )
    
    logger.info(f"Seed directory validated: {data_dir}")


def print_summary(db, stats: Dict[str, int]) -> None:
    """
    Print summary of seeded data.
    
    Args:
        db: Database connection
        stats: Dictionary of table names to record counts
    """
    logger.info("DATABASE SEEDING SUMMARY")
    
    tables = ['yokai', 'attacks', 'techniques', 'soultimate', 'inspirit', 
              'skills', 'attitudes', 'equipment', 'soul_gems']
    
    for table in tables:
        try:
            actual_count = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            migrated_count = stats.get(table, 0)
            status = "good" if actual_count > 0 else "bad"
            logger.info(f"  {status} {table:20s}: {migrated_count:4d} migrated, {actual_count:4d} in DB")
        except Exception as e:
            logger.error(f" {table:20s}: Error querying - {e}")



def main(data_dir: Path) -> int:
    """
    Main seeding function.
    
    Args:
        data_dir: Directory containing JSON seed files
        
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        logger.info("Starting database seeding process...")
        logger.info(f"Seed directory: {data_dir.absolute()}")
        validate_seed_directory(data_dir)
        
        logger.info("Initializing database schema...")
        init_db(drop_existing=True)
        logger.info("Database schema initialized successfully")
        stats = {}
        
      
        stats['skills'] = migrate_skills(data_dir)
        stats['attacks'] = migrate_attacks(data_dir)
        stats['techniques'] = migrate_techniques(data_dir)
        stats['soultimate'] = migrate_soultimate(data_dir)
        stats['inspirit'] = migrate_inspirit(data_dir)
        stats['yokai'] = migrate_yokai(data_dir)
        stats['attitudes'] = migrate_attitudes(data_dir)
        stats['equipment'] = migrate_equipment(data_dir)
        stats['soul_gems'] = migrate_soul_gems(data_dir)

        db = get_duckdb()
        print_summary(db, stats)
        
        logger.info("Database seeding completed successfully!")
        return 0
        
    except SeedingError as e:
        logger.error(f"  Seeding error: {e}")
        return 1
    except Exception as e:
        logger.exception(f"  Unexpected error during seeding: {e}")
        return 1


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Seed the Yo-kai Watch Somen Spirits database from JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Seed from default directory
  uv run seed_database.py
  
  # Seed from custom directory
  uv run seed_database.py --seed-dir /path/to/custom/data
  
  # Verbose logging
  uv run seed_database.py --seed-dir ./seed_data --verbose
        """
    )
    
    parser.add_argument(
        '--seed-dir',
        type=str,
        default='./seed_data',
        help='Directory containing JSON seed files (default: ./seed_data)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    data_dir = Path(args.seed_dir).resolve()    
    exit_code = main(data_dir)
    sys.exit(exit_code)

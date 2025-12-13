from app.core.database import get_duckdb, init_db
from app.data.yokai_data import YOKAI_DATA
from app.data.attacks_data import ATTACKS_DATA
from app.data.techniques_data import TECHNIQUES_DATA
from app.data.soultimate_data import SOULTIMATE_DATA
from app.data.inspirit_data import INSPIRIT_DATA
from app.data.skills_data import SKILLS_DATA


def seed_attacks():
    db = get_duckdb()
    
    print(f"Seeding {len(ATTACKS_DATA)} attacks...")
    db.execute("DELETE FROM attacks")
    for attack in ATTACKS_DATA:
        db.execute("""
            INSERT INTO attacks (id, code, name, bp, hits, targets, attribute)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            attack["id"], attack["code"], attack["name"],
            attack["bp"], attack["hits"], attack["targets"], attack["attribute"]
        ))
    
    print(f"Seeded {len(ATTACKS_DATA)} attacks")


def seed_techniques():
    db = get_duckdb()
    
    print(f"Seeding {len(TECHNIQUES_DATA)} techniques...")
    db.execute("DELETE FROM techniques")
    for tech in TECHNIQUES_DATA:
        db.execute("""
            INSERT INTO techniques (id, code, name, bp, hits, targets, attribute, move_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tech["id"], tech["code"], tech["name"],
            tech["bp"], tech["hits"], tech["targets"],
            tech["attribute"], tech["move_type"]
        ))
    
    print(f"Seeded {len(TECHNIQUES_DATA)} techniques")


def seed_inspirits():
    db = get_duckdb()
    
    print(f"Seeding {len(INSPIRIT_DATA)} inspirits...")
    db.execute("DELETE FROM inspirit")
    for insp in INSPIRIT_DATA:
        db.execute("""
            INSERT INTO inspirit (id, code, name, tags, effect_type)
            VALUES (?, ?, ?, ?, ?)
        """, (
            insp["id"], insp["code"], insp["name"],
            insp["tags"], insp["effect_type"]
        ))
    
    print(f"Seeded {len(INSPIRIT_DATA)} inspirits")


def seed_soultimates():
    db = get_duckdb()
    
    print(f"Seeding {len(SOULTIMATE_DATA)} soultimates...")
    db.execute("DELETE FROM soultimate")
    for soul in SOULTIMATE_DATA:
        db.execute("""
            INSERT INTO soultimate (id, code, name, bp, hits, targets, attribute, move_type, inspirit_effect)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            soul["id"], soul["code"], soul["name"],
            soul["bp"], soul["hits"], soul["targets"],
            soul["attribute"], soul["move_type"], soul.get("inspirit_effect")
        ))
    
    print(f"Seeded {len(SOULTIMATE_DATA)} soultimates")


def seed_skills():
    db = get_duckdb()
    
    print(f"Seeding {len(SKILLS_DATA)} skills...")
    db.execute("DELETE FROM skills")
    for skill in SKILLS_DATA:
        db.execute("""
            INSERT INTO skills (id, code, name, description)
            VALUES (?, ?, ?, ?)
        """, (
            skill["id"], skill["code"], skill["name"], skill["description"]
        ))
    
    print(f"Seeded {len(SKILLS_DATA)} skills")


def seed_yokai():
    db = get_duckdb()
    
    print(f"Seeding {len(YOKAI_DATA)} yokai...")
    db.execute("DELETE FROM yokai")
    for y in YOKAI_DATA:
        db.execute("""
            INSERT INTO yokai (
                code, name, rank, tribe, attribute,
                hp, str_stat, spr_stat, def_stat, spd_stat,
                attack_id, technique_id, soultimate_id, inspirit_id, skill_id, tier,
                fire_res, water_res, lightning_res, earth_res, wind_res, ice_res,
                prob_attack, prob_technique, prob_inspirit, prob_guard, prob_loaf
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            y["code"], y["name"], y["rank"], y["tribe"], y["attribute"],
            y["hp"], y["str_stat"], y["spr_stat"], y["def_stat"], y["spd_stat"],
            y["attack_id"], y["technique_id"], y["soultimate_id"],
            y["inspirit_id"], y["skill_id"], y["tier"],
            y["fire_res"], y["water_res"], y["lightning_res"],
            y["earth_res"], y["wind_res"], y["ice_res"],
            y["prob_attack"], y["prob_technique"], y["prob_inspirit"],
            y["prob_guard"], y["prob_loaf"]
        ))
    
    print(f"Seeded {len(YOKAI_DATA)} yokai")


def main():
    print("Initializing database...")
    init_db()
    
    print("\nSeeding database...")
    try:
        seed_attacks()
        seed_techniques()
        seed_inspirits()
        seed_soultimates()
        seed_skills()
        seed_yokai()
        print("\nDatabase seeded successfully!")
    except Exception as e:
        print(f"\nError seeding database: {e}")
        raise


if __name__ == "__main__":
    main()

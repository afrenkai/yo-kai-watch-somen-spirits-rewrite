from app.core.database import get_duckdb, init_db

def test_database():
    print("Testing DuckDB backend...\n")
    print("Initializing database...")
    try:
        init_db()
        print("Database initialized\n")
    except Exception as e:
        print(f"Could not initialize database: {e}\n")
        return False

    print("Connecting to database...")
    try:
        db = get_duckdb()
        print("Connected to database\n")
    except Exception as e:
        print(f"Could not connect to database: {e}\n")
        return False
 
    print("Checking tables...")
    try:
        tables = db.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'main'
        """).fetchall()
        
        table_names = [t[0] for t in tables]
        expected_tables = ['yokai', 'attacks', 'techniques', 'skills', 
                          'inspirits', 'soultimates', 'users', 'teams', 
                          'battles', 'battle_logs', 'player_stats']
        
        print(f"   Found {len(table_names)} tables:")
        for table in table_names:
            status = "ok" if table in expected_tables else "bad"
            print(f"{status} {table}")
        print()
    except Exception as e:
        print(f"Failed to fetch tables: {e}\n")
        return False
    
    print("Testing query...")
    try:
        result = db.execute("SELECT COUNT(*) FROM yokai").fetchone()
        yokai_count = result[0]
        print(f"Found {yokai_count} yokai in database\n")
    except Exception as e:
        print(f"Failed to count yokai: {e}\n")
        return False
    
    print("All tests passed!")
    return True

if __name__ == "__main__":
    success = test_database()
    exit(0 if success else 1)

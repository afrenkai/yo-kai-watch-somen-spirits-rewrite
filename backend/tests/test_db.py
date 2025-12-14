import pytest
from app.core.database import get_db


class TestDatabaseTables:
    
    def test_attacks_table_exists(self, db_connection):
        result = db_connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attacks'").fetchone()
        assert result is not None
    
    def test_attacks_table_structure(self, db_connection):
        result = db_connection.execute("SELECT * FROM attacks LIMIT 1").fetchall()
        assert db_connection.description is not None
        columns = [desc[0] for desc in db_connection.description]
        assert 'id' in columns
        assert 'command' in columns
    
    def test_techniques_table_exists(self, db_connection):
        result = db_connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='techniques'").fetchone()
        assert result is not None
    
    def test_techniques_table_structure(self, db_connection):
        result = db_connection.execute("SELECT * FROM techniques LIMIT 1").fetchall()
        assert db_connection.description is not None
        columns = [desc[0] for desc in db_connection.description]
        assert 'id' in columns
        assert 'command' in columns
        assert 'element' in columns
    
    def test_soultimate_table_exists(self, db_connection):
        result = db_connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='soultimate'").fetchone()
        assert result is not None
    
    def test_soultimate_table_structure(self, db_connection):
        result = db_connection.execute("SELECT * FROM soultimate LIMIT 1").fetchall()
        assert db_connection.description is not None
        columns = [desc[0] for desc in db_connection.description]
        assert 'id' in columns
        assert 'command' in columns
    
    def test_inspirit_table_exists(self, db_connection):
        result = db_connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inspirit'").fetchone()
        assert result is not None
    
    def test_inspirit_table_structure(self, db_connection):
        result = db_connection.execute("SELECT * FROM inspirit LIMIT 1").fetchall()
        assert db_connection.description is not None
        columns = [desc[0] for desc in db_connection.description]
        assert 'id' in columns
        assert 'command' in columns
    
    def test_yokai_table_exists(self, db_connection):
        result = db_connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='yokai'").fetchone()
        assert result is not None
    
    def test_yokai_table_structure(self, db_connection):
        result = db_connection.execute("SELECT * FROM yokai LIMIT 1").fetchall()
        assert db_connection.description is not None
        columns = [desc[0] for desc in db_connection.description]
        assert 'id' in columns
        assert 'name' in columns
        assert 'tribe' in columns


class TestDatabaseCRUD:
    
    def test_query_all_yokai(self, db_connection):
        result = db_connection.execute("SELECT * FROM yokai").fetchall()
        assert isinstance(result, list)
    
    def test_query_yokai_by_id(self, db_connection):
        result = db_connection.execute("SELECT * FROM yokai WHERE id = ?", [1]).fetchone()
        # Result may be None if no data exists
        assert result is None or isinstance(result, tuple)
    
    def test_query_yokai_by_tribe(self, db_connection):
        result = db_connection.execute("SELECT * FROM yokai WHERE tribe = ?", ["Brave"]).fetchall()
        assert isinstance(result, list)
    
    def test_query_all_attacks(self, db_connection):
        result = db_connection.execute("SELECT * FROM attacks").fetchall()
        assert isinstance(result, list)
    
    def test_query_attack_by_id(self, db_connection):
        result = db_connection.execute("SELECT * FROM attacks WHERE id = ?", [1]).fetchone()
        # Result may be None if no data exists
        assert result is None or isinstance(result, tuple)
    
    def test_query_all_techniques(self, db_connection):
        result = db_connection.execute("SELECT * FROM techniques").fetchall()
        assert isinstance(result, list)
    
    def test_query_technique_by_attribute(self, db_connection):
        result = db_connection.execute("SELECT * FROM techniques WHERE element = ?", ["fire"]).fetchall()
        assert isinstance(result, list)
    
    def test_query_all_soultimates(self, db_connection):
        result = db_connection.execute("SELECT * FROM soultimate").fetchall()
        assert isinstance(result, list)
    
    def test_query_all_inspirits(self, db_connection):
        result = db_connection.execute("SELECT * FROM inspirit").fetchall()
        assert isinstance(result, list)
    
    def test_count_yokai(self, db_connection):
        result = db_connection.execute("SELECT COUNT(*) FROM yokai").fetchone()
        assert result[0] >= 0
    
    def test_count_attacks(self, db_connection):
        result = db_connection.execute("SELECT COUNT(*) FROM attacks").fetchone()
        assert result[0] >= 0


class TestDatabaseIntegrity:
    
    def test_no_null_yokai_names(self, db_connection):
        result = db_connection.execute("SELECT COUNT(*) FROM yokai WHERE name IS NULL").fetchone()
        assert result[0] == 0
    
    def test_yokai_resistances_valid(self, db_connection):
        result = db_connection.execute("SELECT * FROM yokai WHERE fire_res < 0 OR water_res < 0").fetchall()
        assert len(result) == 0
    
    def test_attack_bp_positive(self, db_connection):
        result = db_connection.execute("SELECT * FROM attacks WHERE lv1_power < 0").fetchall()
        assert len(result) == 0
    
    def test_technique_bp_positive(self, db_connection):
        result = db_connection.execute("SELECT * FROM techniques WHERE lv1_power < 0").fetchall()
        assert len(result) == 0


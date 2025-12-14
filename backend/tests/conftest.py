import pytest
import sys
import os
from typing import Generator
from fastapi.testclient import TestClient
from app.core.database import init_db, get_db
from main import socket_app


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def test_db():
    init_db(drop_existing=True)
    yield
    

@pytest.fixture(scope="function")
def db_connection(test_db):
    with get_db() as conn:
        yield conn


@pytest.fixture(scope="module")
def client(test_db) -> Generator:
    with TestClient(socket_app) as test_client:
        yield test_client


@pytest.fixture
def sample_yokai_data():
    return {
        'id': 1,
        'name': 'Test Yokai',
        'hp': 220,
        'str': 80,
        'spr': 75,
        'def': 70,
        'spd': 65,
        'fire_res': 1.0,
        'water_res': 1.0,
        'lightning_res': 1.0,
        'ice_res': 1.0,
        'earth_res': 1.0,
        'wind_res': 1.0,
        'tribe': 'Brave',
        'rank': 'A',
        'level': 50,
        'hp_iv': 0,
        'str_iv': 0,
        'spr_iv': 0,
        'def_iv': 0,
        'spd_iv': 0,
        'hp_gym': 0,
        'str_gym': 0,
        'spr_gym': 0,
        'def_gym': 0,
        'spd_gym': 0,
        'attitude_hp_boost': 0,
        'attitude_str_boost': 0,
        'attitude_spr_boost': 0,
        'attitude_def_boost': 0,
        'attitude_spd_boost': 0
    }


@pytest.fixture
def sample_attack_data():
    return {
        'id': 1,
        'name': 'Test Attack',
        'bp': 60,
        'hits': 1,
        'accuracy': 100
    }


@pytest.fixture
def sample_technique_data():
    return {
        'id': 1,
        'name': 'Test Technique',
        'bp': 80,
        'attribute': 'fire',
        'accuracy': 95,
        'spirit_cost': 20
    }


@pytest.fixture
def sample_team():
    return [
        {'id': 1, 'hp': 220},
        {'id': 2, 'hp': 200},
        {'id': 3, 'hp': 240}
    ]


@pytest.fixture
def sample_battle_state():
    return {
        'team1': [
            {'id': 1, 'hp': 220, 'max_hp': 220, 'spirit': 100},
            {'id': 2, 'hp': 200, 'max_hp': 200, 'spirit': 100},
            {'id': 3, 'hp': 240, 'max_hp': 240, 'spirit': 100}
        ],
        'team2': [
            {'id': 4, 'hp': 210, 'max_hp': 210, 'spirit': 100},
            {'id': 5, 'hp': 190, 'max_hp': 190, 'spirit': 100},
            {'id': 6, 'hp': 230, 'max_hp': 230, 'spirit': 100}
        ],
        'turn': 1,
        'log': [],
        'weather': None,
        'field_effects': []
    }

import pytest
from pydantic import ValidationError

from app.models.yokai import Yokai
from app.models.attack import Attack
from app.models.technique import Technique
from app.models.inspirit import Inspirit
from app.models.soultimate import Soultimate
from app.models.skill import Skill
from app.models.equipment import Equipment
from app.models.attitude import Attitude
from app.models.soul_gem import SoulGem


class TestYokaiModel:
    
    def test_yokai_creation_with_minimal_data(self):
        yokai = Yokai(id="001", name="Jibanyan")
        assert yokai.id == "001"
        assert yokai.name == "Jibanyan"
        assert yokai.fire_res == 1.0
        assert yokai.equipment_slots == 1
    
    def test_yokai_creation_with_full_data(self):
        yokai = Yokai(
            id="001",
            name="Jibanyan",
            bs_a_hp=100,
            bs_a_str=50,
            bs_a_spr=40,
            bs_a_def=45,
            bs_a_spd=55,
            bs_b_hp=250,
            bs_b_str=120,
            bs_b_spr=110,
            bs_b_def=115,
            bs_b_spd=130,
            fire_res=1.5,
            water_res=0.5,
            tribe="Charming",
            rank="D"
        )
        assert yokai.fire_res == 1.5
        assert yokai.water_res == 0.5
        assert yokai.tribe == "Charming"
    
    def test_yokai_resistance_defaults(self):
        yokai = Yokai(id="001", name="Test")
        assert yokai.fire_res == 1.0
        assert yokai.water_res == 1.0
        assert yokai.electric_res == 1.0
        assert yokai.earth_res == 1.0
        assert yokai.wind_res == 1.0
        assert yokai.ice_res == 1.0
    
    def test_yokai_serialization(self):
        yokai = Yokai(id="001", name="Jibanyan", tribe="Charming")
        data = yokai.model_dump()
        assert data["id"] == "001"
        assert data["name"] == "Jibanyan"
        assert data["tribe"] == "Charming"
    
    def test_yokai_from_dict(self):
        data = {
            "id": "002",
            "name": "Whisper",
            "tribe": "Brave",
            "rank": "C"
        }
        yokai = Yokai(**data)
        assert yokai.id == "002"
        assert yokai.name == "Whisper"


class TestAttackModel:
    
    def test_attack_creation_minimal(self):
        attack = Attack(id="A001", name="Punch")
        assert attack.id == "A001"
        assert attack.name == "Punch"
    
    def test_attack_with_stats(self):
        attack = Attack(
            id="A001",
            name="Punch",
            bp=40,
            hits=1,
            accuracy=100
        )
        assert attack.bp == 40
        assert attack.hits == 1
        assert attack.accuracy == 100
    
    def test_attack_serialization(self):
        attack = Attack(id="A001", name="Punch", bp=40)
        data = attack.model_dump()
        assert data["id"] == "A001"
        assert data["name"] == "Punch"


class TestTechniqueModel:
    
    def test_technique_creation(self):
        tech = Technique(id="T001", name="Blaze")
        assert tech.id == "T001"
        assert tech.name == "Blaze"
    
    def test_technique_with_attribute(self):
        tech = Technique(
            id="T001",
            name="Blaze",
            attribute="fire",
            bp=80,
            spirit_cost=20
        )
        assert tech.attribute == "fire"
        assert tech.bp == 80
        assert tech.spirit_cost == 20
    
    def test_technique_serialization(self):
        tech = Technique(id="T001", name="Blaze", attribute="fire")
        data = tech.model_dump()
        assert data["id"] == "T001"
        assert data["attribute"] == "fire"


class TestInspiritModel:
    
    def test_inspirit_creation(self):
        inspirit = Inspirit(id="I001", name="Terrorize")
        assert inspirit.id == "I001"
        assert inspirit.name == "Terrorize"
    
    def test_inspirit_with_effect(self):
        inspirit = Inspirit(
            id="I001",
            name="Terrorize",
            effect_type="stat_down",
            target_stat="def",
            magnitude=2
        )
        assert inspirit.effect_type == "stat_down"
        assert inspirit.target_stat == "def"
        assert inspirit.magnitude == 2


class TestSoultimateModel:
    
    def test_soultimate_creation(self):
        soultimate = Soultimate(id="S001", name="Paws of Fury")
        assert soultimate.id == "S001"
        assert soultimate.name == "Paws of Fury"
    
    def test_soultimate_with_power(self):
        soultimate = Soultimate(
            id="S001",
            name="Paws of Fury",
            bp=120,
            attribute="fire",
            target="single"
        )
        assert soultimate.bp == 120
        assert soultimate.attribute == "fire"
        assert soultimate.target == "single"


class TestSkillModel:
    
    def test_skill_creation(self):
        skill = Skill(id=1, name="Popularity")
        assert skill.id == 1
        assert skill.name == "Popularity"
    
    def test_skill_with_effect(self):
        skill = Skill(
            id=1,
            name="Popularity",
            effect_type="stat_boost",
            magnitude=1.2
        )
        assert skill.effect_type == "stat_boost"
        assert skill.magnitude == 1.2


class TestEquipmentModel:
    
    def test_equipment_creation(self):
        equipment = Equipment(id=1, name="Swords of the Gods")
        assert equipment.id == 1
        assert equipment.name == "Swords of the Gods"
    
    def test_equipment_with_stats(self):
        equipment = Equipment(
            id=1,
            name="Swords of the Gods",
            str_bonus=20,
            spr_bonus=10,
            def_bonus=5
        )
        assert equipment.str_bonus == 20
        assert equipment.spr_bonus == 10
        assert equipment.def_bonus == 5


class TestAttitudeModel:
    
    def test_attitude_creation(self):
        attitude = Attitude(id=1, name="Rough")
        assert attitude.id == 1
        assert attitude.name == "Rough"
    
    def test_attitude_with_bonuses(self):
        attitude = Attitude(
            id=1,
            name="Rough",
            str_boost=15,
            spr_boost=-10,
            def_boost=5
        )
        assert attitude.str_boost == 15
        assert attitude.spr_boost == -10
        assert attitude.def_boost == 5


class TestSoulGemModel:
    
    def test_soul_gem_creation(self):
        gem = SoulGem(id=1, name="Jibanyan's Soul Gem")
        assert gem.id == 1
        assert gem.name == "Jibanyan's Soul Gem"
    
    def test_soul_gem_with_yokai_id(self):
        gem = SoulGem(
            id=1,
            name="Jibanyan's Soul Gem",
            yokai_id="001",
            bonus_stat="str",
            bonus_value=30
        )
        assert gem.yokai_id == "001"
        assert gem.bonus_stat == "str"
        assert gem.bonus_value == 30

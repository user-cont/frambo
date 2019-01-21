from frambo.dict_in_redis import PersistentDict
import pytest
from uuid import uuid4


class TestPersistentDict:

    @pytest.fixture
    def db(self):
        return PersistentDict(hash_name=str(uuid4()))

    @pytest.fixture
    def dictionary(self):
        return {"key": "some value",
                "key2": ["an", "array"],
                "key3": {"a": "dictionary", "b": 2, "c": ["one"]}
                }

    def test_one_by_one(self, db, dictionary):
        for key, value in dictionary.items():
            assert key not in db
            db[key] = value
            assert key in db
            assert db[key] == value
            del db[key]
            assert key not in db

    def test_more_keys(self, db, dictionary):
        assert len(db) == 0
        for key, value in dictionary.items():
            assert key not in db
            db[key] = value
        assert len(db) == len(dictionary)
        assert len(db.get_all()) == len(dictionary)
        assert db.get_all() == dictionary
        assert len(db.items()) == len(dictionary)
        assert db.keys() == dictionary.keys()
        db.clear()
        assert len(db) == 0

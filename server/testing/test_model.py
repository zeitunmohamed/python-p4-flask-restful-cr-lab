import pytest
from models import db, Plant
from main import app


class TestPlant:
    '''Plant model in models.py'''

    def test_can_instantiate(self):
        '''Can be instantiated with a name, image, and price.'''
        p = Plant(
            name="Douglas Fir",
            image="https://example.com/fir.png",
            price=19.99
        )
        assert p.name == "Douglas Fir"
        assert p.image == "https://example.com/fir.png"
        assert p.price == 19.99

    def test_can_be_created(self):
        '''Can create records that can be committed to the database.'''
        with app.app_context():
            p = Plant(
                name="Douglas Fir",
                image="https://example.com/fir.png",
                price=19.99
            )
            db.session.add(p)
            db.session.commit()
            assert p.id is not None
            db.session.delete(p)
            db.session.commit()

    def test_can_be_retrieved(self):
        '''Can be used to retrieve records from the database.'''
        with app.app_context():
            p = Plant(
                name="Douglas Fir",
                image="https://example.com/fir.png",
                price=19.99
            )
            db.session.add(p)
            db.session.commit()
            plants = Plant.query.all()
            assert len(plants) > 0
            db.session.delete(p)
            db.session.commit()

    def test_can_be_serialized(self):
        '''Can serialize to dictionary using to_dict().'''
        with app.app_context():
            p = Plant(
                name="Douglas Fir",
                image="https://example.com/fir.png",
                price=19.99
            )
            db.session.add(p)
            db.session.commit()

            p_dict = Plant.query.filter_by(name="Douglas Fir").first().to_dict()
            assert isinstance(p_dict, dict)
            assert p_dict["name"] == "Douglas Fir"
            assert "id" in p_dict
            assert "image" in p_dict
            assert "price" in p_dict

            db.session.delete(p)
            db.session.commit()

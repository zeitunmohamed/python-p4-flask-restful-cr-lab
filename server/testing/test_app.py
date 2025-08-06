import json
import pytest

from models import db, Plant
from main import app


class TestApp:
    '''Flask application tests'''

    def test_plants_get_route(self):
        '''has a resource available at "/plants".'''
        response = app.test_client().get('/plants')
        assert response.status_code == 200

    def test_plants_get_route_returns_list_of_plant_objects(self):
        '''returns JSON representing Plant objects at "/plants".'''
        with app.app_context():
            p = Plant(name="Douglas Fir", image="example.png", price=10.0)
            db.session.add(p)
            db.session.commit()

            response = app.test_client().get('/plants')
            data = json.loads(response.data.decode())
            assert type(data) == list
            assert any(record['name'] == "Douglas Fir" for record in data)

            db.session.delete(p)
            db.session.commit()

    def test_plants_post_route_creates_plant_record_in_db(self):
        '''allows users to create Plant records through the "/plants" POST route.'''
        response = app.test_client().post(
            '/plants',
            json={
                "name": "Live Oak",
                "image": "https://example.com/oak.png",
                "price": 250.00,
            }
        )
        assert response.status_code == 201

        with app.app_context():
            lo = Plant.query.filter_by(name="Live Oak").first()
            assert lo is not None
            assert lo.name == "Live Oak"
            db.session.delete(lo)
            db.session.commit()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        with app.app_context():
            p = Plant(name="Maple", image="maple.png", price=15.0)
            db.session.add(p)
            db.session.commit()

            response = app.test_client().get(f'/plants/{p.id}')
            assert response.status_code == 200

            db.session.delete(p)
            db.session.commit()

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        with app.app_context():
            p = Plant(name="Pine", image="pine.png", price=12.0)
            db.session.add(p)
            db.session.commit()

            response = app.test_client().get(f'/plants/{p.id}')
            data = json.loads(response.data.decode())

            assert type(data) == dict
            assert data["name"] == "Pine"

            db.session.delete(p)
            db.session.commit()

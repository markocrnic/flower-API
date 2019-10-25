import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../app'))

from interface import app
from db.dbconnect import connection
from flask import json


# Test DB connection
def test_db_connection_successful():
    c, conn = connection()
    assert c and conn
    c.close()
    conn.close()


# Test GET all flowers successfully
def test_get_all_flowers_succsessful():
    response = app.test_client().get('/flowers/')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200 or response.status_code == 204


'''
# Test POST flower successfully
def test_post_flower_succsessful():
    response = app.test_client().post('/flowers/', json={
        "description": "description2",
        "name_lat": "name_lat2",
        "name_ser": "name_ser2",
        "watering_period": "5"
    })

    data = json.loads(response.get_data(as_text=True))

    assert data == {"msg": "New flower added to DB."} and response.status_code == 201
'''


# Test POST flower invalid data
def test_post_flower_unsuccsessful():
    response = app.test_client().post('/flowers/', json={
        "description": "description2",
        "name_lat": "name_lat2",
        "name_ser": "name_ser2"
    })

    data = json.loads(response.get_data(as_text=True))

    assert data == {'msg': 'Data is not valid.'} and response.status_code == 403


# Test Method not allowed
def test_method_not_allowed():
    response = app.test_client().put('/flowers/', json={
        "description": "description2",
        "name_lat": "name_lat2",
        "name_ser": "name_ser2",
        "watering_period": "5"
    })

    assert response.status_code == 405


# Test GET flower by id successfully
def test_get_flower_by_id_succsessful():
    response = app.test_client().get('/flowers/20')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200 or data == "No data to return."


'''
# Test PUT flower by id successfully
def test_put_user_by_id_succsessful():
    response = app.test_client().put('/users/20/', json={
        "description": "Poreklom iz Afrike, Azije i Australije. Ime potiče od grčke reči Drakanija- ženski zmaj. Rod sadrži 40 vrsta. Jedne su od omiljlenih biljaka zbog svoje otpornosti i lakog uzgajanja. Rastu kao grm koji se iz godina razvija u stablo. Raste do 2,5 m visine u sobnim uslovima i prečnika 80 do 120 cm. Raste sporo 10 do 15 cm godišnje. U prosečnim uslovima,leti 1 do 2 puta nedeljno, zimi 1 u 10 dana. Potrebno je naći ravnotežu. Biljka ne sme da stoji u vodi ali ni da se potpuno isuši.",
        "flower_id": "20",
        "name_lat": "Dracaena",
        "name_ser": "Zmajevac",
        "watering_period": "7"
    })

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201 and data == {"msg": "New flower added to DB."} or data == {"msg": "Flower with flower_id 20 is updated."} and response.status_code == 200
'''


# Test DELETE flower by id not existing in DB
def test_delete_flower_by_id_not_exist_in_db():
    response = app.test_client().delete('/flowers/6969420666')

    data = json.loads(response.get_data(as_text=True))

    assert data == {"msg": "Flower with flower_id 6969420666 does not exist in DB."} and response.status_code == 200


# Test Method not allowed /flowers/<id>
def test_method_not_allowed_flower_with_id():
    response = app.test_client().post('/flowers/666', json={
        "description": "description2",
        "name_lat": "name_lat2",
        "name_ser": "name_ser2",
        "watering_period": "5"
    })

    assert response.status_code == 405

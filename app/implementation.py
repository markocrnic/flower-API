from dbconnect import connection

import json


def getAllFlowers():
    try:
        c, conn = connection()

        data = c.execute('SELECT * FROM flower')
        data = c.fetchall()
        payload = []

        if data is not None and c.rowcount != 0:
            for flower in data:
                content = {"flower_id": str(flower[0]), "name_ser": flower[1], "name_lat": flower[2], "description": flower[3],
                           "watering_period": str(flower[4])}
                payload.append(content)
            c.close()
            conn.close()
            return payload
        else:
            return {'msg': 'No data to return.'}
    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {'msg': 'Something went wrong while fetching flowers.'}, 500


def postFlower(request):
    try:
        c, conn = connection()

        print('Starting execute')
        print(request.json['name_ser'], request.json['name_lat'], request.json['description'], request.json['watering_period'])
        c.execute('INSERT INTO flower (name_ser, name_lat, description, watering_period) values (%s, %s, %s, %s)', (str(request.json['name_ser']), str(request.json['name_lat']), str(request.json['description']), str(request.json['watering_period'])))
        conn.commit()

        c.close()
        conn.close()
        return {"msg": "New flower added to DB."}, 201

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while inserting flower to DB."}, 500


def getFlowerByID(flower_id):
    try:
        c, conn = connection()
        data = c.execute('SELECT * FROM flower where flower_id = ' + str(flower_id))
        data = c.fetchone()
        if data is not None and c.rowcount != 0:
            content = {"flower_id": str(data[0]), "name_ser": data[1], "name_lat": data[2], "description": data[3],
                           "watering_period": str(data[4])}
            c.close()
            conn.close()
            return content
        else:
            c.close()
            conn.close()
            return "No data to return."

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while fetching flower by id."}, 500


def putFlowerByID(request, flower_id):
    try:
        c, conn = connection()

        data = getFlowerByID(flower_id)
        if data == "No data to return.":
            return postFlower(request)
        else:
            putData = putDataCheck(request, data)
            if putData == "Something went wrong in mapping data.":
                return {"msg": "Something went wrong in mapping data."}, 500
            c.execute('UPDATE flower SET flower_id = %s, name_ser = %s, name_lat = %s, description = %s, watering_period = %s WHERE flower_id = %s',(str(flower_id), putData[0], putData[1], putData[2], putData[3], str(flower_id)))
            conn.commit()
            print("Flower with flower_id " + str(flower_id) + " is updated.")

            c.close()
            conn.close()
            return {"msg": "Flower with flower_id " + str(flower_id) + " is updated."}

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while updating flower."}


def deleteFlowerByID(flower_id):
    try:
        c, conn = connection()

        data = getFlowerByID(flower_id)
        if data == "No data to return.":
            return {"msg": "Flower with flower_id " + str(flower_id) + " does not exist in DB."}
        else:
            c.execute('DELETE FROM flower WHERE flower_id = %s', (str(flower_id)))
            conn.commit()
            print("Flower with flower_id " + str(flower_id) + " is deleted from DB.")

            c.close()
            conn.close()
            return {"msg": "Flower with flower_id " + str(flower_id) + " is deleted from DB."}

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while deleting flower"}, 500


def putDataCheck(request, data):
    try:
        listData = []
        for field in data:
            listData.append(data[field])
        name_ser = listData[1]
        name_lat = listData[2]
        description = listData[3]
        watering_period = listData[4]
        if 'name_ser' in request.json:
            name_ser = request.json['name_ser']
        if 'name_lat' in request.json:
            name_lat = request.json['name_lat']
        if 'description' in request.json:
            description = request.json['description']
        if 'watering_period' in request.json:
            watering_period = request.json['watering_period']
        updateData = [name_ser, name_lat, description, watering_period]

        return updateData
    except:
        return "Something went wrong in mapping data."









from dbconnect import connection
from flask import jsonify
import implementation as operations


def querydb(data, operation, check=None, flower_id=None, request=None):
    try:
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        if operation == 'POST':

            c.execute('INSERT INTO flower (name_ser, name_lat, description, watering_period) values (%s, %s, %s, %s)', (
            str(request.json['name_ser']), str(request.json['name_lat']), str(request.json['description']),
            str(request.json['watering_period'])))
            conn.commit()

            c.close()
            conn.close()
            return {"msg": "New flower added to DB."}, 201

        if operation == 'GET':

            c.execute(data)

            if check == 'list':
                data = c.fetchall()
                payload = []

                if data is not None and c.rowcount != 0:
                    for flower in data:
                        content = {"flower_id": str(flower[0]), "name_ser": flower[1], "name_lat": flower[2],
                                   "description": flower[3],
                                   "watering_period": str(flower[4])}
                        payload.append(content)
                    c.close()
                    conn.close()
                    return jsonify(payload)
                else:
                    return {'msg': 'No data to return.'}, 204

            if check == 'tuple':
                data = c.fetchone()
                if data is not None and c.rowcount != 0:
                    content = {"flower_id": str(data[0]), "name_ser": data[1], "name_lat": data[2],
                               "description": data[3],
                               "watering_period": str(data[4])}
                    c.close()
                    conn.close()
                    return content
                else:
                    c.close()
                    conn.close()
                    return "No data to return."

        if operation == 'PUT':

            data = operations.getFlowerByID(flower_id)
            if data == "No data to return.":
                return operations.postFlower(request)
            else:
                putData = operations.putDataCheck(request, data)
                if putData == "Something went wrong in mapping data.":
                    return {"msg": "Something went wrong in mapping data."}, 500
                c.execute(
                    'UPDATE flower SET flower_id = %s, name_ser = %s, name_lat = %s, description = %s, watering_period = %s WHERE flower_id = %s',
                    (str(flower_id), putData[0], putData[1], putData[2], putData[3], str(flower_id)))
                conn.commit()
                print("Flower with flower_id " + str(flower_id) + " is updated.")

                c.close()
                conn.close()
                return {"msg": "Flower with flower_id " + str(flower_id) + " is updated."}

        if operation == 'DELETE':
            data = operations.getFlowerByID(flower_id)
            if data == "No data to return.":
                return {"msg": "Flower with flower_id " + str(flower_id) + " does not exist in DB."}
            else:
                c.execute('DELETE FROM flower WHERE flower_id = ' + (str(flower_id)))
                conn.commit()
                print("Flower with flower_id " + str(flower_id) + " is deleted from DB.")

                c.close()
                conn.close()
                return {"msg": "Flower with flower_id " + str(flower_id) + " is deleted from DB."}

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {'msg': 'Something went wrong while executing ' + operation + ' operation on flowers.'}, 500
from dbconnect import connection
from flask import jsonify
import implementation as operations


def querydb(data, operation, check=None, flower_id=None):
    try:
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        if operation == 'POST':

            c.execute(data)
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

            c.execute(data)
            conn.commit()
            print("Flower with flower_id " + str(flower_id) + " is updated.")

            c.close()
            conn.close()
            return {"msg": "Flower with flower_id " + str(flower_id) + " is updated."}

        if operation == 'DELETE':
            c.execute(data)
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
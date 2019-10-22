from dbquery import querydb
from schema import Schema, And, Use


def getAllFlowers():
    data = 'SELECT * FROM flower'
    return querydb(data, operation='GET', check='list')


def postFlower(request):
    data = "INSERT INTO flower (name_ser, name_lat, description, watering_period) values ('" + str(
        request.json['name_ser']) + "', '" + str(request.json['name_lat']) + "', '" + str(
        request.json['description']) + "', '" + str(request.json['watering_period']) + "')"

    return querydb(data, operation='POST')


def getFlowerByID(flower_id):
    data = 'SELECT * FROM flower where flower_id = ' + str(flower_id)
    return querydb(data, 'GET', 'tuple', flower_id=flower_id)


def putFlowerByID(request, flower_id):
    data = getFlowerByID(flower_id)
    if data == "No data to return.":
        return postFlower(request)
    else:
        putData = putDataCheck(request, data)
        if putData == "Something went wrong in mapping data.":
            return {"msg": "Something went wrong in mapping data."}, 500
        data = "UPDATE flower SET flower_id = '" + str(flower_id) + "', name_ser = '" + putData[0] + "', name_lat = '" + \
               putData[1] + "', description = '" + putData[2] + "', watering_period = '" + putData[
                   3] + "' WHERE flower_id = '" + str(flower_id) + "'"
        return querydb(data, 'PUT', flower_id=flower_id)


def deleteFlowerByID(flower_id):

    data = getFlowerByID(flower_id)
    if data == "No data to return.":
        return {"msg": "Flower with flower_id " + str(flower_id) + " does not exist in DB."}
    else:
        data = 'DELETE FROM flower WHERE flower_id = ' + (str(flower_id))
        return querydb(data, 'DELETE', flower_id=flower_id)


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


def getSchema():
    return Schema({'name_ser': And(str, len),
                   'name_lat': And(str, len),
                   'description': And(str, len),
                   'watering_period': And(Use(int))})

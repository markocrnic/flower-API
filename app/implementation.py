from dbquery import querydb


def getAllFlowers():

    data = 'SELECT * FROM flower'
    return querydb(data, operation='GET', check='list')


def postFlower(request):

    return querydb("", operation='POST', request=request)


def getFlowerByID(flower_id):

    data = 'SELECT * FROM flower where flower_id = ' + str(flower_id)
    return querydb(data, 'GET', 'tuple', flower_id=flower_id)


def putFlowerByID(request, flower_id):

    return querydb("", 'PUT', flower_id=flower_id, request=request)


def deleteFlowerByID(flower_id):

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


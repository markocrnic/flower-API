from flask import Flask, request, jsonify
from schema import Schema, And, Use

import implementation as implementation


app = Flask(__name__)

schema = Schema({'name_ser': And(str, len),
                 'name_lat': And(str, len),
                 'description': And(str, len),
                 'watering_period': And(Use(int))})


@app.route('/flowers/', methods=['GET', 'POST'])
def flowersGlobal():
    try:
        if request.method == 'GET':
            data = implementation.getAllFlowers()
            return jsonify(data)
        elif request.method == 'POST':
            try:
                validated = schema.validate(request.json)
            except:
                return 'Data is not valid.'
            return implementation.postFlower(request)
    except:
        return 'Something went wrong at /flowers/'


@app.route('/flowers/<int:flower_id>', methods=['GET', 'PUT', 'DELETE'])
def flowersWithID(flower_id):
    try:
        if request.method == 'GET':
            return implementation.getFlowerByID(flower_id)
        elif request.method == 'PUT':
            return implementation.putFlowerByID(request, flower_id)
        elif request.method == 'DELETE':
            return implementation.deleteFlowerByID(flower_id)
        else:
            return "Check request again."
    except Exception as e:
        print(e)
        return "Something went wrong at /flowers/<int:flower_id>"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, request
from flask_cors import CORS
from api_management.jaeger import initializejaeger
from flask_opentracing import FlaskTracing
import implementation as implementation


app = Flask(__name__)
CORS(app)

# Initialize jaeger and flask tracer
jaeger_tracer = initializejaeger()
tracing = FlaskTracing(jaeger_tracer)


@app.route('/flowers/', methods=['GET', 'POST'])
@tracing.trace()
def flowersGlobal():
    with jaeger_tracer.start_active_span(
            'Flowers-API endpoint /flowers/') as scope:
        scope.span.log_kv({'event': 'Calling endpoint /flowers/', 'request_method': request.method})
        try:
            if request.method == 'GET':
                data = implementation.getAllFlowers()
                return data
            elif request.method == 'POST':
                try:
                    schema = implementation.getSchema()
                    schema.validate(request.json)
                except:
                    return {'msg': 'Data is not valid.'}, 403
                return implementation.postFlower(request)
        except:
            return {'msg': 'Something went wrong at /flowers/'}, 500


@app.route('/flowers/<int:flower_id>/', methods=['GET', 'PUT', 'DELETE'])
@tracing.trace()
def flowersWithID(flower_id):
    with jaeger_tracer.start_active_span(
            'Flowers-API endpoint /flowers/<int:flower_id>/') as scope:
        scope.span.log_kv({'event': 'Calling endpoint /flowers/<int:flower_id>/', 'request_method': request.method})
        try:
            if request.method == 'GET':
                return implementation.getFlowerByID(flower_id)
            elif request.method == 'PUT':
                return implementation.putFlowerByID(request, flower_id)
            elif request.method == 'DELETE':
                return implementation.deleteFlowerByID(flower_id)
            else:
                return {"msg": "Check request again."}, 403
        except Exception as e:
            print(e)
            return {"msg": "Something went wrong at /flowers/<int:flower_id>"}, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
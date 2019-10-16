from flask import Flask, jsonify, request
import cop_prediction as cop
import clustering

# declare constants
HOST = '0.0.0.0'
PORT = 8081

# initialize flask application
app = Flask(__name__)

# Prediccion
@app.route('/api/train', methods=['POST'])
def train():
    cop_model = cop.COP()
    accuracy = cop_model.fit_grupo_frio_1()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict', methods=['POST'])
def predict():
    # get data to be predicted
    #X = request.get_json()
    X = { "POTENCIA GRUPO FRÍO 1" : 4, "POTENCIA TERMICA GRUPO FRIO 1": 4, "TEMPERATURA EXTERIOR": 4}
    X = [[float(X['POTENCIA GRUPO FRÍO 1']), float(X['POTENCIA TERMICA GRUPO FRIO 1']), float(X['TEMPERATURA EXTERIOR'])]]
    cop_model = cop.COP()
    prediction = cop_model.predict_grupo_frio_1(X)
    print(prediction)
    return jsonify({'cop_grupo_frio_1': prediction[0]})

# Clustering
@app.route('/api/train_kmeans', methods=['POST'])
def train_kmeans():
    kmeans_ = clustering.KMeans_()
    centroides = kmeans_.kmeans_carlos()
    return jsonify({'centroides': centroides})

@app.route('/api/predict_kmeans', methods=['POST'])
def predict_kmeans():
    # get data to be predicted
    #X = request.get_json()
    X = {'POTENCIA BOMBA CALOR CARLOS' : 6.22666645050049, 'POTENCIA TERMICA BOMBA CALOR CARLOS': 181.58,
        'TEMPERATURA EXTERIOR' : 33.02, 'TEMPERATURA SALIDA BOMBA CALOR CARLOS': 13.9333333969116}

    X = [[float(X['POTENCIA BOMBA CALOR CARLOS']), float(X['POTENCIA TERMICA BOMBA CALOR CARLOS']),
          float(X['TEMPERATURA EXTERIOR']), float(X['TEMPERATURA SALIDA BOMBA CALOR CARLOS'])]]
    kmeans_ = clustering.KMeans_()
    prediction = kmeans_.predict_carlos(X)
    print(prediction)
    return jsonify({'cluster carlos': str(prediction[0])})


if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)
from flask import Flask, jsonify, request
from sklearn.externals import joblib
import cop_prediction as cop

# declare constants
HOST = '0.0.0.0'
PORT = 8081

# initialize flask application
app = Flask(__name__)

@app.route('/api/train', methods=['POST'])
def train():
    cop_model = cop.COP()
    accuracy = cop_model.fit_grupo_frio_1()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict', methods=['POST'])
def predict():
    # get data to be predicted
    X = request.get_json()
    X = [[float(X['POTENCIA GRUPO FRÍO 1']), float(X['POTENCIA TERMICA GRUPO FRIO 1']), float(X['TEMPERATURA EXTERIOR'])]]
    cop_model = cop.COP()
    prediction = cop_model.predict_grupo_frio_1(X)
    print(prediction.shape)
    return jsonify({'cop_grupo_frio_1': prediction[0]})


if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)
from flask import Flask, jsonify
from flask_cors import CORS
import copy
import cop_prediction as cop
import clustering
import dataset

# declare constants
HOST = '0.0.0.0'
PORT = 8081

# initialize flask application
app = Flask(__name__)

CORS(app)

# Datos
obj = dataset.Dataset()
data = obj.read_dataset_lectura()
dataFrio1 = copy.deepcopy(data)
dataCarlos = copy.deepcopy(data)
dataFelipe = copy.deepcopy(data)

# Prediccion
@app.route('/api/train_frio_1', methods=['GET'])
def train_frio_1():
    cop_model = cop.COP()
    accuracy = cop_model.fit_grupo_frio_1()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict_frio_1', methods=['GET'])
def predict_frio_1():
    cop_model = cop.COP()
    diccionario = []
    for i in range(0, 10):
        df = dataFrio1.iloc[i]
        # get data to be predicted
        X = [[float(df['POTENCIA GRUPO FRÍO 1']), float(df['POTENCIA TERMICA GRUPO FRIO 1']),
              float(df['TEMPERATURA EXTERIOR'])]]
        prediction_ = cop_model.predict_grupo_frio_1(X)
        prediction = float(prediction_[0])
        valorReal = float(df['C_O_P MÁQUINA GRUPO FRÍO 1'])
        # COP malo --> diagnostico (clustering)
        kmeans_prediction = ' '
        if (((valorReal <= 3.5) or (valorReal >= 4.5)) and ((prediction <= 3.5) or (prediction >= 4.5))
                or (valorReal <= prediction - 0.5) or (valorReal >= prediction + 0.5)):
            kmeans_ = clustering.KMeans_()
            kmeans_prediction = kmeans_.predict_frio_1(X)
        # Diccionario con todas las variables de un registro que se va retornar
        df.loc['Diagnostico'] = kmeans_prediction
        df.loc['C_O_P MÁQUINA GRUPO FRÍO 1 PREDICHO'] = prediction
        registro_dict = df.to_dict()
        diccionario.append(registro_dict)
    dataFrio1.drop(range(0, 10), inplace=True)
    dataFrio1.reset_index(drop=True, inplace=True)
    return jsonify(diccionario)

@app.route('/api/train_carlos', methods=['GET'])
def train_carlos():
    cop_model = cop.COP()
    accuracy = cop_model.fit_carlos()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict_carlos', methods=['GET'])
def predict_carlos():
    cop_model = cop.COP()
    diccionario = []
    for i in range(0, 10):
        df = dataCarlos.iloc[i]
        # get data to be predicted
        X = [[float(df['POTENCIA BOMBA CALOR CARLOS']), float(df['POTENCIA TERMICA BOMBA CALOR CARLOS']),
              float(df['TEMPERATURA EXTERIOR']), float(df['TEMPERATURA SALIDA BOMBA CALOR CARLOS'])]]
        prediction_ = cop_model.predict_carlos(X)
        prediction = float(prediction_[0])
        valorReal = float(df['C_O_P BOMBA CALOR CARLOS'])
        # COP malo --> diagnostico (clustering)
        kmeans_prediction = ' '
        if (((valorReal <= 3.5) or (valorReal >= 4.5)) and ((prediction <= 3.5) or (prediction >= 4.5))
                or (valorReal <= prediction - 0.5) or (valorReal >= prediction + 0.5)):
            kmeans_ = clustering.KMeans_()
            kmeans_prediction = kmeans_.predict_carlos(X)
        # Diccionario con todas las variables de un registro que se va retornar
        df.loc['Diagnostico'] = kmeans_prediction
        df.loc['C_O_P BOMBA CALOR CARLOS PREDICHO'] = prediction
        registro_dict = df.to_dict()
        diccionario.append(registro_dict)
    dataCarlos.drop(range(0, 10), inplace=True)
    dataCarlos.reset_index(drop=True, inplace=True)
    return jsonify(diccionario)

@app.route('/api/train_felipe', methods=['GET'])
def train_felipe():
    cop_model = cop.COP()
    accuracy = cop_model.fit_felipe()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict_felipe', methods=['GET'])
def predict_felipe():
    cop_model = cop.COP()
    diccionario = []
    for i in range(0, 10):
        df = dataFelipe.iloc[i]
        # get data to be predicted
        X = [[float(df['POTENCIA BOMBA CALOR FELIPE']), float(df['POTENCIA TERMICA BOMBA CALOR FELIPE']),
              float(df['TEMPERATURA EXTERIOR']), float(df['TEMPERATURA SALIDA BOMBA CALOR FELIPE'])]]
        prediction_ = cop_model.predict_felipe(X)
        prediction = float(prediction_[0])
        valorReal = float(df['C_O_P BOMBA CALOR FELIPE'])
        # COP malo --> diagnostico (clustering)
        kmeans_prediction = ' '
        if (((valorReal <= 3.5) or (valorReal >= 4.5)) and ((prediction <= 3.5) or (prediction >= 4.5))
                or (valorReal <= prediction - 0.5) or (valorReal >= prediction + 0.5)):
            kmeans_ = clustering.KMeans_()
            kmeans_prediction = kmeans_.predict_felipe(X)
        # Diccionario con todas las variables de un registro que se va retornar
        df.loc['Diagnostico'] = kmeans_prediction
        df.loc['C_O_P BOMBA CALOR FELIPE PREDICHO'] = prediction
        registro_dict = df.to_dict()
        diccionario.append(registro_dict)
    dataFelipe.drop(range(0, 10), inplace=True)
    dataFelipe.reset_index(drop=True, inplace=True)
    return jsonify(diccionario)

# Clustering
@app.route('/api/train_kmeans_frio_1', methods=['GET'])
def train_kmeans_frio_1():
    kmeans_ = clustering.KMeans_()
    centroides = kmeans_.kmeans_frio_1()
    return jsonify({'centroides': centroides})

@app.route('/api/train_kmeans_carlos', methods=['GET'])
def train_kmeans_carlos():
    kmeans_ = clustering.KMeans_()
    centroides = kmeans_.kmeans_carlos()
    return jsonify({'centroides': centroides})

@app.route('/api/train_kmeans_felipe', methods=['GET'])
def train_kmeans_felipe():
    kmeans_ = clustering.KMeans_()
    centroides = kmeans_.kmeans_felipe()
    return jsonify({'centroides': centroides})

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)

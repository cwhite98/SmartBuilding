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
print("Dataset leido")

# Prediccion
@app.route('/api/train_frio_1', methods=['POST'])
def train_frio_1():
    cop_model = cop.COP()
    accuracy = cop_model.fit_grupo_frio_1()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict_frio_1', methods=['POST'])
def predict_frio_1():
    cop_model = cop.COP()
    diccionario = {}
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
        print('Diagnostico frio 1:', kmeans_prediction)
        # Diccionario con todas las variables de un registro que se va retornar
        df.loc['Diagnostico'] = kmeans_prediction
        df.loc['C_O_P MÁQUINA GRUPO FRÍO 1 PREDICHO'] = prediction
        registro_dict = df.to_dict()
        var = 'registro_' + str(i)
        diccionario[var] = registro_dict
    dataFrio1.drop(range(0, 10), inplace=True)
    length = dataFrio1.shape
    index_ = range(0, length[0])
    dataFrio1.index = index_
    return jsonify(diccionario)

@app.route('/api/train_carlos', methods=['POST'])
def train_carlos():
    cop_model = cop.COP()
    accuracy = cop_model.fit_carlos()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict_carlos', methods=['POST'])
def predict_carlos():
    cop_model = cop.COP()
    diccionario = {}
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
        print('Diagnostico frio 1:', kmeans_prediction)
        # Diccionario con todas las variables de un registro que se va retornar
        df.loc['Diagnostico'] = kmeans_prediction
        df.loc['C_O_P BOMBA CALOR CARLOS PREDICHO'] = prediction
        registro_dict = df.to_dict()
        var = 'registro_' + str(i)
        diccionario[var] = registro_dict
    dataCarlos.drop(range(0, 10), inplace=True)
    length = dataCarlos.shape
    index_ = range(0, length[0])
    dataCarlos.index = index_
    return jsonify(diccionario)

# Clustering
@app.route('/api/train_kmeans_frio_1', methods=['POST'])
def train_kmeans_frio_1():
    kmeans_ = clustering.KMeans_()
    centroides = kmeans_.kmeans_frio_1()
    return jsonify({'centroides': centroides})

@app.route('/api/train_kmeans_carlos', methods=['POST'])
def train_kmeans_carlos():
    kmeans_ = clustering.KMeans_()
    centroides = kmeans_.kmeans_carlos()
    return jsonify({'centroides': centroides})

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)

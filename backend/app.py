from flask import Flask, jsonify
import cop_prediction as cop
import clustering
import pandas as pd

# declare constants
HOST = '0.0.0.0'
PORT = 8081

# initialize flask application
app = Flask(__name__)

# Datos
columns = ['POTENCIA TRAFO 2', 'POTENCIA TRAFO 3', 'POTENCIA TRAFO 4', 'POTENCIA TRAFO 5', 'POTENCIA MEDIA CONECTADA',
           'PERIODO P6', 'CONTROL FRÍO', 'CONTROL CALOR', 'CAPACIDAD BOMBA CALOR FELIPE %', 'CAPACIDAD BOMBA CALOR CARLOS %',
           'POTENCIA BOMBA CALOR FELIPE', 'POTENCIA BOMBA CALOR CARLOS', 'TEMPERATURA AMBIENTE BOMBA CALOR CARLOS',
           'TEMPERATURA AMBIENTE BOMBA CALOR FELIPE', 'TEMPERATURA EXTERIOR', 'CAPACIDAD GRUPO DE FRÍO 1', 'CAPACIDAD GRUPO DE FRÍO 2',
           'POTENCIA GRUPO FRÍO 1', 'POTENCIA GRUPO FRÍO 2', 'ENTRADA AGUA A TORRE 1', 'SALIDA AGUA TORRE 1', 'ENTRADA AGUA A TORRE 2',
           'SALIDA AGUA TORRE 2', 'C_O_P MÁQUINA GRUPO FRÍO 1', 'C_O_P MÁQUINA GRUPO FRÍO 2', 'C_O_P BOMBA CALOR CARLOS',
           'C_O_P BOMBA CALOR FELIPE', 	 'TEMPERATURA SALIDA BOMBA CALOR CARLOS', 'TEMPERATURA SALIDA BOMBA CALOR FELIPE',
           'KILO CALORÍAS GENERADAS BOMBA CALOR CARLOS', 'KILO CALORÍAS GENERADAS BOMBA CALOR FELIPE',
           'KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1', 'KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2', 'VÁLVULA BY PASS SECUNDARIO FRÍO',
           'TEMPERATURA CONTROL DE BY PASS SECUNDARIO', 'SECUNDARIO FRÍO 1', 'SECUNDARIO FRÍO 2', 'SECUNDARIO FRÍO 3',
           'IMPULSIÓN SECUNDARIO CALOR', 'MODO INVIERNO BC1', 'MODO INVIERNO BC2', 'SECUNDARIO CALOR 1', 'SECUNDARIO CALOR 2',
           'SECUNDARIO CALOR 3' ]
diccionario = {'POTENCIA TRAFO 2': 1.48, 'POTENCIA TRAFO 3': 4.79, 'POTENCIA TRAFO 4': 269.04, 	'POTENCIA TRAFO 5': 393.82,
               'POTENCIA MEDIA CONECTADA': 715.97, 'PERIODO P6': 1, 'CONTROL FRÍO': 13.7, 'CONTROL CALOR': 0,
               'CAPACIDAD BOMBA CALOR FELIPE %': 0, 'CAPACIDAD BOMBA CALOR CARLOS %': 31.87, 'POTENCIA BOMBA CALOR FELIPE': 0.64,
               'POTENCIA BOMBA CALOR CARLOS': 49.47, 'TEMPERATURA AMBIENTE BOMBA CALOR CARLOS': 23.28,
               'TEMPERATURA AMBIENTE BOMBA CALOR FELIPE': 23.83, 'TEMPERATURA EXTERIOR': 0, 'CAPACIDAD GRUPO DE FRÍO 1': 1.33,
               'CAPACIDAD GRUPO DE FRÍO 2': 84, 'POTENCIA GRUPO FRÍO 1': 1.38, 'POTENCIA GRUPO FRÍO 2': 63.34,
               'ENTRADA AGUA A TORRE 1': 24.21, 'SALIDA AGUA TORRE 1': 23.99, 'ENTRADA AGUA A TORRE 2': 30.67,
               'SALIDA AGUA TORRE 2': 25.93, 'C_O_P MÁQUINA GRUPO FRÍO 1': 0.02, 'C_O_P MÁQUINA GRUPO FRÍO 2': 4.28,
               'C_O_P BOMBA CALOR CARLOS': 4.2, 'C_O_P BOMBA CALOR FELIPE': 0, 'TEMPERATURA SALIDA BOMBA CALOR CARLOS': 44.05,
               'TEMPERATURA SALIDA BOMBA CALOR FELIPE': 23.11, 'KILO CALORÍAS GENERADAS BOMBA CALOR CARLOS': 174156.64,
               'KILO CALORÍAS GENERADAS BOMBA CALOR FELIPE': 0, 'KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1': 10349.98,
               'KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2': 236150, 'VÁLVULA BY PASS SECUNDARIO FRÍO': 0,
               'TEMPERATURA CONTROL DE BY PASS SECUNDARIO': 0, 'SECUNDARIO FRÍO 1': 0, 'SECUNDARIO FRÍO 2': 0,
               'SECUNDARIO FRÍO 3': 0, 'IMPULSIÓN SECUNDARIO CALOR': 0, 'MODO INVIERNO BC1': 0, 'MODO INVIERNO BC2': 0,
               'SECUNDARIO CALOR 1': 0, 	 'SECUNDARIO CALOR 2': 0, 'SECUNDARIO CALOR 3': 0}
df = pd.DataFrame(columns=columns)
df = df.append(diccionario, ignore_index=True)
df["POTENCIA TERMICA BOMBA CALOR CARLOS"] = df["KILO CALORÍAS GENERADAS BOMBA CALOR CARLOS"] * 0.001163
df["POTENCIA TERMICA BOMBA CALOR FELIPE"] = df["KILO CALORÍAS GENERADAS BOMBA CALOR FELIPE"] * 0.001163
df["POTENCIA TERMICA GRUPO FRIO 1"] = df["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1"] * 0.001163
df["POTENCIA TERMICA GRUPO FRIO 2"] = df["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2"] * 0.001163

# Prediccion
@app.route('/api/train_frio_1', methods=['POST'])
def train_frio_1():
    cop_model = cop.COP()
    accuracy = cop_model.fit_grupo_frio_1()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict_frio_1', methods=['POST'])
def predict_frio_1():
    # get data to be predicted
    X = [[float(df['POTENCIA GRUPO FRÍO 1']), float(df['POTENCIA TERMICA GRUPO FRIO 1']),
          float(df['TEMPERATURA EXTERIOR'])]]
    cop_model = cop.COP()
    prediction_ = cop_model.predict_grupo_frio_1(X)
    prediction = float(prediction_[0])
    valorReal = float(df['C_O_P MÁQUINA GRUPO FRÍO 1'].iloc[0])
    print('COP frio 1 predicho:', prediction)
    print('COP frio 1 leido:', valorReal)
    # COP malo --> diagnostico
    if (((valorReal <= 3.5) or (valorReal >= 4.5)) and ((prediction <= 3.5) or (prediction >= 4.5))
            or (valorReal <= prediction - 0.5) or (valorReal >= prediction + 0.5)):
        kmeans_ = clustering.KMeans_()
        kmeans_prediction = kmeans_.predict_frio_1(X)
        print('Diagnostico frio 1:', kmeans_prediction)
    return jsonify({'registro': "todos las variables + el diagnostico"})

@app.route('/api/train_carlos', methods=['POST'])
def train_carlos():
    cop_model = cop.COP()
    accuracy = cop_model.fit_carlos()
    return jsonify({'accuracy': round(accuracy * 100, 2)})

@app.route('/api/predict_carlos', methods=['POST'])
def predict_carlos():
    # get data to be predicted
    X = [[float(df['POTENCIA BOMBA CALOR CARLOS']), float(df['POTENCIA TERMICA BOMBA CALOR CARLOS']),
          float(df['TEMPERATURA EXTERIOR']), float(df['TEMPERATURA SALIDA BOMBA CALOR CARLOS'])]]
    cop_model = cop.COP()
    prediction_ = cop_model.predict_carlos(X)
    prediction = float(prediction_[0])
    valorReal = float(df['C_O_P MÁQUINA GRUPO FRÍO 1'].iloc[0])
    print('COP carlos predicho:', prediction)
    print('COP carlos leido:', valorReal)
    # COP malo --> diagnostico
    if (((valorReal <= 3.5) or (valorReal >= 4.5)) and ((prediction <= 3.5) or (prediction >= 4.5))
            or (valorReal <= prediction - 0.5) or (valorReal >= prediction + 0.5)):
        kmeans_ = clustering.KMeans_()
        kmeans_prediction = kmeans_.predict_carlos(X)
        print('Diagnostico carlos:', kmeans_prediction)
    return jsonify({'registro': "todos las variables + el diagnostico"})

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

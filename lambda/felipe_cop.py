import joblib
import boto3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsRegressor
import s3fs
import os

key = os.environ['aws_key']
secret_key = os.environ['aws_secret_key']

s3 = boto3.client('s3',
                  aws_access_key_id=key,
                  aws_secret_access_key=secret_key,
                  region_name='us-east-2')
BUCKET_NAME = 'smart-building-integrador'

url = 'https://smart-building-integrador.s3.us-east-2.amazonaws.com/HVAC.csv'
dataFelipe_cop = pd.read_csv(url)

def predict_felipe_cop(kmeans, clusters):
        centroids = kmeans.cluster_centers_
        diagnostico = ''
        diagnosticos = []
        minPotenciaFelipe = 0.04
        maxPotenciaFelipe = 32
        minPotenciaTermicaFelipe = 0.25
        maxPotenciaTermicaFelipe = 114
        minTempExterior = 10
        maxTempExterior = 28
        minTempSalidaFelipe = 15
        maxTempSalidaFelipe = 42
        for cluster in clusters:
            if not ((centroids[cluster][0] > minPotenciaFelipe) and (centroids[cluster][0] <= maxPotenciaFelipe)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA BOMBA CALOR FELIPE.') 
            if not ((centroids[cluster][1] > minPotenciaTermicaFelipe) and (centroids[cluster][1] <= maxPotenciaTermicaFelipe)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TERMICA BOMBA CALOR FELIPE.')
            if not ((centroids[cluster][2] > minTempExterior) and (centroids[cluster][2] <= maxTempExterior)):
                diagnosticos.append('La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.')
            if not ((centroids[cluster][3] > minTempSalidaFelipe) and (centroids[cluster][3] <= maxTempSalidaFelipe)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la TEMPERATURA SALIDA BOMBA CALOR FELIPE.')
        if (len(diagnosticos) == 0):
            diagnostico = 'Máquina BOMBA CALOR FELIPE apagada o iniciando.'
        else:
            for i in range(len(diagnosticos) - 1):
                if (len(diagnosticos) == 1):
                    diagnostico = diagnosticos[0]
                else:
                    diagnostico += diagnosticos[i] + ' | '
                    diagnostico += diagnosticos[-1]
        return diagnostico

def lambda_handler(event, context):
    diccionario = []
    urlContadores = 'https://smart-building-integrador.s3.us-east-2.amazonaws.com/indices/indiceFelipe_COP.csv'
    data = pd.read_csv(urlContadores, sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    valorFelipe_cop = data['felipe_cop']
    
    s3.download_file(BUCKET_NAME, 'models/neigh_felipe.pkl', '/tmp/neigh_felipe.pkl')
    neigh = joblib.load('/tmp/neigh_felipe.pkl')
    s3.download_file(BUCKET_NAME, 'models/kmeans_felipe_cop.pkl', '/tmp/kmeans_felipe_cop.pkl')
    kmeans = joblib.load('/tmp/kmeans_felipe_cop.pkl')
    
    for i in range(int(valorFelipe_cop), int(valorFelipe_cop)+10):
        df = dataFelipe_cop.iloc[i]
        # get data to be predicted
        X = [[float(df['POTENCIA BOMBA CALOR FELIPE']), float(df['POTENCIA TERMICA BOMBA CALOR FELIPE']),
              float(df['TEMPERATURA EXTERIOR']), float(df['TEMPERATURA SALIDA BOMBA CALOR FELIPE'])]]
        prediction_ = neigh.predict(X)
        prediction = float(prediction_[0])
        valorReal = float(df['C_O_P BOMBA CALOR FELIPE'])
        # COP malo --> diagnostico (clustering)
        kmeans_prediction = ' '
        if (((valorReal <= 3.5) or (valorReal >= 4.5)) and ((prediction <= 3.5) or (prediction >= 4.5))
                or (valorReal <= prediction - 0.5) or (valorReal >= prediction + 0.5)):
            clusters = kmeans.predict(X)
            kmeans_prediction = predict_felipe_cop(kmeans, clusters)
        # Diccionario con todas las variables de un registro que se va retornar
        df.loc['C_O_P BOMBA CALOR FELIPE PREDICHO'] = prediction
        df.loc['Diagnostico'] = kmeans_prediction
        registro_dict = df.to_dict()
        diccionario.append(registro_dict)
    data['felipe_cop'] = valorFelipe_cop + 10
    bytes_to_write = data.to_csv(None, index=False).encode()
    fs = s3fs.S3FileSystem(key=key, secret=secret_key)
    with fs.open('s3://smart-building-integrador/indices/indiceFelipe_COP.csv', 'wb') as f:
        f.write(bytes_to_write)
    return(diccionario)
import json
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
dataFelipe_potencia = pd.read_csv(url)
valorToleranciaPotencia = 0.25

def predict_felipe_potencia(kmeans, clusters):
    centroids = kmeans.cluster_centers_
    diagnostico = ''
    diagnosticos = []
    minTempSalidaFelipe = 14 #mean - std
    maxTempSalidaFelipe = 42
    minPotenciaTermicaFelipe = 0
    maxPotenciaTermicaFelipe = 115
    minCOPFelipe = 0  #mean - std
    maxCOPFelipe = 4
    minPotTrafo4 = 0 
    maxPotTrafo4 = 318
    minPotTrafo5 = 0
    maxPotTrafo5 = 348
    minTempExterior = 4 #mean - std
    maxTempExterior = 27
    minTempAmbienteFelipe = 16 #mean - std
    maxTempAmbienteFelipe = 27
    for cluster in clusters:
        if not ((centroids[cluster][0] > minTempSalidaFelipe) and (centroids[cluster][0] <= maxTempSalidaFelipe)):
            diagnosticos.append('Revisar la anomalia derivada al valor de la TEMPERATURA SALIDA BOMBA CALOR FELIPE.')
        if not ((centroids[cluster][1] > minPotenciaTermicaFelipe) and (centroids[cluster][1] <= maxPotenciaTermicaFelipe)):
            diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TERMICA BOMBA CALOR FELIPE.')
        if not ((centroids[cluster][2] > minCOPFelipe) and (centroids[cluster][2] <= maxCOPFelipe)):
            diagnosticos.append('Revisar la anomalia derivada al valor de el C_O_P BOMBA CALOR FELIPE.')
        if not ((centroids[cluster][3] > minPotTrafo4) and (centroids[cluster][3] <= maxPotTrafo4)):
            diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TRAFO 4.')
        if not ((centroids[cluster][4] > minPotTrafo5) and (centroids[cluster][4] <= maxPotTrafo5)):
            diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TRAFO 5.')
        if not ((centroids[cluster][5] > minTempExterior) and (centroids[cluster][5] <= maxTempExterior)):
            diagnosticos.append('La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.')
        if not ((centroids[cluster][6] > minTempAmbienteFelipe) and (centroids[cluster][6] <= maxTempAmbienteFelipe)):
            diagnosticos.append('Revisar la anomalia derivada al valor de la TEMPERATURA AMBIENTE BOMBA CALOR FELIPE.')
    if (len(diagnosticos) == 0):
        diagnostico = 'Máquina BOMBA CALOR FELIPE apagada o iniciando.'
    elif (len(diagnosticos) == 1):
        diagnostico = diagnosticos[0]
    else:
        for i in range(1, len(diagnosticos) - 1):
            diagnostico += diagnosticos[i] + ' | '
        diagnostico += diagnosticos[-1]
    return diagnostico

def lambda_handler(event, context):
    diccionario = []
    urlContadores = 'https://smart-building-integrador.s3.us-east-2.amazonaws.com/indices/indexFelipe_potencia.csv'
    data = pd.read_csv(urlContadores, sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    valorFelipe_potencia = data['felipe_potencia']
    
    s3.download_file(BUCKET_NAME, 'models/rf_felipe.pkl', '/tmp/rf_felipe.pkl')
    regr = joblib.load('/tmp/rf_felipe.pkl')
    s3.download_file(BUCKET_NAME, 'models/kmeans_felipe_potencia.pkl', '/tmp/kmeans_felipe_potencia.pkl')
    kmeans = joblib.load('/tmp/kmeans_felipe_potencia.pkl')
    
    for i in range(0, 10):
        df = dataFelipe_potencia.iloc[i]
        # get data to be predicted
        X = [[float(df['TEMPERATURA SALIDA BOMBA CALOR FELIPE']), float(df['POTENCIA TERMICA BOMBA CALOR FELIPE']), float(df['C_O_P BOMBA CALOR FELIPE']),
                float(df['POTENCIA TRAFO 4']), float(df['POTENCIA TRAFO 5']), float(df['TEMPERATURA EXTERIOR']), float(df['TEMPERATURA AMBIENTE BOMBA CALOR FELIPE'])]]
        prediction_ = regr.predict(X)
        prediction = float(prediction_[0])
        valorReal = float(df['POTENCIA BOMBA CALOR FELIPE'])
        # Potencia mala --> diagnostico (clustering)
        kmeans_prediction = ' '
        tolerancia = valorReal * valorToleranciaPotencia
        if (prediction < (valorReal - tolerancia) or prediction > (valorReal + tolerancia)):
            clusters = kmeans.predict(X)
            kmeans_prediction = predict_felipe_potencia(kmeans, clusters)
        # Diccionario con todas las variables de un registro que se va retornar
        resultado = {'Diagnostico': kmeans_prediction, 'POTENCIA BOMBA CALOR FELIPE PREDICHA' : round(prediction, 3)}
        diccionario.append(resultado)
    data['felipe_potencia'] = valorFelipe_potencia + 10
    bytes_to_write = data.to_csv(None, index=False).encode()
    fs = s3fs.S3FileSystem(key=key, secret=secret_key)
    with fs.open('s3://smart-building-integrador/indices/indexFelipe_potencia.csv', 'wb') as f:
        f.write(bytes_to_write)
    return(diccionario)
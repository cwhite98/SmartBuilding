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
dataFrio2_potencia = pd.read_csv(url)
valorToleranciaPotencia = 0.25

def predict_frio_2_potencia(kmeans, clusters):
        centroids = kmeans.cluster_centers_
        diagnostico = ''
        diagnosticos = []
        minPotenciaTermicaFrio2 = 0
        maxPotenciaTermicaFrio2 = 98
        minEntradaAgua2 = 5 #mean - std
        maxEntradaAgua2 = 31
        minSalidaAgua2 = 5 #mean - std
        maxSalidaAgua2 = 29
        minPotTrafo4 = 0
        maxPotTrafo4 = 318
        minPotTrafo5 = 0
        maxPotTrafo5 = 348
        minPotMediaConectada = 459 #mean - std
        maxPotMediaConectada = 1075
        minControlFrio = 2 #mean - std
        maxControlFrio = 17
        minKigoFrigorias2 = 0
        maxKigoFrigorias2 = 84085
        minTempExterior = 4 #mean - std
        maxTempExterior = 27
        for cluster in clusters:
            if not ((centroids[cluster][0] > minPotenciaTermicaFrio2) and (centroids[cluster][0] <= maxPotenciaTermicaFrio2)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TERMICA GRUPO FRIO 2.') 
            if not ((centroids[cluster][1] > minEntradaAgua2) and (centroids[cluster][1] <= maxEntradaAgua2)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la ENTRADA AGUA A TORRE 2.') 
            if not ((centroids[cluster][2] > minSalidaAgua2) and (centroids[cluster][2] <= maxSalidaAgua2)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la SALIDA AGUA TORRE 2.')
            if not ((centroids[cluster][3] > minPotTrafo4) and (centroids[cluster][3] <= maxPotTrafo4)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TRAFO 4.')
            if not ((centroids[cluster][4] > minPotTrafo5) and (centroids[cluster][4] <= maxPotTrafo5)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TRAFO 5.')
            if not ((centroids[cluster][5] > minPotMediaConectada) and (centroids[cluster][5] <= maxPotMediaConectada)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA MEDIA CONECTADA.')
            if not ((centroids[cluster][6] > minControlFrio) and (centroids[cluster][6] <= maxControlFrio)):
                diagnosticos.append('Revisar la anomalia derivada al valor de el CONTROL FRÍO.')
            if not ((centroids[cluster][7] > minKigoFrigorias2) and (centroids[cluster][7] <= maxKigoFrigorias2)):
                diagnosticos.append('Revisar la anomalia derivada al valor de las KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2.')
            if not ((centroids[cluster][8] > minTempExterior) and (centroids[cluster][8] <= maxTempExterior)):
                diagnosticos.append('La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.')
        if (len(diagnosticos) == 0):
            diagnostico = 'Máquina GRUPO FRÍO 2 apagada o iniciando.'
        elif (len(diagnosticos) == 1):
            diagnostico = diagnosticos[0]
        else:
            for i in range(1, len(diagnosticos) - 1):
                diagnostico += diagnosticos[i] + ' | '
            diagnostico += diagnosticos[-1]
        return diagnostico

def lambda_handler(event, context):
    diccionario = []
    urlContadores = 'https://smart-building-integrador.s3.us-east-2.amazonaws.com/indices/indexFrio2_potencia.csv'
    data = pd.read_csv(urlContadores, sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    valorFrio2_potencia = data['grupo_frio2_potencia']
    
    s3.download_file(BUCKET_NAME, 'models/rf_frio_1.pkl', '/tmp/rf_frio_1.pkl')
    regr = joblib.load('/tmp/rf_frio_1.pkl')
    s3.download_file(BUCKET_NAME, 'models/kmeans_frio_2_potencia.pkl', '/tmp/kmeans_frio_2_potencia.pkl')
    kmeans = joblib.load('/tmp/kmeans_frio_2_potencia.pkl')
    
    for i in range(int(valorFrio2_potencia), int(valorFrio2_potencia)+10):
        df = dataFrio2_potencia.iloc[i]
        # get data to be predicted
        X = [[float(df['POTENCIA TERMICA GRUPO FRIO 2']), float(df['ENTRADA AGUA A TORRE 2']), float(df['SALIDA AGUA TORRE 2']),
                float(df['POTENCIA TRAFO 4']), float(df['POTENCIA TRAFO 5']), float(df['POTENCIA MEDIA CONECTADA']), float(df['CONTROL FRÍO']),
                float(df['KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2']), float(df['TEMPERATURA EXTERIOR'])]]
        prediction_ = regr.predict(X)
        prediction = float(prediction_[0])
        valorReal = float(df['POTENCIA GRUPO FRÍO 2'])
        # Potencia mala --> diagnostico (clustering)
        kmeans_prediction = ' '
        tolerancia = valorReal * valorToleranciaPotencia
        if (prediction < (valorReal - tolerancia) or prediction > (valorReal + tolerancia)):
            clusters = kmeans.predict(X)
            kmeans_prediction = predict_frio_2_potencia(kmeans, clusters)
        # Diccionario con todas las variables de un registro que se va retornar
        resultado = {'Diagnostico': kmeans_prediction, 'POTENCIA GRUPO FRÍO 2 PREDICHA' : round(prediction, 3)}
        diccionario.append(resultado)
    data['grupo_frio2_potencia'] = valorFrio2_potencia + 10
    bytes_to_write = data.to_csv(None, index=False).encode()
    fs = s3fs.S3FileSystem(key=key, secret=secret_key)
    with fs.open('s3://smart-building-integrador/indices/indexFrio2_potencia.csv', 'wb') as f:
        f.write(bytes_to_write)
    return (diccionario)

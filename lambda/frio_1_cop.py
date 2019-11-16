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
dataFrio1_cop = pd.read_csv(url)
    
def predict_frio_1_cop(kmeans, clusters):
    centroids = kmeans.cluster_centers_
    diagnostico = ''
    diagnosticos = []
    minPotenciaFrio1 = 0
    maxPotenciaFrio1 = 20
    minPotenciaTermicaFrio1 = 0
    maxPotenciaTermicaFrio1 = 129
    minTempExterior = 10
    maxTempExterior = 27
    for cluster in clusters:
        if not ((centroids[cluster][0] > minPotenciaFrio1) and (centroids[cluster][0] <= maxPotenciaFrio1)):
            diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA GRUPO FRÍO 1.') 
        if not ((centroids[cluster][1] > minPotenciaTermicaFrio1) and (centroids[cluster][1] <= maxPotenciaTermicaFrio1)):
            diagnosticos.append('Revisar la anomalia derivado al valor de la POTENCIA TERMICA GRUPO FRIO 1.')
        if not ((centroids[cluster][2] > minTempExterior) and (centroids[cluster][2] <= maxTempExterior)):
            diagnosticos.append('La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.')
    if (len(diagnosticos) == 0):
        diagnostico = 'Máquina GRUPO FRÍO 1 apagada o iniciando.'
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
    urlContadores = 'https://smart-building-integrador.s3.us-east-2.amazonaws.com/indices/indexFrio1_COP.csv'
    data = pd.read_csv(urlContadores, sep='\s*,\s*', header=0, encoding='ascii', engine='python')
    valorDataFrio1_cop = data['grupo_frio1_cop']
    
    #Cargar los modelos
    s3.download_file(BUCKET_NAME, 'models/neigh_frio_1.pkl', '/tmp/neigh_frio_1.pkl')
    neigh = joblib.load('/tmp/neigh_frio_1.pkl')
    s3.download_file(BUCKET_NAME, 'models/kmeans_frio_1_cop.pkl', '/tmp/kmeans_frio_1_cop.pkl')
    kmeans = joblib.load('/tmp/kmeans_frio_1_cop.pkl')
    
    for i in range(int(valorDataFrio1_cop), int(valorDataFrio1_cop+10)):
        df = dataFrio1_cop.iloc[i]
        # get data to be predicted
        X = [[float(df['POTENCIA GRUPO FRÍO 1']), float(df['POTENCIA TERMICA GRUPO FRIO 1']),
              float(df['TEMPERATURA EXTERIOR'])]]
        prediction_ = neigh.predict(X)
        prediction = float(prediction_[0])
        valorReal = float(df['C_O_P MÁQUINA GRUPO FRÍO 1'])
        # COP malo --> diagnostico (clustering)
        kmeans_prediction = ' '
        if (((valorReal <= 3.5) or (valorReal >= 4.5)) and ((prediction <= 3.5) or (prediction >= 4.5))
                or (valorReal <= prediction - 0.5) or (valorReal >= prediction + 0.5)):
            clusters = kmeans.predict(X)
            kmeans_prediction = predict_frio_1_cop(kmeans, clusters)
        # Diccionario con todas las variables de un registro que se va retornar
        df.loc['C_O_P MÁQUINA GRUPO FRÍO 1 PREDICHO'] = prediction
        df.loc['Diagnostico'] = kmeans_prediction
        df2 = df.drop(labels=['Diagnostico', 'Fecha- hora de lectura'])
        df2 = df2.apply(lambda x: round(float(x), 3))
        dfAux = df[['Diagnostico', 'Fecha- hora de lectura']]
        dfR = pd.concat([df2, dfAux], axis=0, sort=False)
        registro_dict = dfR.to_dict()
        diccionario.append(registro_dict)
    data['grupo_frio1_cop'] = valorDataFrio1_cop + 10
    bytes_to_write = data.to_csv(None, index=False).encode()
    fs = s3fs.S3FileSystem(key=key, secret=secret_key)
    with fs.open('s3://smart-building-integrador/indices/indexFrio1_COP.csv', 'wb') as f:
        f.write(bytes_to_write)
    return diccionario
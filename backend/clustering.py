from sklearn.cluster import KMeans
import joblib
import dataset
import boto3

s3 = boto3.client('s3',
                  aws_access_key_id='*******',
                  aws_secret_access_key='*******',
                  region_name='us-east-2')
BUCKET_NAME = 'smart-building-integrador'


class KMeans_:

    # Clustering COP
    def kmeans_frio_1_cop(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataFrio1 = data[['POTENCIA GRUPO FRÍO 1', 'POTENCIA TERMICA GRUPO FRIO 1', 'TEMPERATURA EXTERIOR']]
        kmeans = KMeans(4)
        kmeans.fit(dataFrio1)
        joblib.dump(kmeans, 'kmeans_frio_1_cop.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_frio_1_cop(self, X):
        s3.download_file(BUCKET_NAME, 'models/kmeans_frio_1_cop.pkl', '/tmp/kmeans_frio_1_cop.pkl')
        kmeans = joblib.load('/tmp/kmeans_frio_1_cop.pkl')
        clusters = kmeans.predict(X)
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
            diagnostico = 'COP malo por razón no definida.'
        else:
            for i in range(len(diagnosticos) - 1):
                if (len(diagnosticos) == 1):
                    diagnostico = diagnosticos[0]
                else:
                    diagnostico += diagnosticos[i] + ' | '
                    diagnostico += diagnosticos[-1]
        return diagnostico

    def kmeans_frio_2_cop(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataFrio2 = data[['POTENCIA GRUPO FRÍO 2', 'POTENCIA TERMICA GRUPO FRIO 2', 'TEMPERATURA EXTERIOR']]
        kmeans = KMeans(4)
        kmeans.fit(dataFrio2)
        joblib.dump(kmeans, 'kmeans_frio_2_cop.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_frio_2_cop(self, X):
        s3.download_file(BUCKET_NAME, 'models/kmeans_frio_2_cop.pkl', '/tmp/kmeans_frio_2_cop.pkl')
        kmeans = joblib.load('/tmp/kmeans_frio_2_cop.pkl')
        clusters = kmeans.predict(X)
        centroids = kmeans.cluster_centers_
        diagnostico = ''
        diagnosticos = []
        minPotenciaFrio2 = 0
        maxPotenciaFrio2 = 27
        minPotenciaTermicaFrio2 = 0
        maxPotenciaTermicaFrio2 = 97
        minTempExterior = 10.102595
        maxTempExterior = 27.313549000000002
        for cluster in clusters:
            if not ((centroids[cluster][0] > minPotenciaFrio2) and (centroids[cluster][0] <= maxPotenciaFrio2)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA GRUPO FRÍO 2.') 
            if not ((centroids[cluster][1] > minPotenciaTermicaFrio2) and (centroids[cluster][1] <= maxPotenciaTermicaFrio2)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TERMICA GRUPO FRIO 2.')
            if not ((centroids[cluster][2] > minTempExterior) and (centroids[cluster][2] <= maxTempExterior)):
                diagnosticos.append('La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.')
        if (len(diagnosticos) == 0):
            diagnostico = 'COP malo por razón no definida.'
        else:
            for i in range(len(diagnosticos) - 1):
                if (len(diagnosticos) == 1):
                    diagnostico = diagnosticos[0]
                else:
                    diagnostico += diagnosticos[i] + ' | '
                    diagnostico += diagnosticos[-1]
        return diagnostico

    def kmeans_carlos_cop(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataCarlos = data[['POTENCIA BOMBA CALOR CARLOS', 'POTENCIA TERMICA BOMBA CALOR CARLOS',
                           'TEMPERATURA EXTERIOR', 'TEMPERATURA SALIDA BOMBA CALOR CARLOS']]
        kmeans = KMeans(4)
        kmeans.fit(dataCarlos)
        joblib.dump(kmeans, 'kmeans_carlos_cop.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_carlos_cop(self, X):
        s3.download_file(BUCKET_NAME, 'models/kmeans_carlos_cop.pkl', '/tmp/kmeans_carlos_cop.pkl')
        kmeans = joblib.load('/tmp/kmeans_carlos_cop.pkl')
        clusters = kmeans.predict(X)
        centroids = kmeans.cluster_centers_
        diagnostico = ''
        diagnosticos = []
        minPotenciaCarlos = 0.02
        maxPotenciaCarlos = 34
        minPotenciaTermicaCarlos = 0.2
        maxPotenciaTermicaCarlos = 134
        minTempExterior = 10
        maxTempExterior = 28
        minTempSalidaCarlos = 17
        maxTempSalidaCarlos = 43
        for cluster in clusters:
            if not ((centroids[cluster][0] > minPotenciaCarlos) and (centroids[cluster][0] <= maxPotenciaCarlos)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA BOMBA CALOR CARLOS.') 
            if not ((centroids[cluster][1] > minPotenciaTermicaCarlos) and (centroids[cluster][1] <= maxPotenciaTermicaCarlos)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TERMICA BOMBA CALOR CARLOS.')
            if not ((centroids[cluster][2] > minTempExterior) and (centroids[cluster][2] <= maxTempExterior)):
                diagnosticos.append('La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.')
            if not ((centroids[cluster][3] > minTempSalidaCarlos) and (centroids[cluster][3] <= maxTempSalidaCarlos)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la TEMPERATURA SALIDA BOMBA CALOR CARLOS.')
        if (len(diagnosticos) == 0):
            diagnostico = 'COP malo por razón no definida.'
        else:
            for i in range(len(diagnosticos) - 1):
                if (len(diagnosticos) == 1):
                    diagnostico = diagnosticos[0]
                else:
                    diagnostico += diagnosticos[i] + ' | '
                    diagnostico += diagnosticos[-1]
        return diagnostico

    def kmeans_felipe_cop(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataFelipe = data[['POTENCIA BOMBA CALOR FELIPE', 'POTENCIA TERMICA BOMBA CALOR FELIPE', 'TEMPERATURA EXTERIOR',
                            'TEMPERATURA SALIDA BOMBA CALOR FELIPE']]
        kmeans = KMeans(4)
        kmeans.fit(dataFelipe)
        joblib.dump(kmeans, 'kmeans_felipe_cop.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_felipe_cop(self, X):
        s3.download_file(BUCKET_NAME, 'models/kmeans_felipe_cop.pkl', '/tmp/kmeans_felipe_cop.pkl')
        kmeans = joblib.load('/tmp/kmeans_felipe_cop.pkl')
        clusters = kmeans.predict(X)
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
            diagnostico = 'COP malo por razón no definida.'
        else:
            for i in range(len(diagnosticos) - 1):
                if (len(diagnosticos) == 1):
                    diagnostico = diagnosticos[0]
                else:
                    diagnostico += diagnosticos[i] + ' | '
                    diagnostico += diagnosticos[-1]
        return diagnostico

    # Clustering Potencia
    def kmeans_frio_1_potencia(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataFrio1 = data[['POTENCIA TERMICA GRUPO FRIO 1', 'ENTRADA AGUA A TORRE 1', 'SALIDA AGUA TORRE 1',
                   'POTENCIA TRAFO 4', 'POTENCIA TRAFO 5', 'POTENCIA MEDIA CONECTADA', 'CONTROL FRÍO',
                   'KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1', 'TEMPERATURA EXTERIOR']]
        kmeans = KMeans(3)
        kmeans.fit(dataFrio1)
        joblib.dump(kmeans, 'kmeans_frio_1_potencia.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_frio_1_potencia(self, X):
        s3.download_file(BUCKET_NAME, 'models/kmeans_frio_1_potencia.pkl', '/tmp/kmeans_frio_1_potencia.pkl')
        kmeans = joblib.load('/tmp/kmeans_frio_1_potencia.pkl')
        clusters = kmeans.predict(X)
        centroids = kmeans.cluster_centers_
        diagnostico = ''
        diagnosticos = []
        minPotenciaTermicaFrio1 = 0
        maxPotenciaTermicaFrio1 = 96
        minEntradaAgua1 = 5 #mean - std
        maxEntradaAgua1 = 30
        minSalidaAgua1 = 4 #mean - std
        maxSalidaAgua1 = 28
        minPotTrafo4 = 0
        maxPotTrafo4 = 318
        minPotTrafo5 = 0
        maxPotTrafo5 = 348
        minPotMediaConectada = 459 #mean - std
        maxPotMediaConectada = 1075
        minControlFrio = 2 #mean - std
        maxControlFrio = 17
        minKigoFrigorias1 = 0
        maxKigoFrigorias1 = 83000
        minTempExterior = 4 #mean - std
        maxTempExterior = 27
        for cluster in clusters:
            if not ((centroids[cluster][0] > minPotenciaTermicaFrio1) and (centroids[cluster][0] <= maxPotenciaTermicaFrio1)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TERMICA GRUPO FRIO 1.') 
            if not ((centroids[cluster][1] > minEntradaAgua1) and (centroids[cluster][1] <= maxEntradaAgua1)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la ENTRADA AGUA A TORRE 1.') 
            if not ((centroids[cluster][2] > minSalidaAgua1) and (centroids[cluster][2] <= maxSalidaAgua1)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la SALIDA AGUA TORRE 1.')
            if not ((centroids[cluster][3] > minPotTrafo4) and (centroids[cluster][3] <= maxPotTrafo4)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TRAFO 4.')
            if not ((centroids[cluster][4] > minPotTrafo5) and (centroids[cluster][4] <= maxPotTrafo5)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TRAFO 5.')
            if not ((centroids[cluster][5] > minPotMediaConectada) and (centroids[cluster][5] <= maxPotMediaConectada)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA MEDIA CONECTADA.')
            if not ((centroids[cluster][6] > minControlFrio) and (centroids[cluster][6] <= maxControlFrio)):
                diagnosticos.append('Revisar la anomalia derivada al valor de el CONTROL FRÍO.')
            if not ((centroids[cluster][7] > minKigoFrigorias1) and (centroids[cluster][7] <= maxKigoFrigorias1)):
                diagnosticos.append('Revisar la anomalia derivada al valor de las KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1.')
            if not ((centroids[cluster][8] > minTempExterior) and (centroids[cluster][8] <= maxTempExterior)):
                diagnosticos.append('La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.')
        if (len(diagnosticos) == 0):
            diagnostico = 'Potencia mala por razón no definida.'
        elif (len(diagnosticos) == 1):
            diagnostico = diagnosticos[0]
        else:
            for i in range(1, len(diagnosticos) - 1):
                diagnostico += diagnosticos[i] + ' | '
            diagnostico += diagnosticos[-1]
        return diagnostico

    def kmeans_frio_2_potencia(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataFrio2 = data[['POTENCIA TERMICA GRUPO FRIO 2', 'ENTRADA AGUA A TORRE 2', 'SALIDA AGUA TORRE 2',
                   'POTENCIA TRAFO 4', 'POTENCIA TRAFO 5', 'POTENCIA MEDIA CONECTADA', 'CONTROL FRÍO',
                   'KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2', 'TEMPERATURA EXTERIOR']]
        kmeans = KMeans(3)
        kmeans.fit(dataFrio2)
        joblib.dump(kmeans, 'kmeans_frio_2_potencia.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_frio_2_potencia(self, X):
        s3.download_file(BUCKET_NAME, 'models/kmeans_frio_2_potencia.pkl', '/tmp/kmeans_frio_2_potencia.pkl')
        kmeans = joblib.load('/tmp/kmeans_frio_2_potencia.pkl')
        clusters = kmeans.predict(X)
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
            diagnostico = 'Potencia mala por razón no definida.'
        elif (len(diagnosticos) == 1):
            diagnostico = diagnosticos[0]
        else:
            for i in range(1, len(diagnosticos) - 1):
                diagnostico += diagnosticos[i] + ' | '
            diagnostico += diagnosticos[-1]
        return diagnostico

    def kmeans_carlos_potencia(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataCarlos = data[['TEMPERATURA SALIDA BOMBA CALOR CARLOS','POTENCIA TERMICA BOMBA CALOR CARLOS', 
                    'C_O_P BOMBA CALOR CARLOS', 'POTENCIA TRAFO 4', 'POTENCIA TRAFO 5',
                    'TEMPERATURA EXTERIOR', 'TEMPERATURA AMBIENTE BOMBA CALOR CARLOS']]
        kmeans = KMeans(3)
        kmeans.fit(dataCarlos)
        joblib.dump(kmeans, 'kmeans_carlos_potencia.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_carlos_potencia(self, X):
        s3.download_file(BUCKET_NAME, 'models/kmeans_carlos_potencia.pkl', '/tmp/kmeans_carlos_potencia.pkl')
        kmeans = joblib.load('/tmp/kmeans_carlos_potencia.pkl')
        clusters = kmeans.predict(X)
        centroids = kmeans.cluster_centers_
        diagnostico = ''
        diagnosticos = []
        minTempSalidaCarlos = 16.441466 #mean - std
        maxTempSalidaCarlos = 43.095148
        minPotenciaTermicaCarlos = 0 
        maxPotenciaTermicaCarlos = 132
        minCOPCarlos = 3.2656959999999997  #mean - std
        maxCOPCarlos = 4.0215179999999995
        minPotTrafo4 = 0 
        maxPotTrafo4 = 318
        minPotTrafo5 = 0
        maxPotTrafo5 = 348
        minTempExterior = 10
        maxTempExterior = 28
        minTempAmbienteCarlos = 3.73738 #mean - std
        maxTempAmbienteCarlos = 26.429133999999998
        for cluster in clusters:
            if not ((centroids[cluster][0] > minTempSalidaCarlos) and (centroids[cluster][0] <= maxTempSalidaCarlos)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la TEMPERATURA SALIDA BOMBA CALOR CARLOS.')
            if not ((centroids[cluster][1] > minPotenciaTermicaCarlos) and (centroids[cluster][1] <= maxPotenciaTermicaCarlos)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TERMICA BOMBA CALOR CARLOS.')
            if not ((centroids[cluster][2] > minCOPCarlos) and (centroids[cluster][2] <= maxCOPCarlos)):
                diagnosticos.append('Revisar la anomalia derivada al valor de el C_O_P BOMBA CALOR CARLOS.')
            if not ((centroids[cluster][3] > minPotTrafo4) and (centroids[cluster][3] <= maxPotTrafo4)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TRAFO 4.')
            if not ((centroids[cluster][4] > minPotTrafo5) and (centroids[cluster][4] <= maxPotTrafo5)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la POTENCIA TRAFO 5.')
            if not ((centroids[cluster][5] > minTempExterior) and (centroids[cluster][5] <= maxTempExterior)):
                diagnosticos.append('La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.')
            if not ((centroids[cluster][6] > minTempAmbienteCarlos) and (centroids[cluster][6] <= maxTempAmbienteCarlos)):
                diagnosticos.append('Revisar la anomalia derivada al valor de la TEMPERATURA AMBIENTE BOMBA CALOR CARLOS.')
        if (len(diagnosticos) == 0):
            diagnostico = 'Potencia mala por razón no definida.'
        elif (len(diagnosticos) == 1):
            diagnostico = diagnosticos[0]
        else:
            for i in range(1, len(diagnosticos) - 1):
                diagnostico += diagnosticos[i] + ' | '
            diagnostico += diagnosticos[-1]
        return diagnostico

    def kmeans_felipe_potencia(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataFelipe = data[['TEMPERATURA SALIDA BOMBA CALOR FELIPE','POTENCIA TERMICA BOMBA CALOR FELIPE', 
                    'C_O_P BOMBA CALOR FELIPE', 'POTENCIA TRAFO 4','POTENCIA TRAFO 5',
                    'TEMPERATURA EXTERIOR', 'TEMPERATURA AMBIENTE BOMBA CALOR FELIPE']]
        kmeans = KMeans(3)
        kmeans.fit(dataFelipe)
        joblib.dump(kmeans, 'kmeans_felipe_potencia.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_felipe_potencia(self, X):
        s3.download_file(BUCKET_NAME, 'models/kmeans_felipe_potencia.pkl', '/tmp/kmeans_felipe_potencia.pkl')
        kmeans = joblib.load('/tmp/kmeans_felipe_potencia.pkl')
        clusters = kmeans.predict(X)
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
            diagnostico = 'Potencia mala por razón no definida.'
        elif (len(diagnosticos) == 1):
            diagnostico = diagnosticos[0]
        else:
            for i in range(1, len(diagnosticos) - 1):
                diagnostico += diagnosticos[i] + ' | '
            diagnostico += diagnosticos[-1]
        return diagnostico

from sklearn.cluster import KMeans
from sklearn.externals import joblib
import dataset


class KMeans_:

    def kmeans_frio_1(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataFrio1 = data[['POTENCIA GRUPO FRÍO 1', 'POTENCIA TERMICA GRUPO FRIO 1', 'TEMPERATURA EXTERIOR']]
        kmeans = KMeans(4)
        kmeans.fit(dataFrio1)
        joblib.dump(kmeans, 'kmeans_frio_1.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_frio_1(self, X):
        kmeans = joblib.load('kmeans_frio_1.pkl')
        clusters = kmeans.predict(X)
        centroids = kmeans.cluster_centers_
        diagnostico = 'COP malo, pero no sabemos la razon'
        for cluster in clusters:
            minPotenciaFrio1 = 0
            maxPotenciaFrio1 = 20
            minPotenciaTermicaFrio1 = 0
            maxPotenciaTermicaFrio1 = 129
            minTempExterior = 10
            maxTempExterior = 27
            if ((centroids[cluster][0] < minPotenciaFrio1) and (centroids[cluster][0] >= maxPotenciaFrio1)):
                diagnostico = 'Revisar la POTENCIA GRUPO FRÍO 1.'
            if ((centroids[cluster][1] < minPotenciaTermicaFrio1) and (centroids[cluster][1] >= maxPotenciaTermicaFrio1)):
                diagnostico = 'Revisar la POTENCIA TERMICA GRUPO FRIO 1.'
            if ((centroids[cluster][2] < minTempExterior) and (centroids[cluster][2] >= maxTempExterior)):
                diagnostico = 'La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.'
        return diagnostico

    def kmeans_frio_2(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataFrio2 = data[['POTENCIA GRUPO FRÍO 2', 'POTENCIA TERMICA GRUPO FRIO 2', 'TEMPERATURA EXTERIOR']]
        kmeans = KMeans(4)
        kmeans.fit(dataFrio2)
        joblib.dump(kmeans, 'kmeans_frio_2.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_frio_2(self, X):
        kmeans = joblib.load('kmeans_frio_2.pkl')
        clusters = kmeans.predict(X)
        centroids = kmeans.cluster_centers_
        diagnostico = 'COP malo, pero no sabemos la razon'
        for cluster in clusters:
            minPotenciaFrio2 = 0
            maxPotenciaFrio2 = 27
            minPotenciaTermicaFrio2 = 0
            maxPotenciaTermicaFrio2 = 97
            minTempExterior = 10.102595
            maxTempExterior = 27.313549000000002
            if ((centroids[cluster][0] < minPotenciaFrio2) and (centroids[cluster][0] >= maxPotenciaFrio2)):
                diagnostico = 'Revisar la POTENCIA GRUPO FRÍO 2.'
            if ((centroids[cluster][1] < minPotenciaTermicaFrio2) and (centroids[cluster][1] >= maxPotenciaTermicaFrio2)):
                diagnostico = 'Revisar la POTENCIA TERMICA GRUPO FRIO 2.'
            if ((centroids[cluster][2] < minTempExterior) and (centroids[cluster][2] >= maxTempExterior)):
                diagnostico = 'La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.'
        return diagnostico

    def kmeans_carlos(self):
        obj = dataset.Dataset()
        data = obj.read_dataset()
        dataCarlos = data[['POTENCIA BOMBA CALOR CARLOS', 'POTENCIA TERMICA BOMBA CALOR CARLOS',
                           'TEMPERATURA EXTERIOR', 'TEMPERATURA SALIDA BOMBA CALOR CARLOS']]
        kmeans = KMeans(4)
        kmeans.fit(dataCarlos)
        joblib.dump(kmeans, 'kmeans_carlos.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_carlos(self, X):
        kmeans = joblib.load('kmeans_carlos.pkl')
        clusters = kmeans.predict(X)
        centroids = kmeans.cluster_centers_
        diagnostico = 'COP malo, pero no sabemos la razon'
        for cluster in clusters:
            minPotenciaCarlos = 0.02
            maxPotenciaCarlos = 34
            minPotenciaTermicaCarlos = 0.2
            maxPotenciaTermicaCarlos = 134
            minTempExterior = 10
            maxTempExterior = 28
            minTempSalidaCarlos = 17
            maxTempSalidaCarlos = 43
            if not ((centroids[cluster][0] > minPotenciaCarlos) and (centroids[cluster][0] <= maxPotenciaCarlos)):
                diagnostico = 'Revisar la POTENCIA BOMBA CALOR CARLOS.'
            if not ((centroids[cluster][1] > minPotenciaTermicaCarlos) and (centroids[cluster][1] <= maxPotenciaTermicaCarlos)):
                diagnostico = 'Revisar la POTENCIA TERMICA BOMBA CALOR CARLOS.'
            if not ((centroids[cluster][2] > minTempExterior) and (centroids[cluster][2] <= maxTempExterior)):
                diagnostico = 'La TEMPERATURA EXTERIOR esta generando una anomalia en el climatizador.'
            if not ((centroids[cluster][3] > minTempSalidaCarlos) and (centroids[cluster][3] <= maxTempSalidaCarlos)):
                diagnostico = 'Revisar la anomalia derivado al valor de la TEMPERATURA SALIDA BOMBA CALOR CARLOS que es X'
        return diagnostico

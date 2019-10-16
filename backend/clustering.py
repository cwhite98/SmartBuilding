import pandas as pd
from sklearn.cluster import KMeans
from sklearn.externals import joblib


class KMeans_:

    def dataset(self):
        data = pd.read_excel("../Datasets/HVAC.xlsx", "HISTORICO_DATOS", index_col=0)
        variables_a_eliminar = ["C_O_P_ BOMBA CALOR FELIPE", "C_O_P_ BOMBA CALOR CARLOS",
                                "C_O_P_ INSTALACIÓN GRUPO FRÍO 1", "C_O_P_ INSTALACÍON GRUPO FRÍO 2",
                                "ORDEN", "VÁLVULA BY PASS SECUNDARIO FRÍO",
                                "TEMPERATURA CONTROL DE BY PASS SECUNDARIO", "SECUNDARIO FRÍO 1",
                                "SECUNDARIO FRÍO 2", "SECUNDARIO FRÍO 3", "MODO INVIERNO BC1",
                                "MODO INVIERNO BC2", "PERIODO P6", "CONTROL CALOR",
                                "CAPACIDAD BOMBA CALOR FELIPE %", "CAPACIDAD BOMBA CALOR CARLOS %",
                                "CAPACIDAD GRUPO DE FRÍO 1", " CAPACIDAD GRUPO DE FRÍO 2",
                                "IMPULSIÓN SECUNDARIO CALOR", "SECUNDARIO CALOR 1",
                                "SECUNDARIO CALOR 2", "SECUNDARIO CALOR 3",
                                "Fecha- hora de lectura"]
        lista_variables = data.columns.values.tolist()
        subLista = [x for x in lista_variables if x not in variables_a_eliminar]
        data[subLista]
        data["POTENCIA TERMICA BOMBA CALOR CARLOS"] = data["KILO CALORÍAS GENERADAS BOMBA CALOR CARLOS"] * 0.001163
        data["POTENCIA TERMICA BOMBA CALOR FELIPE"] = data["KILO CALORÍAS GENERADAS BOMBA CALOR FELIPE"] * 0.001163
        data["POTENCIA TERMICA GRUPO FRIO 1"] = data["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1"] * 0.001163
        data["POTENCIA TERMICA GRUPO FRIO 2"] = data["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2"] * 0.001163
        return data

    def kmeans_carlos(self):
        obj = KMeans_()
        data = obj.dataset()
        dataCarlos = data[['POTENCIA BOMBA CALOR CARLOS', 'POTENCIA TERMICA BOMBA CALOR CARLOS',
                           'TEMPERATURA EXTERIOR', 'TEMPERATURA SALIDA BOMBA CALOR CARLOS']]
        kmeans = KMeans(4)
        kmeans.fit(dataCarlos)
        joblib.dump(kmeans, 'kmeans_carlos.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_carlos(self, X):
        kmeans = joblib.load('kmeans_carlos.pkl')
        predicts = kmeans.predict(X)
        return predicts

    def kmeans_frio_1(self):
        obj = KMeans_()
        data = obj.dataset()
        dataFrio1 = data[['POTENCIA GRUPO FRÍO 1', 'POTENCIA TERMICA GRUPO FRIO 1', 'TEMPERATURA EXTERIOR']]
        kmeans = KMeans(4)
        kmeans.fit(dataFrio1)
        joblib.dump(kmeans, 'kmeans_frio_1.pkl')
        centroids = kmeans.cluster_centers_
        return str(centroids)

    def predict_frio_1(self, X):
        kmeans = joblib.load('kmeans_frio_1.pkl')
        predicts = kmeans.predict(X)
        return predicts
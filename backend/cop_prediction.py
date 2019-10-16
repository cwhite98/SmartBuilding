import pandas as pd
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

class COP:
        
    def fit_grupo_frio_1(self):
        data = pd.read_excel("../Datasets/HVAC_limpio.xlsx", "HVAC_limpio", index_col=0)
        data['Fecha- hora de lectura'] = (data['Fecha- hora de lectura'] - data['Fecha- hora de lectura'].min())  / np.timedelta64(1,'D')
        X = data[['POTENCIA GRUPO FRÍO 1', 'POTENCIA TERMICA GRUPO FRIO 1', 'TEMPERATURA EXTERIOR']]
        y = data['C_O_P MÁQUINA GRUPO FRÍO 1']
        neigh = KNeighborsRegressor(n_neighbors=15)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        neigh.fit(X_train, y_train) 
        # persist model
        joblib.dump(neigh, 'neigh.pkl')
        acc = neigh.score(X_test, y_test)
        return acc
    
    def predict_grupo_frio_1(self, X):
        neigh = joblib.load('neigh.pkl')
        predicts = neigh.predict(X)
        return predicts
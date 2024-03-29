import dataset
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

class Potencia:

    def fit_grupo_frio_1(self):
        obj = dataset.Dataset()
        data = obj.read_dataset_limpio()
        X = data[['POTENCIA TERMICA GRUPO FRIO 1', 'ENTRADA AGUA A TORRE 1', 'SALIDA AGUA TORRE 1',
                'POTENCIA TRAFO 4', 'POTENCIA TRAFO 5', 'POTENCIA MEDIA CONECTADA', 'CONTROL FRÍO',
                'KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1', 'TEMPERATURA EXTERIOR']]
        y = data['POTENCIA GRUPO FRÍO 1']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        regr = RandomForestRegressor(n_estimators=10)
        regr.fit(X_train, y_train)
        # persist model
        joblib.dump(regr, 'rf_frio_1.pkl')

    def predict_grupo_frio_1(self, X):
        regr = joblib.load('rf_frio_1.pkl')
        predicts = regr.predict(X)
        return predicts

    def fit_grupo_frio_2(self):
        obj = dataset.Dataset()
        data = obj.read_dataset_limpio()
        X = data[['POTENCIA TERMICA GRUPO FRIO 2', 'ENTRADA AGUA A TORRE 2', 'SALIDA AGUA TORRE 2',
          'POTENCIA TRAFO 4', 'POTENCIA TRAFO 5', 'POTENCIA MEDIA CONECTADA', 'CONTROL FRÍO',
          'KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2', 'TEMPERATURA EXTERIOR']]
        y = data['POTENCIA GRUPO FRÍO 2']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        regr = RandomForestRegressor(n_estimators=10)
        regr.fit(X_train, y_train)
        # persist model
        joblib.dump(regr, 'rf_frio_2.pkl')

    def predict_grupo_frio_2(self, X):
        regr = joblib.load('rf_frio_2.pkl')
        predicts = regr.predict(X)
        return predicts

    def fit_carlos(self):
        obj = dataset.Dataset()
        data = obj.read_dataset_limpio()
        X = data[['TEMPERATURA SALIDA BOMBA CALOR CARLOS', 'POTENCIA TERMICA BOMBA CALOR CARLOS',
                  'C_O_P BOMBA CALOR CARLOS', 'POTENCIA TRAFO 4', 'POTENCIA TRAFO 5',
                  'TEMPERATURA EXTERIOR', 'TEMPERATURA AMBIENTE BOMBA CALOR CARLOS']]
        y = data['POTENCIA BOMBA CALOR CARLOS']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        regr = RandomForestRegressor(n_estimators=10)
        regr.fit(X_train, y_train)
        # persist model
        joblib.dump(regr, 'rf_carlos.pkl')

    def predict_carlos(self, X):
        regr = joblib.load('rf_carlos.pkl')
        predicts = regr.predict(X)
        return predicts

    def fit_felipe(self):
        obj = dataset.Dataset()
        data = obj.read_dataset_limpio()
        X = data[['TEMPERATURA SALIDA BOMBA CALOR FELIPE','POTENCIA TERMICA BOMBA CALOR FELIPE', 
          'C_O_P BOMBA CALOR FELIPE', 'POTENCIA TRAFO 4','POTENCIA TRAFO 5',
          'TEMPERATURA EXTERIOR', 'TEMPERATURA AMBIENTE BOMBA CALOR FELIPE' ]]
        y = data['POTENCIA BOMBA CALOR FELIPE']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        regr = RandomForestRegressor(n_estimators=10)
        regr.fit(X_train, y_train)
        # persist model
        joblib.dump(regr, 'rf_felipe.pkl')

    def predict_felipe(self, X):
        regr = joblib.load('rf_felipe.pkl')
        predicts = regr.predict(X)
        return predicts
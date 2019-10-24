import dataset
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

class Potencia:

    def fit_grupo_frio_1(self):
        pass

    def predict_grupo_frio_1(self, X):
        pass

    def fit_grupo_frio_2(self):
        pass

    def predict_grupo_frio_2(self, X):
        pass

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
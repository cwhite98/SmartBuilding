import dataset
##from sklearn.externals import joblib
import joblib
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

#For S3
import boto3
s3 = boto3.client('s3',
                  aws_access_key_id='AKIAJJQYB6EN75OXWVGA',
                  aws_secret_access_key='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',
                  region_name='us-east-2')
BUCKET_NAME = 'smart-building-integrador'


class COP:

    def fit_grupo_frio_1(self):
        obj = dataset.Dataset()
        data = obj.read_dataset_limpio()
        X = data[['POTENCIA GRUPO FRÍO 1', 'POTENCIA TERMICA GRUPO FRIO 1', 'TEMPERATURA EXTERIOR']]
        y = data['C_O_P MÁQUINA GRUPO FRÍO 1']
        neigh = KNeighborsRegressor(n_neighbors=15)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        neigh.fit(X_train, y_train) 
        # persist model
        #joblib.dump(neigh, 'neigh_frio_1.pkl')
        joblib.dump(neigh, open('neigh_frio_1.pkl', 'wb'))
    
    def predict_grupo_frio_1(self, X):
        #neigh = joblib.load('neigh_frio_1.pkl')        
        s3.download_file(BUCKET_NAME, 'models/neigh_frio_1.pkl', '/tmp/neigh_frio_1.pkl')
        neigh = joblib.load('/tmp/neigh_frio_1.pkl')
        print("PASE")
        predicts = neigh.predict(X)
        print(predicts)
        return predicts

    def fit_grupo_frio_2(self):
        obj = dataset.Dataset()
        data = obj.read_dataset_limpio()
        X = data[['POTENCIA GRUPO FRÍO 2', 'POTENCIA TERMICA GRUPO FRIO 2', 'TEMPERATURA EXTERIOR']]
        y = data['C_O_P MÁQUINA GRUPO FRÍO 2']
        neigh = KNeighborsRegressor(n_neighbors=15)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        neigh.fit(X_train, y_train) 
        # persist model
        joblib.dump(neigh, 'neigh_frio_2.pkl')
    
    def predict_grupo_frio_2(self, X):
        neigh = joblib.load('neigh_frio_2.pkl')
        predicts = neigh.predict(X)
        return predicts

    def fit_carlos(self):
        obj = dataset.Dataset()
        data = obj.read_dataset_limpio()
        X = data[['POTENCIA BOMBA CALOR CARLOS', 'POTENCIA TERMICA BOMBA CALOR CARLOS',
                  'TEMPERATURA EXTERIOR', 'TEMPERATURA SALIDA BOMBA CALOR CARLOS']]
        y = data['C_O_P BOMBA CALOR CARLOS']
        neigh = KNeighborsRegressor(n_neighbors=15)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        neigh.fit(X_train, y_train)
        # persist model
        joblib.dump(neigh, 'neigh_carlos.pkl')

    def predict_carlos(self, X):
        neigh = joblib.load('neigh_carlos.pkl')
        predicts = neigh.predict(X)
        return predicts

    def fit_felipe(self):
        obj = dataset.Dataset()
        data = obj.read_dataset_limpio()
        X = data[['POTENCIA BOMBA CALOR FELIPE', 'POTENCIA TERMICA BOMBA CALOR FELIPE', 'TEMPERATURA EXTERIOR',
                'TEMPERATURA SALIDA BOMBA CALOR FELIPE']]
        y = data['C_O_P BOMBA CALOR FELIPE']
        neigh = KNeighborsRegressor(n_neighbors=15)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        neigh.fit(X_train, y_train)
        # persist model
        joblib.dump(neigh, 'neigh_felipe.pkl')

    def predict_felipe(self, X):
        neigh = joblib.load('neigh_felipe.pkl')
        predicts = neigh.predict(X)
        return predicts

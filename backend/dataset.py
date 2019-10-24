import pandas as pd
import numpy as np


class Dataset:

    def read_dataset(self):
        data = pd.read_excel("../Datasets/HVAC.xlsx", "HISTORICO_DATOS")
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
        data = data[subLista]
        data["POTENCIA TERMICA BOMBA CALOR CARLOS"] = data["KILO CALORÍAS GENERADAS BOMBA CALOR CARLOS"] * 0.001163
        data["POTENCIA TERMICA BOMBA CALOR FELIPE"] = data["KILO CALORÍAS GENERADAS BOMBA CALOR FELIPE"] * 0.001163
        data["POTENCIA TERMICA GRUPO FRIO 1"] = data["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1"] * 0.001163
        data["POTENCIA TERMICA GRUPO FRIO 2"] = data["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2"] * 0.001163
        return data
    
    def read_dataset_limpio(self):
        data = pd.read_excel("../Datasets/HVAC_limpio.xlsx", "HVAC_limpio", index_col=0)
        data['Fecha- hora de lectura'] = (data['Fecha- hora de lectura'] - data['Fecha- hora de lectura'].min()) / np.timedelta64(1, 'D')
        return data

    def read_dataset_lectura(self):
        data = pd.read_excel("../Datasets/HVAC.xlsx", "HISTORICO_DATOS")
        variables_a_eliminar = ["C_O_P_ BOMBA CALOR FELIPE", "C_O_P_ BOMBA CALOR CARLOS",
                                "C_O_P_ INSTALACIÓN GRUPO FRÍO 1", "C_O_P_ INSTALACÍON GRUPO FRÍO 2",
                                "ORDEN", "VÁLVULA BY PASS SECUNDARIO FRÍO",
                                "TEMPERATURA CONTROL DE BY PASS SECUNDARIO", "SECUNDARIO FRÍO 1",
                                "SECUNDARIO FRÍO 2", "SECUNDARIO FRÍO 3", "MODO INVIERNO BC1",
                                "MODO INVIERNO BC2", "PERIODO P6", "CONTROL CALOR",
                                "CAPACIDAD BOMBA CALOR FELIPE %", "CAPACIDAD BOMBA CALOR CARLOS %",
                                "CAPACIDAD GRUPO DE FRÍO 1", " CAPACIDAD GRUPO DE FRÍO 2",
                                "IMPULSIÓN SECUNDARIO CALOR", "SECUNDARIO CALOR 1",
                                "SECUNDARIO CALOR 2", "SECUNDARIO CALOR 3"]
        lista_variables = data.columns.values.tolist()
        subLista = [x for x in lista_variables if x not in variables_a_eliminar]
        data = data[subLista]
        data["POTENCIA TERMICA BOMBA CALOR CARLOS"] = data["KILO CALORÍAS GENERADAS BOMBA CALOR CARLOS"] * 0.001163
        data["POTENCIA TERMICA BOMBA CALOR FELIPE"] = data["KILO CALORÍAS GENERADAS BOMBA CALOR FELIPE"] * 0.001163
        data["POTENCIA TERMICA GRUPO FRIO 1"] = data["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1"] * 0.001163
        data["POTENCIA TERMICA GRUPO FRIO 2"] = data["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2"] * 0.001163
        return data
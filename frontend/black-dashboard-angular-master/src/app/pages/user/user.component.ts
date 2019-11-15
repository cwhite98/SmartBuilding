import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from 'rxjs/Rx';

@Component({
  selector: "app-user",
  templateUrl: "user.component.html"
})
export class UserComponent implements OnInit {
  public predFrio1_cop;
  public potenciaFrio1=false;
  public potenciaFrio2=false;
  public potenciaCalorCarlos=false;
  public potenciaCalorFelipe=false;
  public tempSalidaCalorCarlos=false;
  public tempSalidaCalorFelipe=false;
  public potenciaTermicaFrio1=false;
  public potenciaTermicaFrio2=false;
  public potenciaTermicaCalorCarlos=false;
  public potenciaTermicaCalorFelipe=false;
  public tempAmbCalorCarlos=false;
  public tempAmbCalorFelipe=false;
  public entradaAgua1=false;
  public entradaAgua2=false;
  public salidaAgua1=false;
  public salidaAgua2=false;
  public kigofriFrio1=false;
  public kigofriFrio2=false;
  public potenciaTrafo4=false;
  public potenciaTrafo5=false;
  public potenciaMedia=false;
  public controlFrio=false;
  public tempExt=false;
  public labels=["POTENCIA GRUPO FRÍO 1",
    "POTENCIA GRUPO FRÍO 2",
    "POTENCIA BOMBA CALOR CARLOS",
    "POTENCIA BOMBA CALOR FELIPE",
    "TEMPERATURA SALIDA BOMBA CALOR FELIPE",
    "TEMPERATURA SALIDA BOMBA CALOR CARLOS",
    "POTENCIA TERMICA GRUPO FRIO 1",
    "POTENCIA TERMICA GRUPO FRIO 2",
    "POTENCIA TERMICA BOMBA CALOR CARLOS",
    "POTENCIA TERMICA BOMBA CALOR FELIPE",
    "TEMPERATURA AMBIENTE BOMBA CALOR CARLOS",
    "TEMPERATURA AMBIENTE BOMBA CALOR FELIPE",
    "ENTRADA AGUA A TORRE 1",
    "ENTRADA AGUA A TORRE 2",
    "SALIDA AGUA TORRE 1",
    "SALIDA AGUA TORRE 2",
    "KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1",
    "KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2",
    "POTENCIA TRAFO 4",
    "POTENCIA TRAFO 5",
    "POTENCIA MEDIA CONECTADA",
    "CONTROL FRÍO",
    "TEMPERATURA EXTERIOR"]
  public valores=[]
  public registros = -1;
  constructor(private http: HttpClient) {
    this.recibirRegistros();
    Observable.interval(4000).subscribe(x => {
      this.recibirRegistros();
    });
  }
  public recibirRegistros() {
    if (this.registros == -1) {
      this.predict_frio_1();
      this.registros++;
    } else if(this.registros > 9){
      this.registros = -1;
    } else {
      this.valores=[]
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA GRUPO FRÍO 1"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA GRUPO FRÍO 2"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA BOMBA CALOR CARLOS"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA BOMBA CALOR FELIPE"])
      this.valores.push(this.predFrio1_cop[this.registros]["TEMPERATURA SALIDA BOMBA CALOR CARLOS"])
      this.valores.push(this.predFrio1_cop[this.registros]["TEMPERATURA SALIDA BOMBA CALOR FELIPE"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA TERMICA GRUPO FRIO 1"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA TERMICA GRUPO FRIO 2"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA TERMICA BOMBA CALOR CARLOS"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA TERMICA BOMBA CALOR FELIPE"])
      this.valores.push(this.predFrio1_cop[this.registros]["TEMPERATURA AMBIENTE BOMBA CALOR CARLOS"])
      this.valores.push(this.predFrio1_cop[this.registros]["TEMPERATURA AMBIENTE BOMBA CALOR FELIPE"])
      this.valores.push(this.predFrio1_cop[this.registros]["ENTRADA AGUA A TORRE 1"])
      this.valores.push(this.predFrio1_cop[this.registros]["ENTRADA AGUA A TORRE 2"])
      this.valores.push(this.predFrio1_cop[this.registros]["SALIDA AGUA TORRE 1"])
      this.valores.push(this.predFrio1_cop[this.registros]["SALIDA AGUA TORRE 2"])
      this.valores.push(this.predFrio1_cop[this.registros]["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 1"])
      this.valores.push(this.predFrio1_cop[this.registros]["KIGO FRIGORÍAS GENERADAS GRUPO DE FRÍO 2"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA TRAFO 4"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA TRAFO 5"])
      this.valores.push(this.predFrio1_cop[this.registros]["POTENCIA MEDIA CONECTADA"])
      this.valores.push(this.predFrio1_cop[this.registros]["CONTROL FRÍO"])
      this.valores.push(this.predFrio1_cop[this.registros]["TEMPERATURA EXTERIOR"])
      this.potenciaFrio1=false;
      this.potenciaFrio2=false;
      this.potenciaCalorCarlos=false;
      this.potenciaCalorFelipe=false;
      this.tempSalidaCalorCarlos=false;
      this.tempSalidaCalorFelipe=false;
      this.potenciaTermicaFrio1=false;
      this.potenciaTermicaFrio2=false;
      this.potenciaTermicaCalorCarlos=false;
      this.potenciaTermicaCalorFelipe=false;
      this.tempAmbCalorCarlos=false;
      this.tempAmbCalorFelipe=false;
      this.entradaAgua1=false;
      this.entradaAgua2=false;
      this.salidaAgua1=false;
      this.salidaAgua2=false;
      this.kigofriFrio1=false;
      this.kigofriFrio2=false;
      this.potenciaTrafo4=false;
      this.potenciaTrafo5=false;
      this.potenciaMedia=false;
      this.controlFrio=false;
      this.tempExt=true;
      if(this.valores[0]>38){this.potenciaFrio1=true;}
      if(this.valores[1]>52){this.potenciaFrio2=true;}
      if(this.valores[2]>66){this.potenciaCalorCarlos =true;}
      if(this.valores[3]>66){this.potenciaCalorFelipe=true;}
      if(this.valores[4]>42){this.tempSalidaCalorCarlos=true;}
      if(this.valores[5]>42){this.tempSalidaCalorFelipe=true;}
      if(this.valores[6]>33){this.potenciaTermicaFrio1=true;}
      if(this.valores[7]>33){this.potenciaTermicaFrio2=true;}
      if(this.valores[8]>33){this.potenciaTermicaCalorCarlos=true;}
      if(this.valores[9]>33){this.potenciaTermicaCalorFelipe=true;}
      if(this.valores[10]>25){this.tempAmbCalorCarlos=true;}
      if(this.valores[11]>24){this.tempAmbCalorFelipe=true;}
      if(this.valores[12]>28){this.entradaAgua1=true;}
      if(this.valores[13]>28){this.entradaAgua2=true;}
      if(this.valores[14]>26){this.salidaAgua1=true;}
      if(this.valores[15]>26){this.salidaAgua2=true;}
      if(this.valores[16]>148400){this.kigofriFrio1=true;}
      if(this.valores[17]>153519){this.kigofriFrio2=true;}
      if(this.valores[18]>408){this.potenciaTrafo4=true;}
      if(this.valores[19]>475){this.potenciaTrafo5=true;}
      if(this.valores[20]>1016){this.potenciaMedia=true;}
      if(this.valores[21]>14){this.controlFrio=true;}
      if(this.valores[21]>23){this.tempExt=true;}

      this.registros++;
    }
  }
  public predict_frio_1() {
    this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-frio-1-cop').subscribe(
      res => {
        this.predFrio1_cop = this.json2array(res)
      },
      err => {
        console.log(err);
      }
    );

  }
  public json2array(json) {
    var result = [];
    var keys = Object.keys(json);
    keys.forEach(function (key) {
      result.push(json[key]);
    });
    return result;
  }
  ngOnInit() {}
}

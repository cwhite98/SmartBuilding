import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from 'rxjs/Rx';

@Component({
  selector: "app-user",
  templateUrl: "user.component.html"
})
export class UserComponent implements OnInit {
  public predFrio1_cop;
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
      console.log(this.predFrio1_cop[this.registros])
      this.registros++;
    }
  }
  public predict_frio_1() {
    this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict_frio_1_cop').subscribe(
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

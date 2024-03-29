import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from 'rxjs/Rx';
import Chart from 'chart.js';

@Component({
  selector: "app-dashboard",
  templateUrl: "dashboard.component.html"
})
export class DashboardComponent implements OnInit {
  //arreglos para mostrar datos
  public errores = [];
  public tempExt = [];
  public time = [];
  public COPFrio1 = [];
  public COPFrio1Pre = [];
  public COPFrio2 = [];
  public COPFrio2Pre = [];
  public COPCalorCarlos = [];
  public COPCalorCarlosPre = [];
  public COPCalorFelipe = [];
  public COPCalorFelipePre = [];
  public potenciaFrio1 = [];
  public potenciaFrio2 = [];
  public potenciaCalorCarlos = [];
  public potenciaCalorFelipe = [];
  public datosTiempoReal = [];
  public potenciaFrio1Real = [];
  public potenciaFrio2Real = [];
  public potenciaCalorCarlosReal = [];
  public potenciaCalorFelipeReal = [];
  public labels2 = ["COP FRIO 1", "COP FRIO 2", "COP CALOR CARLOS", "COP CALOR FELIPE", "POTENCIA FRIO 1", "POTENCIA FRIO 2", "POTENCIA CALOR CARLOS", "POTENCIA CALOR FELIPE"]
  public canvas: any;
  public ctx;
  //donde se guardan los datos traidos del http
  public predFrio1_cop;
  public predFrio1_potencia;
  public predFrio2_cop;
  public predFrio2_potencia;
  public predCarlos_cop;
  public predCarlos_potencia;
  public predFelipe_cop;
  public predFelipe_potencia;
  public datasets: any;
  public data: any;
  //graficas
  public myChartData;
  public myChartCOPFrio1;
  public myChartPotenciaFrio1;
  public myChartCOPFrio2
  public myChartPotenciaFrio2;
  public myChartCOPCalorCarlos;
  public myChartPotenciaCalorCarlos;
  public myChartCOPCalorFelipe;
  public myChartPotenciaCalorFelipe;
  public registros = -1;
  public contador = 0;


  constructor(private http: HttpClient) {
    this.recibirRegistros();
    Observable.interval(4000).subscribe(x => {
      this.recibirRegistros();
    });
  }
  async recibirRegistros() {
    if (this.registros == -1) {
      this.errores = [];
      await this.predict_frio_1();
      await this.predict_frio_2();
      await this.predict_carlos();
      await this.predict_felipe();
      this.registros++;
    } else if (this.registros > 9) {
      this.registros = -1;
    } else {
      if (this.contador < 10) {
        this.actualizar()
      }
      else {
        this.tempExt.shift()
        this.COPFrio1.shift()
        this.COPFrio1Pre.shift()
        this.time.shift()
        this.COPFrio2.shift()
        this.COPFrio2Pre.shift()
        this.COPCalorCarlos.shift()
        this.COPCalorCarlosPre.shift()
        this.COPCalorFelipe.shift()
        this.COPCalorFelipePre.shift()
        this.potenciaFrio1.shift()
        this.potenciaFrio1Real.shift()
        this.potenciaFrio2.shift()
        this.potenciaFrio2Real.shift()
        this.potenciaCalorCarlos.shift()
        this.potenciaCalorCarlosReal.shift()
        this.potenciaCalorFelipe.shift()
        this.potenciaCalorFelipeReal.shift()
        this.actualizar()
      }
      this.registros++;
      this.contador++;
    }
  }
  public actualizar() {
    this.tempExt.push(this.predFrio1_cop[this.registros]["TEMPERATURA EXTERIOR"])
    this.COPFrio1.push(this.predFrio1_cop[this.registros]["C_O_P MÁQUINA GRUPO FRÍO 1"])
    this.COPFrio1Pre.push(this.predFrio1_cop[this.registros]["C_O_P MÁQUINA GRUPO FRÍO 1 PREDICHO"])
    this.time.push(this.predFrio1_cop[this.registros]["Fecha- hora de lectura"])
    this.myChartCOPFrio1.data.datasets[0].data = this.COPFrio1;
    this.myChartCOPFrio1.data.datasets[1].data = this.COPFrio1Pre;
    this.myChartCOPFrio1.update()
    this.COPFrio2.push(this.predFrio2_cop[this.registros]["C_O_P MÁQUINA GRUPO FRÍO 2"])
    this.COPFrio2Pre.push(this.predFrio2_cop[this.registros]["C_O_P MÁQUINA GRUPO FRÍO 2 PREDICHO"])
    this.myChartCOPFrio2.data.datasets[0].data = this.COPFrio2;
    this.myChartCOPFrio2.data.datasets[1].data = this.COPFrio2Pre;
    this.myChartCOPFrio2.update()
    this.COPCalorCarlos.push(this.predCarlos_cop[this.registros]["C_O_P BOMBA CALOR CARLOS"])
    this.COPCalorCarlosPre.push(this.predCarlos_cop[this.registros]["C_O_P BOMBA CALOR CARLOS PREDICHO"])
    this.myChartCOPCalorCarlos.update()
    this.COPCalorFelipe.push(this.predFelipe_cop[this.registros]["C_O_P BOMBA CALOR FELIPE"])
    this.COPCalorFelipePre.push(this.predFelipe_cop[this.registros]["C_O_P BOMBA CALOR FELIPE PREDICHO"])
    this.myChartCOPCalorFelipe.update()
    this.potenciaFrio1.push(this.predFrio1_potencia[this.registros]["POTENCIA GRUPO FRÍO 1 PREDICHA"])
    this.potenciaFrio1Real.push(this.predFrio1_cop[this.registros]["POTENCIA GRUPO FRÍO 1"])
    this.myChartPotenciaFrio1.data.datasets[0].data = this.potenciaFrio1
    this.myChartPotenciaFrio1.data.datasets[1].data = this.potenciaFrio1Real
    this.myChartPotenciaFrio1.update();
    this.potenciaFrio2.push(this.predFrio2_potencia[this.registros]["POTENCIA GRUPO FRÍO 2 PREDICHA"])
    this.potenciaFrio2Real.push(this.predFrio2_cop[this.registros]["POTENCIA GRUPO FRÍO 2"])
    this.myChartPotenciaFrio2.data.datasets[0].data = this.potenciaFrio2
    this.myChartPotenciaFrio2.data.datasets[1].data = this.potenciaFrio2Real
    this.myChartPotenciaFrio2.update();
    this.potenciaCalorCarlos.push(this.predCarlos_potencia[this.registros]["POTENCIA BOMBA CALOR CARLOS PREDICHA"])
    this.potenciaCalorCarlosReal.push(this.predCarlos_cop[this.registros]["POTENCIA BOMBA CALOR CARLOS"])
    this.myChartPotenciaCalorCarlos.data.datasets[0].data = this.potenciaCalorCarlos
    this.myChartPotenciaCalorCarlos.data.datasets[1].data = this.potenciaCalorCarlosReal
    this.myChartPotenciaCalorCarlos.update();
    this.potenciaCalorFelipe.push(this.predFelipe_potencia[this.registros]["POTENCIA BOMBA CALOR FELIPE PREDICHA"])
    this.potenciaCalorFelipeReal.push(this.predFelipe_cop[this.registros]["POTENCIA BOMBA CALOR FELIPE"])
    this.myChartPotenciaCalorFelipe.data.datasets[0].data = this.potenciaCalorFelipe
    this.myChartPotenciaCalorFelipe.data.datasets[1].data = this.potenciaCalorFelipeReal
    this.myChartPotenciaCalorFelipe.update();
    //Temperatura externa
    this.myChartData.data.datasets[0].data = this.tempExt;
    this.myChartData.update();
    //datos tiempo real
    this.datosTiempoReal = []
    this.datosTiempoReal.push(this.predFrio1_cop[this.registros]["C_O_P MÁQUINA GRUPO FRÍO 1"])
    this.datosTiempoReal.push(this.predFrio1_cop[this.registros]["C_O_P MÁQUINA GRUPO FRÍO 2"])
    this.datosTiempoReal.push(this.predFrio1_cop[this.registros]["C_O_P BOMBA CALOR CARLOS"])
    this.datosTiempoReal.push(this.predFrio1_cop[this.registros]["C_O_P BOMBA CALOR FELIPE"])

    this.datosTiempoReal.push(this.predFrio1_potencia[this.registros]["POTENCIA GRUPO FRÍO 1 PREDICHA"])
    this.datosTiempoReal.push(this.predFrio2_potencia[this.registros]["POTENCIA GRUPO FRÍO 2 PREDICHA"])
    this.datosTiempoReal.push(this.predCarlos_potencia[this.registros]["POTENCIA BOMBA CALOR CARLOS PREDICHA"])
    this.datosTiempoReal.push(this.predFelipe_potencia[this.registros]["POTENCIA BOMBA CALOR FELIPE PREDICHA"])
  }
  //------------------------------------------------------------------------------------------------------
  //------------------------------------------------------------------------------------------------------
  //------------------------------------------------------------------------------------------------------
  //------------------------------------------------------------------------------------------------------
  //------------------------------------------------------------------------------------------------------
  //------------------------------------------------------------------------------------------------------
  //------------------------------------------------------------------------------------------------------
  //------------------------------------------------------------------------------------------------------
  //Peticiones http
  async predict_frio_1() {
    const response = await this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-frio-1-cop').toPromise();
    this.predFrio1_cop = this.json2array(response)
    for (var i = 0; i < 10; i++) {
      if (!this.errores.includes(this.predFrio1_cop[i]["Diagnostico"]) && (this.predFrio1_cop[i]["Diagnostico"] != " ")) {
        if (this.predFrio1_cop[i]["Diagnostico"].includes("|")) {
          var diagnosticos = this.predFrio1_cop[i]["Diagnostico"].split("|")
          for (var j = 0; j < diagnosticos.length; j++) {
            if (!this.errores.includes(diagnosticos[j])) {
              this.errores.push(diagnosticos[j])
            }
          }
        } else {
          this.errores.push(this.predFrio1_cop[i]["Diagnostico"])
        }
      }
    }

    const response1 = await this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-frio-1-potencia').toPromise();
    this.predFrio1_potencia = this.json2array(response1)
    for (var i = 0; i < 10; i++) {
      if (!this.errores.includes(this.predFrio1_potencia[i]["Diagnostico"]) && (this.predFrio1_potencia[i]["Diagnostico"] != " ")) {
        if (this.predFrio1_potencia[i]["Diagnostico"].includes("|")) {
          var diagnosticos = this.predFrio1_potencia[i]["Diagnostico"].split("|")
          for (var j = 0; j < diagnosticos.length; j++) {
            if (!this.errores.includes(diagnosticos[j])) {
              this.errores.push(diagnosticos[j])
            }
          }
        } else {
          this.errores.push(this.predFrio1_potencia[i]["Diagnostico"])
        }
      }
    }
  }

  async predict_frio_2() {
    const response = await this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-frio-2-cop').toPromise();
    this.predFrio2_cop = this.json2array(response)
    for (var i = 0; i < 10; i++) {
      if (!this.errores.includes(this.predFrio2_cop[i]["Diagnostico"]) && (this.predFrio2_cop[i]["Diagnostico"] != " ")) {
        if (this.predFrio2_cop[i]["Diagnostico"].includes("|")) {
          var diagnosticos = this.predFrio2_cop[i]["Diagnostico"].split("|")
          for (var j = 0; j < diagnosticos.length; j++) {
            if (!this.errores.includes(diagnosticos[j])) {
              this.errores.push(diagnosticos[j])
            }
          }
        } else {
          this.errores.push(this.predFrio2_cop[i]["Diagnostico"])
        }
      }
    }
    const response1 = await this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-frio-2-potencia').toPromise();
    this.predFrio2_potencia = this.json2array(response1)
    for (var i = 0; i < 10; i++) {
      if (!this.errores.includes(this.predFrio2_potencia[i]["Diagnostico"]) && (this.predFrio2_potencia[i]["Diagnostico"] != " ")) {
        if (this.predFrio2_potencia[i]["Diagnostico"].includes("|")) {
          var diagnosticos = this.predFrio2_potencia[i]["Diagnostico"].split("|")
          for (var j = 0; j < diagnosticos.length; j++) {
            if (!this.errores.includes(diagnosticos[j])) {
              this.errores.push(diagnosticos[j])
            }
          }
        } else {
          this.errores.push(this.predFrio2_potencia[i]["Diagnostico"])
        }
      }
    }
  }

  async predict_carlos() {
    const response = await this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-carlos-cop').toPromise();
    this.predCarlos_cop = this.json2array(response)
    for (var i = 0; i < 10; i++) {
      if (!this.errores.includes(this.predCarlos_cop[i]["Diagnostico"]) && (this.predCarlos_cop[i]["Diagnostico"] != " ")) {
        if (this.predCarlos_cop[i]["Diagnostico"].includes("|")) {
          var diagnosticos = this.predCarlos_cop[i]["Diagnostico"].split("|")
          for (var j = 0; j < diagnosticos.length; j++) {
            if (!this.errores.includes(diagnosticos[j])) {
              this.errores.push(diagnosticos[j])
            }
          }
        } else {
          this.errores.push(this.predCarlos_cop[i]["Diagnostico"])
        }
      }
    }

    const response1 = await this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-carlos-potencia').toPromise();
    this.predCarlos_potencia = this.json2array(response1)
    for (var i = 0; i < 10; i++) {
      if (!this.errores.includes(this.predCarlos_potencia[i]["Diagnostico"]) && (this.predCarlos_potencia[i]["Diagnostico"] != " ")) {
        if (this.predCarlos_potencia[i]["Diagnostico"].includes("|")) {
          var diagnosticos = this.predCarlos_potencia[i]["Diagnostico"].split("|")
          for (var j = 0; j < diagnosticos.length; j++) {
            if (!this.errores.includes(diagnosticos[j])) {
              this.errores.push(diagnosticos[j])
            }
          }
        } else {
          this.errores.push(this.predCarlos_potencia[i]["Diagnostico"])
        }
      }
    }
  }

  async predict_felipe() {
    const response = await this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-felipe-cop').toPromise();
    this.predFelipe_cop = this.json2array(response)
    for (var i = 0; i < 10; i++) {
      if (!this.errores.includes(this.predFelipe_cop[i]["Diagnostico"]) && (this.predFelipe_cop[i]["Diagnostico"] != " ")) {
        if (this.predFelipe_cop[i]["Diagnostico"].includes("|")) {
          var diagnosticos = this.predFelipe_cop[i]["Diagnostico"].split("|")
          for (var j = 0; j < diagnosticos.length; j++) {
            if (!this.errores.includes(diagnosticos[j])) {
              this.errores.push(diagnosticos[j])
            }
          }
        } else {
          this.errores.push(this.predFelipe_cop[i]["Diagnostico"])
        }
      }
    }

    const response1 = await this.http.get('https://3f3sok0dv9.execute-api.us-east-2.amazonaws.com/v1/predict-felipe-potencia').toPromise();
    this.predFelipe_potencia = this.json2array(response1)
    for (var i = 0; i < 10; i++) {
      if (!this.errores.includes(this.predFelipe_potencia[i]["Diagnostico"]) && (this.predFelipe_potencia[i]["Diagnostico"] != " ")) {
        if (this.predFelipe_potencia[i]["Diagnostico"].includes("|")) {
          var diagnosticos = this.predFelipe_potencia[i]["Diagnostico"].split("|")
          for (var j = 0; j < diagnosticos.length; j++) {
            if (!this.errores.includes(diagnosticos[j])) {
              this.errores.push(diagnosticos[j])
            }
          }
        } else {
          this.errores.push(this.predFelipe_potencia[i]["Diagnostico"])
        }
      }
    }
  }

  //metodo que pasa de json a array
  public json2array(json) {
    var result = [];
    var keys = Object.keys(json);
    keys.forEach(function (key) {
      result.push(json[key]);
    });
    return result;
  }
  
  ngOnInit() {

    var gradientChartOptionsConfigurationWithTooltipRed: any = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 60,
            suggestedMax: 125,
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }],

        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(233,32,16,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9a9a9a"
          }
        }]
      }
    };

    var gradientChartOptionsConfigurationWithTooltipGreen: any = {
      maintainAspectRatio: false,
      legend: {
        display: false
      },

      tooltips: {
        backgroundColor: '#f5f5f5',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
      },
      responsive: true,
      scales: {
        yAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(29,140,248,0.0)',
            zeroLineColor: "transparent",
          },
          ticks: {
            suggestedMin: 50,
            suggestedMax: 125,
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }],

        xAxes: [{
          barPercentage: 1.6,
          gridLines: {
            drawBorder: false,
            color: 'rgba(0,242,195,0.1)',
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 20,
            fontColor: "#9e9e9e"
          }
        }]
      }
    };

    //------------------------------------------------------------------------------------------------------
    //------------------------------------------------------------------------------------------------------
    //------------------------------------------------------------------------------------------------------
    //------------------------------------------------------------------------------------------------------
    //------------------------------------------------------------------------------------------------------
    //------------------------------------------------------------------------------------------------------
    //------------------------------------------------------------------------------------------------------
    //------------------------------------------------------------------------------------------------------


    //Grafica Temperatura Exterior
    this.canvas = document.getElementById("chartTempExt");
    this.ctx = this.canvas.getContext("2d");

    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(233,32,16,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(233,32,16,0.0)');
    gradientStroke.addColorStop(0, 'rgba(233,32,16,0)'); //red colors

    var config = {
      type: 'line',
      data: {
        labels: this.time,
        datasets: [{
          label: "My First dataset",
          fill: true,
          backgroundColor: gradientStroke,
          borderColor: '#ec250d',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          pointBackgroundColor: '#ec250d',
          pointBorderColor: 'rgba(255,255,255,0)',
          pointHoverBackgroundColor: '#ec250d',
          pointBorderWidth: 20,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 15,
          pointRadius: 4,
          data: this.tempExt,
        }]
      },
      options: {
        gradientChartOptionsConfigurationWithTooltipRed,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { suggestedMin: 0, suggestedMan: 20 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: false },
      }
    };
    this.myChartData = new Chart(this.ctx, config);



    //Grafica COP frio1

    this.canvas = document.getElementById("chartCOPFrio1");
    this.ctx = this.canvas.getContext("2d");

    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(233,32,16,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(233,32,16,0.0)');
    gradientStroke.addColorStop(0, 'rgba(233,32,16,0)'); //red colors

    var dataCOPFrio1 = {
      labels: this.time,
      datasets: [{
        label: "Dato leído",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#d600c4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#d600c4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#d600c4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.COPFrio1,
      }, {
        label: "Dato predicho",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#00d6b4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#00d6b4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#00d6b4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.COPFrio1Pre,
      }]
    };

    this.myChartCOPFrio1 = new Chart(this.ctx, {
      type: 'line',
      data: dataCOPFrio1,
      options: {
        gradientChartOptionsConfigurationWithTooltipRed,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { max: 10, min: 0 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: true, position: "bottom" },
      }
    });

    //grafica Potencia Frio 1
    this.canvas = document.getElementById("chartPotenciaFrio1");
    this.ctx = this.canvas.getContext("2d");
    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


    this.myChartPotenciaFrio1 = new Chart(this.ctx, {
      type: 'line',
      responsive: true,
      legend: {
        display: false
      },
      data: {
        labels: this.time,
        datasets: [{
          label: "Potencia Predicha",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: this.potenciaFrio1,
        },{
          label: "Potencia Real",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#dfe364',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: this.potenciaFrio1Real,
        }]
      },
      options: {
        gradientChartOptionsConfigurationWithTooltipRed,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { suggestedMin: 0, suggestedMax: 20 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: true, position: "bottom" },
      }
    });




    //Grafica COP frio 2
    this.canvas = document.getElementById("chartCOPFrio2");
    this.ctx = this.canvas.getContext("2d");


    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
    gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
    gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors

    var dataCOPFrio2 = {
      labels: this.time,
      datasets: [{
        label: "Dato Leído",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#d600c4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#d600c4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#d600c4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.COPFrio2,
      }, {
        label: "Dato predicho",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#00d6b4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#00d6b4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#00d6b4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.COPFrio2Pre,
      }]
    };

    this.myChartCOPFrio2 = new Chart(this.ctx, {
      type: 'line',
      data: dataCOPFrio2,
      options: {
        gradientChartOptionsConfigurationWithTooltipGreen,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { max: 20, min: 0 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: true, position: "bottom" },
      }

    });
    //grafica Potencia Frio 2
    this.canvas = document.getElementById("chartPotenciaFrio2");
    this.ctx = this.canvas.getContext("2d");
    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


    this.myChartPotenciaFrio2 = new Chart(this.ctx, {
      type: 'line',
      responsive: true,
      legend: {
        display: false
      },
      data: {
        labels: this.time,
        datasets: [{
          label: "Potencia Predicha",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: this.potenciaFrio2,
        },{label: "Potencia Real",
        fill: true,
        backgroundColor: gradientStroke,
        hoverBackgroundColor: gradientStroke,
        borderColor: '#dfe364',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        data: this.potenciaFrio2Real,
      }]
      },
      options: {
        gradientChartOptionsConfigurationWithTooltipRed,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { suggestedMin: 0, suggestedMax: 20 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: true, position: "bottom" },
      }
    });

    //Grafica COP Calor Carlos
    this.canvas = document.getElementById("chartCOPCalorCarlos");
    this.ctx = this.canvas.getContext("2d");


    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
    gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
    gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors

    var dataCOPCarlorCarlos = {
      labels: this.time,
      datasets: [{
        label: "Dato Leído",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#d600c4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#d600c4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#d600c4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.COPCalorCarlos,
      }, {
        label: "Dato predicho",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#00d6b4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#00d6b4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#00d6b4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.COPCalorCarlosPre,
      }]
    };

    this.myChartCOPCalorCarlos = new Chart(this.ctx, {
      type: 'line',
      data: dataCOPCarlorCarlos,
      options: {
        gradientChartOptionsConfigurationWithTooltipGreen,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { max: 20, min: 0 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: true, position: "bottom" },
      }

    });

    //grafica Potencia Calor Carlos
    this.canvas = document.getElementById("chartPotenciaCalorCarlos");
    this.ctx = this.canvas.getContext("2d");
    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


    this.myChartPotenciaCalorCarlos = new Chart(this.ctx, {
      type: 'line',
      responsive: true,
      legend: {
        display: false
      },
      data: {
        labels: this.time,
        datasets: [{
          label: "Potencia Predicha",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: this.potenciaCalorCarlos,
        },{
          label: "Potencia Real",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#dfe364',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: this.potenciaCalorCarlosReal,
        }]
      },
      options: {
        gradientChartOptionsConfigurationWithTooltipRed,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { suggestedMin: 0, suggestedMax: 20 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: true, position: "bottom" },
      }
    });

    //Grafica COP Calor Felipe
    this.canvas = document.getElementById("chartCOPCalorFelipe");
    this.ctx = this.canvas.getContext("2d");


    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
    gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
    gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors

    var dataCOPCarlorFelipe = {
      labels: this.time,
      datasets: [{
        label: "Dato Leído",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#d600c4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#d600c4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#d600c4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.COPCalorFelipe,
      }, {
        label: "Dato predicho",
        fill: true,
        backgroundColor: gradientStroke,
        borderColor: '#00d6b4',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: '#00d6b4',
        pointBorderColor: 'rgba(255,255,255,0)',
        pointHoverBackgroundColor: '#00d6b4',
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        data: this.COPCalorFelipePre,
      }]
    };

    this.myChartCOPCalorFelipe = new Chart(this.ctx, {
      type: 'line',
      data: dataCOPCarlorFelipe,
      options: {
        gradientChartOptionsConfigurationWithTooltipGreen,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { max: 20, min: 0 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: true, position: "bottom" },
      }

    });

    //grafica Potencia Calor Felipe
    this.canvas = document.getElementById("chartPotenciaCalorFelipe");
    this.ctx = this.canvas.getContext("2d");
    var gradientStroke = this.ctx.createLinearGradient(0, 230, 0, 50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


    this.myChartPotenciaCalorFelipe = new Chart(this.ctx, {
      type: 'line',
      responsive: true,
      legend: {
        display: false
      },
      data: {
        labels: this.time,
        datasets: [{
          label: "Potencia Predicha",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: this.potenciaCalorFelipe,
        },{
          label: "Potencia Real",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#dfe364',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 0.0,
          data: this.potenciaCalorFelipeReal,
        }]
      },
      options: {
        gradientChartOptionsConfigurationWithTooltipRed,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{ ticks: { suggestedMin: 0, suggestedMax: 20 } }], xAxes: [{
            ticks: {
              display: false //this will remove only the label
            }
          }]
        },
        legend: { display: true, position: "bottom" },
      }
    });

  }
  public updateOptions() {

  }
}

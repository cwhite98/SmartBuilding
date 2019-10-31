import { Component, OnInit,Input } from '@angular/core';

@Component({
  selector: "app-alert",
  templateUrl: "./alert.component.html",
  styleUrls: ["./alert.component.scss"]
})
export class AlertComponent implements OnInit {
  public show=false
  @Input('error') error:any;
  constructor() { 
    
  }

  ngOnInit() {
    if(this.error.includes("apagada")){
      this.show=true
    }
    else{
      this.show=false
    }
  }

}

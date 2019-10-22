import { Component, OnInit,Input } from '@angular/core';

@Component({
  selector: "app-alert",
  templateUrl: "./alert.component.html",
  styleUrls: ["./alert.component.scss"]
})
export class AlertComponent implements OnInit {
  @Input('test') test:any;
  constructor() { }

  ngOnInit() {
  }

}

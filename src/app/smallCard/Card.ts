import {Component, OnInit} from '@angular/core';
import { FirebaseService } from '../services/firebase.service';
import { Router, Params } from '@angular/router';
/**
 * @Small card
 */
@Component({
  selector: 'card-sm',
  templateUrl: 'Card.html',
  styleUrls: ['Card-Sm.css'],
})
export class cardSm {
  week: Array<any>;
  average = 0.0;
  i: number = 0;
  total = 5;
  activity = 0;
  settings: Array<any>;
  daily = 0;

    constructor(
    public firebaseService: FirebaseService,
    private router: Router
  ) { }

  /**
   * This is called when the page is loaded
   */
  ngOnInit(){
    this.getData();
    this.getSettings();
  }

  getData(){
    this.firebaseService.getWeek().subscribe(result => {
      this.week = result;
    })
  }

  getSettings() {
    this.firebaseService.getSettings().subscribe(result => {
      this.settings = result;
      for (let item of this.settings){
        this.daily = Math.floor(item.payload.doc.data().Daily);
      }
    })
  }

  getAverage() {
    this.i = 0;
    this.average = 0;
    this.total = 0;
    for (const item of this.week ){
      /** Math.floor is used to ensure the variable is parsed as an integer, otherwise when added to the total it will concatenate
       *  e.g (5+5 = 55)
       */
      this.activity = Math.floor(item.payload.doc.data().Activity);
      if (this.activity > 0) {
       this.total = this.total + this.activity;
      }
      this.i = this.i + 1;
    }
    this.average = this.total / this.i;
    /**
     * Math.round is used to round the average to 2 decimals to ensure easier reading
     */
    return Math.round((this.average + Number.EPSILON) * 100) / 100;
    }
}
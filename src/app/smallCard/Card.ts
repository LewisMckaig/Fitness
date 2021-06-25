/**
 * Card.ts
 * style - card-Sm.css
 * html - Card.html
 * Author: Lewis Mckaig
 * Date: April 2021
 *
 * Description: Small card, displays the last 7 days of activity and the average minutes of activity
 * shares css file with "goalCard"
 *
 */
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
  average = 0.0; // average daily activity, double
  i: number = 0; // used for looping
  total = 5; // used for calculating average activity
  activity = 0;
  settings: Array<any>;
  daily = 0;
  toggle = true;
  trophies: Array<any>;
  Daily = 0;
  myimage = 'award.svg';

    constructor(
    public firebaseService: FirebaseService,
    private router: Router
  ) { }

  /**
   * runs getData and getSettings() when page is loaded
   */
  ngOnInit(){
    this.getSettings();
    this.getData();
  }

  /**
   * gets the settings from the db
   */
  getSettings() {
    this.firebaseService.getSettings().subscribe(result => {
      this.settings = result;
      for (let item of this.settings){
        this.daily = Math.floor(item.payload.doc.data().Daily);
        this.firebaseService.getGoals(this.daily).subscribe(goals => {
        this.trophies = goals;
      })
      }
    })
  }

  /**
   * gets the last 7 days in the database
   */
  getData(){
    this.firebaseService.getWeek().subscribe(result => {
      this.week = result;
    })
  }

  /**
   * returns : average, rounded to 2 dp
   * gets the average daily activity
   */
  getAverage() {
    this.i = 0;
    this.average = 0;
    this.total = 0;
    for (const item of this.week ){
      // Math.floor is used to ensure the variable is parsed as an integer, otherwise when added to the total it will concatenate
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

    toggleCard(){
      if (this.toggle === true){
        this.toggle = false;
      }
      else if (this.toggle === false){
        this.toggle = true;
      }
    }
}
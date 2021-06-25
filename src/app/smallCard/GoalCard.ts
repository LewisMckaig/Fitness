/**
 * GoalCard.ts
 * style - card-Sm.css
 * html - GoalCard.html
 * Author: Lewis Mckaig
 * Date: April 2021
 *
 * Description: Small card, displays the curernt goals and the current weekly activity
 * shares a css with smallCard
 *
 */
import {Component, OnInit} from '@angular/core';
import { FirebaseService } from '../services/firebase.service';
import { Router, Params } from '@angular/router';
/**
 * @Small card 
 */
@Component({
  selector: 'card-Goal',
  templateUrl: 'GoalCard.html',
  styleUrls: ['Card-Sm.css'],
})
export class GoalCard {
  settings: Array<any>;
  week : Array<any>;
  activity = 0;
  total = 0;

    constructor(
    public firebaseService: FirebaseService,
    private router: Router
  ) { }

  /**
   * Runs getData() and getSettings() when loaded
   */
  ngOnInit(){
    this.getData();
    this.getSettings();
  }

  /**
   * gets the settings that determine the weekly and daily goals
   */
  getSettings(){
    this.firebaseService.getSettings().subscribe(result => {
      this.settings = result;
    })
  }

  /**
   * gets the last 7 items in db, used for calculating total weekly active minutes
   */
  getData()  {
    this.firebaseService.getWeek().subscribe(result => {
      this.week = result;
    })
  }

  /**
   * calculates the toal active minutes
   * returns: total
   */
  getTotal() {
    this.total = 0;
    for (const item of this.week ){
      /** Math.floor is used to ensure the variable is parsed as an integer, otherwise when added to the total it will concatenate
       *  e.g (5+5 = 55)
       */
      this.activity = Math.floor(item.payload.doc.data().Activity);
      if (this.activity > 0) {
       this.total = this.total + this.activity;
      }
    }
    return this.total
    }
}
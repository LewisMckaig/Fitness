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
   * This is called when the page is loaded
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

  getData()  {
    this.firebaseService.getWeek().subscribe(result => {
      this.week = result;
    })
  }

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
/**
 * card.ts
 * style - card.css
 * html - card.html
 * Author: Lewis Mckaig
 * Date: April 2021
 *
 * Description: Main Card which shows todays active minutes and has a toggle button for turning recording on/off
 *
 *
 */
import {Component, OnInit} from '@angular/core';
import { FirebaseService } from '../services/firebase.service';
import { Router, Params } from '@angular/router';

/**
 * @title 
 */
@Component({
  selector: 'Card',
  templateUrl: 'Card.html',
  styleUrls: ['Card.css'],
})
export class Card implements OnInit{
  timeValue: number = 0;
  progress: number = 0;
  items: Array<any>;
  settings: Array<any>;
  daily = 0;
  isChecked: boolean;

    constructor(
    public firebaseService: FirebaseService,
    private router: Router
  ) { }

  /**
   * runs getData() and getSettings() on page load
   */
  ngOnInit() {
    this.getData();
    this.getSettings();
  }

  /**
   * gets the most recent daily activity item in db
   */
  getData() {
    this.firebaseService.getReadings().subscribe(result => {
      this.items = result;
    })
  }
  /**
   * gets the settings, these values are used 
   */
  getSettings() {
    this.firebaseService.getSettings().subscribe(result => {
      this.settings = result;
      for (const item of this.settings){
        this.daily = Math.floor(item.payload.doc.data().Daily);
        this.isChecked = item.payload.doc.data().Recording;
      }
    })
  }

  /**
   * runs when toggle switch is pressed, passes value to firebaseservice.ts
   */
  toggle() {
    this.firebaseService.changeRecordingState(this.isChecked);
  }
}
import {Component, OnInit} from '@angular/core';
import { FirebaseService } from '../services/firebase.service';
import { Router, Params } from '@angular/router';

/**
 * @title Card with multiple sections
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
  isChecked : boolean;

    constructor(
    public firebaseService: FirebaseService,
    private router: Router
  ) { }

  ngOnInit() {
    this.getData();
    this.getSettings();
  }

  getData() {
    this.firebaseService.getReadings().subscribe(result => {
      this.items = result;
    })
  }

  getSettings() {
    this.firebaseService.getSettings().subscribe(result => {
      this.settings = result;
      for (const item of this.settings){
        this.daily = Math.floor(item.payload.doc.data().Daily);
        this.isChecked = item.payload.doc.data().Recording;
      }
    })
  }

  toggle() {
    this.firebaseService.changeRecordingState(this.isChecked);
  }
}
import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FirebaseService } from '../services/firebase.service';
import { Router, Params } from '@angular/router';

/**
 * @Settings Card
 */
@Component({
  selector: 'app-settigns-card',
  templateUrl: 'Settings.html',
  styleUrls: ['Settings.css'],
})

export class Settings {
  settings: Array<any>;
  daily = 0;
  weekly = 0;
  isVisible = false;

  @Output() isVisibleEvent = new EventEmitter<boolean>();

  constructor(
    public firebaseService: FirebaseService,
    private router: Router
  ) { }

  /**
   * This is called when the page is loaded
   */
  ngOnInit() {
    this.getSettings();
  }

  /**
   * gets the settings that determine the weekly and daily goals
   */
  getSettings() {
    this.firebaseService.getSettings().subscribe(result => {
      this.settings = result;
      for (const item of this.settings) {
        this.daily = Math.floor(item.payload.doc.data().Daily)
        this.weekly = Math.floor(item.payload.doc.data().Weekly)
      }
    })
  }

  easyPreset(){
    this.daily = 30;
    this.weekly = 90;
  }

  medPreset(){
    this.daily = 60;
    this.weekly = 150;
  }

  hardPreset(){
    this.daily = 90;
    this.weekly = 240;
  }

  formatLabel(value: number) {
    return value + 'm';
  }

  updateDB(){
    this.firebaseService.updateSettings(this.weekly, this.daily);
  }

  closeWindow(){
    this.isVisible = false;
    this.isVisibleEvent.emit(this.isVisible)
  }

  @Output() valueChange;
  onChangeDaily(data) {
    this.daily = data;
  }
  onChangeWeek(data){
    this.weekly = data;
  }
}

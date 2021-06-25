/**
 * Settings.ts
 * style - Settings.css
 * html - Settings.html
 * Author: Lewis Mckaig
 * Date: April 2021
 *
 * Description: settigns card which can change different settings for the app and device.
 *
 *
 */
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
  sensitivity = 0;
  isVisible = false;

  @Output() isVisibleEvent = new EventEmitter<boolean>();

  constructor(
    public firebaseService: FirebaseService,
    private router: Router
  ) { }

  /**
   * runs getSettings() when page is loaded
   */
  ngOnInit() {
    this.getSettings();
  }

  /**
   * gets the settings and gives the variables teh values.
   * values are then used to set the values of the sliders on the page
   */
  getSettings() {
    this.firebaseService.getSettings().subscribe(result => {
      this.settings = result;
      for (const item of this.settings) {
        this.daily = Math.floor(item.payload.doc.data().Daily)
        this.weekly = Math.floor(item.payload.doc.data().Weekly)
        this.sensitivity = Math.floor(item.payload.doc.data().Sensitivity)
      }
    })
  }

  /**
   * when easy pressed, this runs. Sets the values to an "easy" preset
   * will update the slider values on the card
   */
  easyPreset(){
    this.daily = 30;
    this.weekly = 90;
  }

  /**
   * when easy pressed, this runs. Sets the values to a "medium" preset
   * will update the slider values on the card
   */
  medPreset(){
    this.daily = 60;
    this.weekly = 150;
  }

  /**
   * when easy pressed, this runs. Sets the values to a "hard" preset
   * will update the slider values on the card
   */
  hardPreset(){
    this.daily = 90;
    this.weekly = 240;
  }

  /**
   * used for displaying the current value the slider is on while it is being dragged
   * @param value : value of the slider
   */
  formatLabel(value: number) {
    return value;
  }

  /**
   * run when save button is pressed
   * saves the values curerntly set on the settings card to the db
   */
  updateDB(){
    this.firebaseService.updateSettings(this.weekly, this.daily, this.sensitivity);
  }

  /**
   * sends the value of isVisible to its parent component which will close the card
   */
  closeWindow(){
    this.isVisible = false;
    this.isVisibleEvent.emit(this.isVisible)
  }

  /**
   * these are run when the sliders are moved, one for each slider
   * changes the value of the variable to the value the slider is on
   */
  @Output() valueChange;
  onChangeDaily(data) {
    this.daily = data;
  }
  onChangeWeek(data){
    this.weekly = data;
  }
  onChangeSens(data){
    this.sensitivity = data;
  }
}

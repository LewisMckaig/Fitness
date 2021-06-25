/**
 * firebaseService.ts
 *
 * Author: Lewis Mckaig
 * Date: April 2021
 *
 * Description: Controller for firebase db
 *
 *
 */
import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/firestore';

@Injectable({
  providedIn: 'root'
})

export class FirebaseService {
 constructor(public db: AngularFirestore) {}


/**
 * Get's the newest readng from the database.
 */
 getReadings() {
   return this.db.collection('Device' , ref => ref.orderBy('Date').limitToLast(1)).snapshotChanges();
  }

/**
 * Gets the last 7 records from the database, should be the current week but can vary if the database is missing days in between
 * used in: small card
 */
 getWeek() {
   return this.db.collection('Device' , ref => ref.orderBy('Date').limitToLast(7)).snapshotChanges();
 }

 /**
  * Gets the settings for use in the settings card
  */
 getSettings() {
   return this.db.collection('Settings').snapshotChanges();
 }

 getGoals(daily) {
   return this.db.collection('Device', ref => ref.where('Activity', '>=', daily)).snapshotChanges();
 }

 /**
  * 
  * @param weekly Determines the weekly goal, used in the main card and goal cards
  * @param daily Determines the daily goal, used in the main card and goal cards
  * @param sens :used when the device is recording, determies how easy it is to pass the threshold to be considered movement
  *
  * recieves 3 values to be inserted into the db.
  */
 updateSettings(weekly: number, daily: number, sens: number) {
   this.db.collection('Settings').doc('Goals').update({Daily: daily})
   this.db.collection('Settings').doc('Goals').update({Weekly: weekly})
   this.db.collection('Settings').doc('Goals').update({Sensitivity: sens})
 }

 /**
  * 
  * @param state State of the device - recording/not recording
  *
  * saves the boolean value sent to it and saves to the db
  */
 changeRecordingState(state: boolean){
    this.db.collection('Settings').doc('Goals').update({Recording: state})
 }
}

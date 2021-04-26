import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/firestore';

@Injectable({
  providedIn: 'root'
})

/**
 * this is the controller for the Firebase DB. It contains all DB interactions that are needed.
 */
export class FirebaseService {
 constructor(public db: AngularFirestore) {}


/**
 * Get's the newest readng from the database, should be the current day's actvity depending on whether or not an
 * entry is in the database for that day
 */
 getReadings() {
   return this.db.collection('Device' , ref => ref.orderBy('Date').limitToLast(1)).snapshotChanges();
  }

/**
 * Gets the last 7 records from the database, should be the current week but can vary if the database is missing days in between
 */
 getWeek() {
   return this.db.collection('Device' , ref => ref.orderBy('Date').limitToLast(7)).snapshotChanges();
 }

 getSettings() {
   return this.db.collection('Settings').snapshotChanges();
 }

 updateSettings(weekly: number, daily: number){
   this.db.collection('Settings').doc('Goals').update({Daily: daily})
   this.db.collection('Settings').doc('Goals').update({Weekly: weekly})
 }

 changeRecordingState(state: boolean){
    this.db.collection('Settings').doc('Goals').update({Recording: state})
 }
}

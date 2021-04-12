import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/firestore';

@Injectable({
  providedIn: 'root'
})

export class FirebaseService {
 constructor(public db: AngularFirestore) {}



 getReadings(){
   return this.db.collection('Device' ,ref => ref.orderBy("Date").limitToLast(1)).snapshotChanges();
 }
}
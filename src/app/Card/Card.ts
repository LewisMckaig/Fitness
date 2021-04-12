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

    constructor(
    public firebaseService: FirebaseService,
    private router: Router
  ) { }

  ngOnInit(){
    this.getData();
  }

  getData(){
    this.firebaseService.getReadings().subscribe(result => {
      this.items = result;
    })
  }
}
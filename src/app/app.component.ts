/**
 * AppComponent.ts
 * style - app.component.css
 * html - app.component.html
 * Author: Lewis Mckaig
 * Date: April 2021
 *
 * Description: main page where all other compnents are displayed on.
 *
 */
import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent{
  title = 'Fitness';

  @Input() isVisible: boolean;


}


/**
 * where all the modules are imported for use in the application including cards, firebase etc
 */
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import {ToolbarBasic} from './toolbar-basic';
import {Card} from './Card/Card';
import {DemoMaterialModule} from './material.module'; // material module, used for many of the elements
import { cardSm } from './smallCard/Card';
import { Footer } from './Footer/Footer';
import { AngularFireModule } from '@angular/fire';
import { AngularFirestoreModule } from '@angular/fire/firestore';
import { environment } from '../environments/environment';
import { RouterModule } from '@angular/router';
import { rootRouterConfig } from './App.routes';
import { GoalCard } from './smallCard/GoalCard';
import { Settings } from './settingsCard/Settings';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    ToolbarBasic,
    Card,
    cardSm,
    Footer,
    GoalCard,
    Settings
  ],
  imports: [
    BrowserModule,
    NoopAnimationsModule,
    DemoMaterialModule,
    AngularFireModule.initializeApp(environment.firebase),
    AngularFirestoreModule,
    RouterModule.forRoot(rootRouterConfig, {useHash: false}),
    FormsModule,
  ],
  entryComponents: [ToolbarBasic],
  providers: [],
  bootstrap: [AppComponent, ToolbarBasic],
})
export class AppModule { }






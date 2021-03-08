import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import {ToolbarBasic} from './toolbar-basic';
import {Card} from './Card/Card'
import {DemoMaterialModule} from './material.module';
import { cardSm } from './smallCard/Card';

@NgModule({
  declarations: [
    AppComponent,
    ToolbarBasic,
    Card,
    cardSm
  ],
  imports: [
    BrowserModule,
    NoopAnimationsModule,
    DemoMaterialModule
  ],
  entryComponents: [ToolbarBasic],
  providers: [],
  bootstrap: [AppComponent, ToolbarBasic],
})
export class AppModule { }






  import { Routes } from '@angular/router';
import { cardSm } from './smallCard/Card';
import { Card } from './Card/Card';
import { Footer } from './Footer/Footer';

export const rootRouterConfig: Routes = [
  { path: 'cardSm', component: cardSm },
  { path: 'Card', component:  Card},
  { path: 'Footer', component: Footer },]
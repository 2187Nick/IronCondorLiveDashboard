import { Component } from '@angular/core';

import { StrategyComponent } from './component/strategy/strategy.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title(title: any) {
    throw new Error('Method not implemented.');
  }
  strategy1Key = 'condor30_2024-01-04'; // replace with the key for strategy 1
  strategy2Key = 'condor30_2024-01-04'; // replace with the key for strategy 2
  strategy3Key = 'condor30_2024-01-04'; // replace with the key for strategy 3
}
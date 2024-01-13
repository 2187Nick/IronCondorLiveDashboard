import { Component } from '@angular/core';

import { StrategyComponent } from './component/strategy/strategy.component';
import { DataService } from './services/data.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title(title: any) {
    throw new Error('Method not implemented.');
  }

  latestStrategyKey10: string | null = null;
  latestStrategyKey20: string | null = null;
  latestStrategyKey30: string | null = null;

  currentDate = new Date();
  formattedDate = this.getFormattedDate(this.currentDate);
  
  strategy1Key = 'condor_10_' + this.formattedDate;
  strategy2Key = 'condor_20_' + this.formattedDate;
  strategy3Key = 'condor_30_' + this.formattedDate;

  stratDataKey1: string = '';
  stratDataKey2: string = '';
  stratDataKey3: string = '';

  constructor(private dataService: DataService) {
    this.fetchLatestStrategyKeys();
  }

  ngOnInit() {

  }

  fetchLatestStrategyKeys() {
    this.dataService.getLatestStrategyKey("Strategy10").subscribe(key => {
      this.latestStrategyKey10 = key;
      this.stratDataKey1 = this.calculateStratDataKey("_10", this.latestStrategyKey10);
    });

    this.dataService.getLatestStrategyKey("Strategy20").subscribe(key => {
      this.latestStrategyKey20 = key;
      this.stratDataKey2 = this.calculateStratDataKey("_20", this.latestStrategyKey20);
    });

    this.dataService.getLatestStrategyKey("Strategy30").subscribe(key => {
      this.latestStrategyKey30 = key;
      this.stratDataKey3 = this.calculateStratDataKey("_30", this.latestStrategyKey30);
    });
  }

  getFormattedDate(date: Date): string {
    return `${date.getFullYear()}-${('0' + (date.getMonth() + 1)).slice(-2)}-${('0' + date.getDate()).slice(-2)}`;
  }

  calculateStratDataKey(suffix: string, latestKey: string | null): string {
    const currentTime = new Date();
    const estTime = new Date(currentTime.toLocaleString("en-US", {timeZone: "America/New_York"}));
    const cutoffTime = new Date(estTime);
    cutoffTime.setHours(16, 5, 0, 0); // Set to 4:05 PM EST

    if (estTime <= cutoffTime && latestKey) {
      // It's before 4:05 PM EST, use the latest key
      return latestKey;
    } else {
       // It's after 4:05 PM EST, use today's date
       return this.formattedDate + suffix;
    }
  }
}
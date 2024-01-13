import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(private http: HttpClient) {}

  getDataByKey(key: string): Observable<any> {
    return this.http.get(environment.apiUrl).pipe(
      map((response: any) => {
        if (response.data && response.data.items) {
          console.log("Data Items:", response.data.items); // Log the items array

          // Iterate through the items array and find the item with the matching key
          const foundItem = response.data.items.find((i: any) => i.key === key);
          return foundItem ? foundItem : null;
        }
        return null;
      })
    );
  }

  getStrategyDataByKey(key: string): Observable<any> {
    return this.http.get(environment.apiUrl).pipe(
      map((response: any) => {
        // Check if the response has 'strategies' and 'items' array
        if (response.strategies && response.strategies.items) {
          console.log("Strategy Items:", response.strategies.items); // Log the items array
          // Find the item in the 'items' array with the matching key
          const item = response.strategies.items.find((i: any) => i.key === key);
          // Return the item if found, or null if not found
          return item ? item : null;
        }
        return null;
      })
    );
  }

  getLatestStrategyKey(strategyId: string): Observable<string | null> {
    return this.http.get(environment.apiUrl).pipe(
      map((response: any) => {
        if (response.strategies && response.strategies.items) {
          const strategyItems = response.strategies.items.filter((item: any) => item.STRATEGY_ID === strategyId);

          if (strategyItems.length === 0) {
            return null; // No items found for the strategy
          }

          // Sort by DATE in descending order and get the latest item
          strategyItems.sort((a: any, b: any) => new Date(b.DATE).getTime() - new Date(a.DATE).getTime());
          return strategyItems[0].key; // Return the key of the latest item
        }
        return null;
      })
    );
  }
 
  getStrategyDataByStrat(strategy: string): Observable<any[]> {
    return this.http.get(environment.apiUrl).pipe(
      map((response: any) => {
        if (response.strategies && response.strategies.items) {
          return response.strategies.items.filter((item: any) => item.STRATEGY_ID === strategy);
        }
        return [];
      })
    );
  } 

}
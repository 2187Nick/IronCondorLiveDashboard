import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(private http: HttpClient) {}

  getDataByKey(key: string) {
    /* return this.http.get('http://localhost:4201').pipe( */
    return this.http.get('https://condor_api_node-1-y4339637.deta.app').pipe(
      map((response: any) => {
        const item = response.items.find((item: any) => item.key === key);
        return item ? item.value : null;
      })
    );
  }
}
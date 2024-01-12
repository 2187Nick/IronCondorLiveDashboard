/* import { Component } from '@angular/core';

@Component({
  selector: 'app-strategy',
  templateUrl: './strategy.component.html',
  styleUrls: ['./strategy.component.css']
})
export class StrategyComponent {

} */

import { Component, Input, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-strategy',
  templateUrl: './strategy.component.html', // use templateUrl instead of template
  styleUrls: ['./strategy.component.css']
})
export class StrategyComponent implements OnInit {

  // 2 different was to handle the typescript issue. Decide which to use
  // The error message is indicating that the `key` property in your `StrategyComponent` class is declared but not initialized in the constructor. This is a TypeScript error that occurs when the `strictPropertyInitialization` compiler option is enabled in your `tsconfig.json` file.
  //However, in Angular, `@Input()` properties are usually initialized by the parent component, not in the constructor. So, you have a few options to fix this error:

  //@Input() key!: string;
  // The key is passed in from the parent component
  @Input() key: string = 'defaultKey';
  data: any;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.dataService.getDataByKey(this.key).subscribe(data => {
      this.data = data;
      console.log(this.data);
      // Update the graph
    });
  }

  public graph1 = {
    data: [
      { 
        y: [10000, 10200, 10500, 11000, 12000, 12300, 12800, 13000, 13800, 14500, 15000, 15500], 
        x: ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01', '2022-06-01', '2022-07-01', '2022-08-01', '2022-09-01', '2022-10-01'], 
        type: 'line', 
        mode: 'lines+points', 
        marker: {color: 'green'}, 
        name: 'Line Plot0' // Add a name for the trace
      },
    ],
    layout: {
      paper_bgcolor: 'black',
      plot_bgcolor: 'black',
      font: {
        color: 'green'
      },
      // Going to handle the width and height in the css file
      /* width: 640, 
      height: 480,  */
      title: '$10 Wide Strategy',
      xaxis: {
        title: 'Date',
        gridcolor: 'rgba(255, 255, 255, 0.1)',
      }, // Add a label for the x axis
      yaxis: {
        title: 'Profit $',
        gridcolor: 'rgba(255, 255, 255, 0.1)'
      }, // Add a label for the y axis
      legend: {x: 1, y: 1} // Move the legend to the top right corner
    }
  };
}

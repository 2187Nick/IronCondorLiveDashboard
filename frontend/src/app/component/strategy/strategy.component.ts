import { Component, Input, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-strategy',
  templateUrl: './strategy.component.html',
  styleUrls: ['./strategy.component.css']
})
export class StrategyComponent implements OnInit {
  //@Input() key!: string;
  // The key is passed in from the parent component
  @Input() key: string = 'defaultKey';
  @Input() strat_key: string = 'defaultKey';
  data: any;
  strat_data: any;
  strategy_data: any;
  graph1: any;

  constructor(private dataService: DataService) {}

  ngOnInit() {

    const strategyId = this.extractStrategyId(this.strat_key);
    if (strategyId) {
      this.dataService.getStrategyDataByStrat(strategyId).subscribe({
        next: strategyItems => {
          if (strategyItems && strategyItems.length > 0) {
            this.strategy_data = strategyItems;
            this.graph1 = this.createGraph1(strategyItems);
          } else {
            console.log('No data found for the strategy:', strategyId);
          }
        },
        error: error => {
          console.error('An error occurred while fetching data:', error);
        }
      });
    } else {
      console.log('Invalid strategy key:', this.strat_key);
    }

    
    this.dataService.getDataByKey(this.key).subscribe({
      next: data => {
        if (data) {
          this.data = data;
          //console.log(this.data);
          // Update the graph
        } else {
          console.log('No data found for the key:', this.key);
        }
      },
      error: error => {
        console.error('An error occurred while fetching data:', error);
        // Handle the error here
      }
    });

    this.dataService.getStrategyDataByKey(this.strat_key).subscribe({
      next: strat_data => {
        if (strat_data) {
          this.strat_data = strat_data;
          //console.log(this.strat_data);
          // Update the graph
        } else {
          console.log('No data found for the strat key:', this.strat_key);
        }
      },
      error: error => {
        console.error('An error occurred while fetching data:', error);
        // Handle the error here
      }
    });

  }

  extractStrategyId(strat_key: string): string {
    const parts = strat_key.split('_');
    return parts.length > 1 ? 'Strategy' + parts[1] : '';
  }

  
  createGraph1(strategyData: any[]) {
    //console.log("strategyData: ", strategyData)
    const xValues = strategyData.map(item => item.DATE);
    const yValues = strategyData.map(item => parseFloat((item.CURRENT_BALANCE / 1000).toFixed(2)));
  
    return {
      data: [
        { 
          x: xValues,
          y: yValues,
          type: 'line', 
          mode: 'lines+points', 
          marker: {color: 'green'}, 
          name: 'Balance Over Time'
        },
      ],
      layout: {
        paper_bgcolor: 'black',
        plot_bgcolor: 'black',
        font: {
          color: 'green'
        },
        title: {
          text: "$" + parseInt(strategyData[0].STRATEGY_ID.replace('Strategy', '')) + ' Wide Strategy',
          font: {
            family: 'bold',
            size: 24,
            color: 'green',
            weight: 'bold',

          }
        },
        xaxis: {
          title: 'Date',
          gridcolor: 'gray',
          tickformat: '%m-%d',
          tickvals: xValues,
        },
        yaxis: {
          gridcolor: 'gray',
          //tickformat: '.1fk', // Format the y-axis labels as thousands with 1 decimal place
          title: {
            text: 'Balance (K)',
            standoff: 30 // 
          },
        },
        margin: { 
          l: 80,
          r: 50,
          b: 50,
          t: 50,
          pad: 20
        },
        legend: {x: 1, y: 1}
      }
    };
  }
  
}
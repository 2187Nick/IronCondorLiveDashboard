import { Component } from '@angular/core';

/* template: `
<header>
  <h1>Iron Condor Dashboard</h1>
</header>
<plotly-plot [data]="graph1.data" [layout]="graph1.layout"></plotly-plot>
<plotly-plot [data]="graph2.data" [layout]="graph2.layout"></plotly-plot>
<plotly-plot [data]="graph3.data" [layout]="graph3.layout"></plotly-plot>
`, */

@Component({
  selector: 'app-root',
  template: `
  <div class="app-container">
    <header>
      <h1>Iron Condor Dashboard</h1>
    </header>
    <div class="plot-container">
      <plotly-plot [data]="graph1.data" [layout]="graph1.layout"></plotly-plot>
      <plotly-plot [data]="graph2.data" [layout]="graph2.layout"></plotly-plot>
      <plotly-plot [data]="graph3.data" [layout]="graph3.layout"></plotly-plot>
    </div>
    <footer>
      <p>© 2024 2187.io</p>
    </footer>
  </div>
  `,
    styles: [`
  .app-container {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
  header {
    color: white;
    text-align: center;
    width: 100%;
  }
  .plot-container {
    background-color: black;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    width: 100%;
    flex-grow: 1; /* This will make the plot container take up the remaining space */
  }
  footer {
      color: white;
      text-align: center;
      width: 100%;
      height: 40px; /* Adjust based on your footer's content */
  }
  `]
})
export class AppComponent {
  public graph1 = {
    data: [
      { 
        x: [1, 2, 3], 
        y: [2, 6, 3], 
        type: 'line', 
        mode: 'lines+points', 
        marker: {color: 'red'}, 
        name: 'Line Plot0' // Add a name for the trace
      },
    ],
    layout: {
      paper_bgcolor: 'black',
      plot_bgcolor: 'black',
      font: {
        color: 'orange'
      },
      width: 640, 
      height: 480, 
      title: '$10 Wide Strategy',
      xaxis: {title: 'Date'}, // Add a label for the x axis
      yaxis: {title: 'Profit $'}, // Add a label for the y axis
      legend: {x: 1, y: 1} // Move the legend to the top right corner
    }
  };

  public graph2 = {
    data: [
      { 
        x: [1, 2, 3], 
        y: [2, 6, 3], 
        type: 'line', 
        mode: 'lines+points', 
        marker: {color: 'blue'}, 
        name: 'Line Plot' // Add a name for the trace
      },
    ],
    layout: {
      paper_bgcolor: 'black',
      plot_bgcolor: 'black',
      font: {
        color: 'green'
      },
      width: 640, 
      height: 480, 
      title: '$20 Wide Strategy',
      xaxis: {title: 'Date'}, // Add a label for the x axis
      yaxis: {title: 'Profit $'}, // Add a label for the y axis
      legend: {x: 1, y: 1} // Move the legend to the top right corner
    }
  };

  public graph3 = {
    data: [
      { 
        x: [1, 2, 3], 
        y: [2, 5, 3], 
        type: 'bar', 
        marker: {color: 'orange'}, // Change the color of the bars
        name: 'Bar Only Chart' // Add a name for the trace
      },
    ],
    layout: {
      paper_bgcolor: 'black',
      plot_bgcolor: 'black',
      font: {
        color: 'blue'
      },
      width: 640, 
      height: 480, 
      title: '$30 Wide Strategy',
      xaxis: {title: 'Date'}, // Add a label for the x axis
      yaxis: {title: 'Profit $'}, // Add a label for the y axis
      legend: {x: 1, y: 1} // Move the legend to the top right corner
    }
  };
}


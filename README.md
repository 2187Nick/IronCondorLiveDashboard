# IronCondorLiveDashboard

<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/2187Nick/IronCondorLiveDashboard">
    <img src="images/2187logo.png" alt="Logo" width="120" height="120">
  </a>

  <h3 align="center">Dashboard to Monitor 0dte Option Selling Strategies</h3>

  <p align="center">
    3 Iron Condor Strategies. $10, $20, and $30 Wings.
    <br />
    <a href="https://github.com/2187Nick/IronCondorLiveDashboard"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/2187Nick/IronCondorLiveDashboard">View Demo</a>
    ·
    <a href="https://github.com/2187Nick/IronCondorLiveDashboard">Report Bug</a>
    ·
    <a href="https://github.com/2187Nick/IronCondorLiveDashboard">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
       <ul>
        <li><a href="#iron-condors-explained">Iron Condors Explained</a></li>
      </ul>
       <ul>
        <li><a href="#strategy">Strategy</a></li>
      </ul>
    </li>
    <li>
      <a href="#road-map">Roadmap</a>
      <ul>
        <li><a href="#design">Design</a></li>
        <li><a href="#prototype">Prototype</a></li>
        <li><a href="#deploy">Deploy</a></li>
      </ul>
    </li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#prerequisites">Prerequesites</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![IC_idea](https://github.com/2187Nick/IronCondorLiveDashboard/assets/75052782/4f2a385a-23a2-4bfe-af6d-f98730fee755)


### The goal with this project is to design, build, monitor and eventually go live with an automated strategy.

Key Unknowns:
* Can a strategy work without human intervention?
* Which exit strategy works best for different Condors?
* How to automate TDA API to exit the trade in chaotic conditions?


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Iron Condors Explained
![icprofitloss](https://github.com/2187Nick/IronCondorLiveDashboard/assets/75052782/0683370a-b746-4684-bf76-d0bf55204948)



<!-- USAGE EXAMPLES -->
## Strategy

1. Sell both wings at the open. 1% above and below the opening price.
     ```sh
      $10 Wing Strategy Example with SPX open price of 4500:
          Left Wing:
          * Sell 4455 Put @ .50
          * Buy  4435 Put @ .40
          Credit = $10
  
          Right Wing:
          * Sell 4545 Call @ .50
          * Buy  4555 Call @ .40
          Credit = $10
  
          Total Credit = $20
      
     ```
3. Set a stop loss for both wings at 5x the credit received.
     ```sh
      $10 Wing Exit Strategy Example with SPX open price of 4500
  
          Stop Loss = Total Credit x 5
          Stop Loss = $100
     
          Left Wing:
          * Buy   4455 Put
          * Sell  4435 Put
          Exit @ Spread Value of 1.00
  
          Right Wing:
          * Buy   4545 Call
          * Sell  4555 Call
          Exit @ Spread Value of 1.00
  
          
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
### Road Map

Preparation:
  - [X] Create Repo with README
  - [X] Fill out Roadmap

Design:
  - [ ] Create low-fidelity wireframe
  - [X] Add basic logic of the strategy

Prototype:
  - [ ] Build Front-End structure in Angular
  - [ ] Setup API to backend
  - [ ] Build database

Deploy:
  - [ ] Create subdomain on AWS
  - [ ] Upload Front-End to S3 Bucket
  - [ ] Backend API deploy to Deta
  - [ ] Deta database created

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Design
  ```bash


  ```

## Prototype
  ```bash

  
  ```


## Deploy
  ```bash

  
  ```

## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/2187Nick/IronCondorLiveDashboard.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

* [![Angular][Angular.io]][Angular-url]

* 
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Prerequisites

* npm
  ```sh
  npm install npm@latest -g
  ```



<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Your Name - [@2187Nick](https://twitter.com/2187Nick) - nick@2187.io

Project Link: [https://github.com/2187Nick/IronCondorLiveDashboard](https://github.com/2187Nick/IronCondorLiveDashboard)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Notable Resources:

* [Font Awesome](https://fontawesome.com)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/2187Nick/IronCondorLiveDashboard/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/2187Nick/IronCondorLiveDashboard/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/2187Nick/IronCondorLiveDashboard/stargazers
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/

# aim_bi_project

## Project discription
**Dynamic electricity prices - average cost savings for end consumers from 2025**

As part of the law to restart the digitalization of the energy transition (GNDEW), it is clear: from 1 January 2025, all electricity suppliers must offer dynamic electricity tariffs.

This project looks at data from the electricity price exchange from 2023, as well as the average electricity price per kWh for households in Germany. 

### What are dynamic electricity tariffs?
In contrast to fixed electricity prices with a statically fixed price per kilowatt hour, the prices for dynamic electricity tariffs vary according to the situation on the electricity market, specifically the exchange electricity price. 
Dynamic electricity tariffs are among the variable electricity tariffs, but are the most accurate reflection of the electricity tariff. In addition to dynamic electricity tariffs, there are also time-variable electricity tariffs with, for example, day & night electricity prices, as well as load-variable electricity tariffs, which offer favorable electricity prices when the electricity grid is particularly busy (a lot of solar or wind power).

### What is the objective of this project?
To process data from the electricity price exchange and data on fixed electricity prices so that the theoretical average cost savings from the use of dynamic electricity tariffs can be visualized using a suitable visualization.

### How is it implemented technically?
- Flask as a micro web framework 
- Python, in particular panda's DataFrames, in the backend
- Visualization with vue

### Where does the data come from?
- RestAPI call via awattar, hourly electricity prices from the electricity exchange in Paris

### What assumptions are made?
- Dynamic electricity prices have a baseline, i.e. there is always a minimum amount to be paid & negative prices are not possible. 
- As no detailed price compositions have been disclosed in response to inquiries to electricity suppliers, it is assumed that taxes & levies (12.57 cents/kWh) and grid charges (9.52 cents/kWh) form the baseline.
- If the producer price of electricity falls below 0 cents/kWh, 0 cents/kWh is still charged.


## Requirements

- micromamba
- Node.js
- npm

## Usage

- Clone this repo
- Backend:
  - `micromamba create -p ./.venv -f environment.yml`
  - `micromamba activate -p ./.venv`
- Frontend:
  - `npm install`

Activate the venv and run the flask server with `python backend.py`. Then start the frontend by calling `npm run dev`.

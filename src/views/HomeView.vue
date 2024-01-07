<template>
  <div class="max-w-2xl mx-auto mt-8">
    <h2 class="text-2xl font-bold mb-4">Project Description</h2>

    <p class="mb-4"><strong>Dynamic electricity prices - average cost savings for end consumers from 2025</strong></p>

    <p class="mb-4">As part of the law to restart the digitalization of the energy transition (GNDEW), it is clear: <br>
      &nbsp;&nbsp;&nbsp;&rarr; from 1 January 2025, all electricity suppliers must offer dynamic electricity tariffs.</p>

    <p class="mb-4">This project looks at data from the electricity price exchange from 2023, as well as the average
      electricity price per kWh for households in Germany.</p>

    <h3 class="text-xl font-bold mb-2">What are dynamic electricity tariffs?</h3>
    <p class="mb-4">In contrast to fixed electricity prices with a statically fixed price per kilowatt hour, the prices
      for dynamic electricity tariffs vary according to the situation on the electricity market, specifically the exchange
      electricity price. Dynamic electricity tariffs are among the variable electricity tariffs, but are the most accurate
      reflection of the electricity tariff. In addition to dynamic electricity tariffs, there are also time-variable
      electricity tariffs with, for example, day & night electricity prices, as well as load-variable electricity tariffs,
      which offer favorable electricity prices when the electricity grid is particularly busy (a lot of solar or wind
      power).</p>

    <h3 class="text-xl font-bold mb-2">What is the objective of this project?</h3>
    <p class="mb-4">To process data from the electricity price exchange and data on fixed electricity prices so that the
      theoretical average cost savings from the use of dynamic electricity tariffs can be visualized using a suitable
      visualization.</p>

    <h3 class="text-xl font-bold mb-2">How is it implemented technically?</h3>
    <ul class="list-disc pl-6 mb-4">
      <li>Flask as a micro web framework</li>
      <li>Python, in particular panda's DataFrames, in the backend</li>
      <li>Visualization with vue</li>
    </ul>

    <h3 class="text-xl font-bold mb-2">Where does the data come from?</h3>
    <ul class="list-disc pl-6 mb-4">
      <li>RestAPI call via awattar, hourly electricity prices from the electricity exchange in Paris</li>
    </ul>

    <h3 class="text-xl font-bold mb-2">What assumptions are made?</h3>
    <ul class="list-disc pl-6 mb-4">
      <li>Dynamic electricity prices have a baseline, i.e. there is always a minimum amount to be paid & negative prices
        are not possible.</li>
      <li>As no detailed price compositions have been disclosed in response to inquiries to electricity suppliers, it is
        assumed that taxes & levies (12.57 &#162;/kWh) and grid charges (9.52 &#162;/kWh) form the baseline.</li>
      <li>If the producer price of electricity falls below 0 &#162;/kWh, 0 &#162;/kWh is still charged.</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import BarChart from '../components/BarChart.vue';
import LineChart from '../components/LineChart.vue';
import DoughnutChart from '../components/DoughnutChart.vue';

const router = useRouter();

export default {
  name: 'App',
  components: {
    BarChart, LineChart, DoughnutChart
  },

  data: () => ({
    loaded: false,
    lineChartData: null,
    doughnutChartData: {
      labels: ['Taxes', 'Fees', 'Consumption'],
      datasets: [
        {
          backgroundColor: ['#41B883', '#E46651', '#00D8FF'],
          data: [26.8, 20.3, 52.9]
        }
      ]
    },
    lineChartOptions: {
      responsive: true,
      maintainAspectRatio: false,
    },

  }),
}
</script>

<style scoped></style>

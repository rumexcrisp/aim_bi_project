<template>
  <div class="flex p-4">
    <div class="flex-1 h-64 flex flex-col justify-center items-center">
      <DoughnutChart id="line" :chartOptions="lineChartOptions" :chartData="doughnutChartData">Chart couldn't be loaded.</DoughnutChart>
    </div>
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

<template>
  <div class="flex items-center justify-center h-screen">
    <div v-if="!error">
      <div class="flex p-4">
        <div class="flex-1 h-64 flex flex-col justify-center items-center">
          <LineChart v-if="loaded" id="line" :chartOptions="lineChartOptions" :chartData="lineChartData">Chart couldn't be loaded.</LineChart>
          <div v-else>Loading Line Chart...</div>
        </div>
      </div>
      <div class="flex p-4">
        <div class="flex-1 h-64 flex flex-col justify-center items-center">
          <DoughnutChart v-if="loaded" id="doughnut1" :chartData="doughnutChartData">Chart couldn't be loaded.</DoughnutChart>
          <div v-else>Loading Doughnut Chart 1...</div>
        </div>
        <div class="flex-1 h-64 flex flex-col justify-center items-center">
          <DoughnutChart v-if="loaded" id="doughnut2" :chartData="doughnutChartData">Chart couldn't be loaded.</DoughnutChart>
          <div v-else>Loading Doughnut Chart 2...</div>
        </div>
      </div>
    </div>
    <div v-else class="text-red-500">{{ error }}</div>
  </div>
</template>

<script lang="ts">
import { ref } from "vue";
import axios, { AxiosResponse } from "axios";
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
    error: false,
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
      scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Date'
            },
            ticks: {
              major: {
                enabled: true
              },
              color: '#000000',
            }
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Cent/kWh'
            }
          }
        }
    },

  }),

  mounted() {
    this.loaded = false;
    this.fetchData();
  },

  methods: {
    async fetchData() {
      try {
        const response: AxiosResponse = await axios.get('http://127.0.0.1:5000/api/get_data', {
          timeout: 5000, // Set timeout to 5 seconds (adjust as needed)
        });
        this.processData(response.data);
        this.loaded = true;
      } catch (error) {
        console.error('Error fetching data:', error);
        this.error = "Error fetching data. Please check backend."
      }
    },
    processData(data) {
      // Process the data if needed
      // You might want to format timestamps, convert types, etc.
      this.lineChartData = {
        labels: data.map(entry => entry.date),
        datasets: [
          {
            label: 'Market Price',
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            data: data.map(entry => entry.marketprice),
          },
        ],
      };
    },
  }
}
</script>

<style scoped></style>

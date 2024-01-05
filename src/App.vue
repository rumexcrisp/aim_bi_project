<template>
  <h1>Business Intelligence Project</h1>
  <div class="container">
    <BarChart v-if="loaded" id="line" :options="chartOptions" :data="chartData">Chart couldn't be loaded.</BarChart>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import BarChart from './components/BarChart.vue';
import LineChart from './components/LineChart.vue';

export default {
  name: 'App',
  components: {
    BarChart, LineChart
  },

  data: () => ({
    loaded: false,
    chartData: null,
    chartOptions: null
  }),

  mounted() {
    this.loaded = false;
    this.fetchData();
  },

  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/get_data');
        console.log(response);
        this.processData(response.data);
        this.loaded = true;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    processData(data) {
      // Process the data if needed
      // You might want to format timestamps, convert types, etc.
      this.chartData = {
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
      this.chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
      };
    }
  }
}
</script>
<template>
  <h1>Business Intelligence Vue Project</h1>
  <div>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement
} from 'chart.js'
import { Line, Bar, Doughnut } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'App',
  components: {
    Line, Bar, Doughnut
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Market Price',
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            data: [],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://localhost:5000/api/get_data');
        console.log(response);
        this.processData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    processData(data) {
      // Process the data if needed
      // You might want to format timestamps, convert types, etc.
      this.chartData = {
        labels: data.map(entry => entry.start_timestamp),
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
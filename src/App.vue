<template>
  <div>
    <Line :data="lineChartData" :options="options" />
  </div>
  <div>
    <Bar :data="barChartData" :options="options" />
  </div>
  <div>
    <Doughnut :data="doughnutChartData" :options="options" />
  </div>
</template>

<script lang="ts">
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
import * as chartConfig from './config/chartConfig.js'
import * as doughnutchartConfig from './config/doughnutchartConfig.js'

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
      lineChartData: chartConfig.data,
      barChartData: chartConfig.data,
      doughnutChartData: doughnutchartConfig.data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    };
  }
}
</script>
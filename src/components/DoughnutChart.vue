<template>
    <Doughnut id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>

<script lang="ts">
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

export default {
    name: 'BarChart',
    components: { Doughnut },
    props: {
        chartData: {
            type: Object,
            required: true
        },
        chartOptions: {
            type: Object,
            default: () => ({
                responsive: true,
            })
        }
    }
}
</script>
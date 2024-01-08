<template>
  <div class="flex justify-center h-screen">
    <div v-if="!error">
      <!-- Datepickers -->
      <div class="flex flew-row justify-center p-4 mb-4">
        <div class="mx-2">
          <Datepicker
            v-model="datepick"
            :preview-format="dateFormat"
            range
            auto-apply
            class="border rounded"
          />
        </div>
        <button @click="fetchData" class="bg-blue-500 text-white rounded px-2 py-1 ml-2">Fetch Data</button>
      </div>

      <!-- Charts -->
      <div class="flex p-4">
        <div class="flex-1 h-64 flex flex-col justify-center items-center">
          <template v-if="loaded && lineChartData">
            <LineChart :chartOptions="lineChartOptions" :chartData="lineChartData"></LineChart>
          </template>
          <div v-else>Loading Line Chart...</div>
        </div>
      </div>
      <div class="flex p-4">
        <div class="flex-1 h-64 flex flex-col justify-center items-center">
          <template v-if="loaded">
            <DoughnutChart id="doughnut1" :chartData="doughnutChartData1"></DoughnutChart>
          </template>
          <div v-else>Loading Doughnut Chart 1...</div>
        </div>
        <div class="flex-1 h-64 flex flex-col justify-center items-center">
          <template v-if="loaded">
            <DoughnutChart id="doughnut2" :chartData="doughnutChartData2"></DoughnutChart>
          </template>
          <div v-else>Loading Doughnut Chart 2...</div>
        </div>
      </div>
    </div>
    <div v-else class="text-red-500">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios, { AxiosResponse } from 'axios';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import LineChart from '../components/LineChart.vue';
import DoughnutChart from '../components/DoughnutChart.vue';

interface ChartData {
  date: string;
  marketprice: number;
  avg_marketprice: number;
}

interface PieData {
  dyn_consumer_price_sample: number;
}

const startDate = ref(new Date(2019, 0, 1));
const endDate = ref(new Date(2019, 0, 31));
const datepick = ref([startDate.value, endDate.value]);
// const datepick = ref();
// datepick.value = [startDate, endDate];
const dateFormat = (datepick: Date | null): string => {
  if (datepick instanceof Date) {
    const day = datepick.getDate();
    const month = datepick.getMonth() + 1;
    const year = datepick.getFullYear();
    return `${day}/${month}/${year}`;
  }
  return ''; // Return an empty string or another default value if date is not valid
}

const loaded = ref(false);
const error = ref<string | boolean>(false);
const startTime = ref({ hours: 0, minutes: 0 });

const lineChartData = ref<any>(null);
const doughnutChartData1 = {
  labels: ['Taxes', 'Fees', 'Consumption'],
  datasets: [
    {
      backgroundColor: ['#41B883', '#E46651', '#00D8FF'],
      data: [26.8, 20.3, 52.9],
    },
  ],
};
const doughnutChartData2 = ref<any>(null);

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      display: true,
      title: {
        display: true,
        text: 'Date',
      },
      ticks: {
        major: {
          enabled: true,
        },
        color: '#000000',
      },
    },
    y: {
      display: true,
      title: {
        display: true,
        text: 'Cent/kWh',
      },
    },
  },
  tooltip: {
    intersect: false,
  },
  plugins: {
    decimation: {
      enabled: true,
      algorithm: 'min-max'
      // algorithm: 'lttb',
    }
  },
  indexAxis: 'x',
};

onMounted(() => {
  fetchData();
});

const fetchData = async () => {
  try {
    const startEpoch = datepick.value[0].getTime();
    const endEpoch = datepick.value[1].getTime();

    console.log("start: " + startDate.value + ", end: " + endDate.value);
    console.log("startISO: " + startEpoch + ", endISO: " + endEpoch);

    const lineDateResponse: AxiosResponse = await axios.get('http://127.0.0.1:5000/api/get_line_data', {
      params: {start: startEpoch, end: endEpoch},
      timeout: 5000,
    });
    const responseLineData: ChartData[] = lineDateResponse.data;
    const pieDateResponse: AxiosResponse = await axios.get('http://127.0.0.1:5000/api/get_pie_data', {
      params: {start: startEpoch, end: endEpoch},
      timeout: 5000,
    });
    const responsePieData: PieData[] = pieDateResponse.data;

    console.log(responseLineData);
    console.log(responsePieData);

    processLineData(responseLineData);
    processPieData(responsePieData);
    loaded.value = true;
  } catch (error: any) {
    console.error('Error fetching data:', error);
    error.value = 'Error fetching data. Please check backend.';
  }
};

const processLineData = (data: ChartData[]) => {
  // const mockData: ChartData[] = [
  //   { date: '2022-01-01', marketprice: 10.5, avg_marketprice: 12.0 },
  //   { date: '2022-01-02', marketprice: 11.2, avg_marketprice: 12.0 },
  //   { date: '2022-01-03', marketprice: 12.0, avg_marketprice: 12.0 },
  //   // ... more data
  // ];
  lineChartData.value = {
    labels: data.map((entry) => entry.date),
    datasets: [
      {
        label: 'Market Price',
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        data: data.map((entry) => entry.marketprice),
      },
      {
        label: 'Market Price Average',
        borderColor: 'rgba(160, 0, 192, 1)',
        backgroundColor: 'rgba(160, 0, 192, 0.2)',
        data: data.map((entry) => entry.avg_marketprice),
      },
    ],
  };
};

const processPieData = (data: PieData[]) => {
  doughnutChartData2.value = {
    labels: ['Taxes', 'Fees', 'Consumption'],
    datasets: [
    {
      backgroundColor: ['#41B883', '#E46651', '#00D8FF'],
      data: [12.57, 9.52, data],
    },
  ],
  };
};
</script>

<style scoped></style>

<template>
  <div>
    <h1>Data Table Example</h1>
    <data-table :columns="columns" :data="tableData" />
  </div>
</template>

<script>
import axios from 'axios';
import DataTable from './DataTable.vue';

export default {
  components: {
    DataTable,
  },
  data() {
    return {
      columns: [],
      tableData: [],
    };
  },
  mounted() {
    axios.get('http://localhost:5000/api/get_data')
      .then(response => {
        this.columns = 0;
        this.tableData = response.data;
        if (response.data.length > 0) {
          // Use the keys of the first item as columns
          this.columns = Object.keys(response.data[0]);
        }
        console.log('response:', response.data);
        console.log('Columns:', this.columns);
        console.log('Table Data:', this.tableData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  },
};
</script>

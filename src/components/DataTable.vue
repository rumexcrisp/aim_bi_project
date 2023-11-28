<template>
    <div v-if="data.length > 0">
        <table>
            <thead>
                <tr>
                    <th v-for="(item, columnIndex) in data[0]" :key="columnIndex">{{ columnIndex }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(rowData, rowIndex) in data" :key="rowIndex">
                    <td v-for="(value, columnName) in rowData" :key="columnName">{{ value }}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div v-else>
        No data available.
    </div>
</template>
  
  
<script>
export default {
    props: {
        columns: {
            type: Array,
            required: true,
        },
        data: {
            type: Array,
            required: true,
        },
    },
    mounted() {
        console.log('Columns in DataTable component:', this.columns);
        console.log('Data in DataTable component:', this.data);
    },
};
</script>
  
<style scoped>
/* Your component-specific styles go here */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th,
td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    color: black;
    background-color: #f2f2f2;
}
</style>
  
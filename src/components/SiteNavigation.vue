<template>
  <header class="sticky top-0 bg-white shadow-lg">
    <nav class="container flex flex-col sm:flex-row items-center gap-4 text-black py-6">
      <RouterLink :to="{ name: 'home' }">
        <div class="flex items-center gap-3">
          <i class="fa-solid fa-bolt text-2xl"></i>
          <p class="text-2xl">BI Stromkosten Project</p>
        </div>
      </RouterLink>

      <RouterLink :to="{ name: 'data' }">
        <div class="flex items-center gap-3">
          <i class="fa-solid fa-chart-simple text-2xl"></i>
          <p class="text-2xl">Data</p>
        </div>
      </RouterLink>

      <div class="flex gap-3 flex-1 justify-end">
        <i class="fa-solid fa-circle-info text-xl hover:text-yellow-300 duration-150 cursor-pointer"
          @click="toggleModal"></i>
      </div>

      <BaseModal :modalActive="modalActive" @close-modal="toggleModal">
        <div class="text-black">
          <h1 class="text-3xl mb-2">Composition of electricity prices</h1>
          
          <h2 class="text-2xl">Fix compositon of eletricity prices</h2>
          <p class="mb-4">
          <p>The <strong>average fixed composition</strong> of electricity prices of 2023, according the "Strom-Report"
            from BNetzA and BDEW, is separated into the following parts:</p>
          <ul class="list-disc pl-6">
            <li>Energy Consumption: 52.9 %</li>
            <li>Taxes and Charges: 26.8 %</li>
            <li>Grid Fees: 20.3 %</li>
          </ul>
          </p>
          
          <h2 class="text-2xl">Dynamic composition of electicity prices</h2>
          <p class="mb-4">
            Due to our investigations on the detailed composition of electricity prices, there is no exact definition what
            the end consumer really pays.
          </p>

          <h2 class="text-2xl">Baseline assumption</h2>
          <p class="mb-4">
          <p>For the calculation of the <i>real-world prices</i> for the <strong>dynamic composition</strong> of eletricity prices, the following assumptions are made:</p>
          <ul class="list-disc pl-6">
            <li>Energy Consumption: marketprice from awattar</li>
            <li>Taxes and Charges: 12.57 Cent/kWh</li>
            <li>Grid Fees: 9.52 Cent/kWh</li>
          </ul>
          <p>Therefore, grid charges and taxes build a <strong>baseline</strong> which must be payed.</p>
          </p>

          <h3 class="text-2xl">Fix baseline</h3>
          <p class="mb-4">
          <p>With the fix baseline approach, the minimum marketprice fot the customers is <strong>0 Cent/kWH</strong>. Therefore, the minimum consumer price is always the sum of "Taxes and Charges" and "Grid Fees".</p>
          </p>
        </div>
      </BaseModal>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRoute, useRouter } from "vue-router";
import { uid } from "uid";
import { ref } from "vue";
import BaseModal from "./BaseModal.vue";

const savedCities = ref([]);
const route = useRoute();
const router = useRouter();
const addCity = () => {
  if (localStorage.getItem("savedCities")) {
    savedCities.value = JSON.parse(
      localStorage.getItem("savedCities")
    );
  }

  const locationObj = {
    id: uid(),
    state: route.params.state,
    city: route.params.city,
    coords: {
      lat: route.query.lat,
      lng: route.query.lng,
    },
  };

  savedCities.value.push(locationObj);
  localStorage.setItem(
    "savedCities",
    JSON.stringify(savedCities.value)
  );

  let query = Object.assign({}, route.query);
  delete query.preview;
  query.id = locationObj.id;
  router.replace({ query });
};

const modalActive = ref(null);
const toggleModal = () => {
  modalActive.value = !modalActive.value;
};
</script>

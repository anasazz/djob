<template>
    <div class="grid md:grid-cols-4 gap-3 py-5 px-1">
      <!-- Sidebar -->
       
      <div class="md:col-span-1 px-4 py-6 bg-white border shadow-sm rounded-xl">
        <!-- Search Input -->
        
        <!-- <p>filter params : {{ query }} {{ queryRef }}</p>
        <p>categories params : {{ query }} {{ queryRef }}</p>
   -->


<!-- <p class="py-4">Estimation: </p> -->

   <!-- <div class="p-5 ">
    
    <price-range-slider 
    :trackHeight="0.5"
    />
        <hr class="my-6 opacity-30">
  
   </div> -->
<p>Date limite: </p>

<Datepicker v-model="date" />

        <!-- Sectors and Categories -->
        <div class="mt-6 space-y-4">
            <!-- Country Selection -->
    <CountrySelection  />
          <!-- Sectors -->
          <hr class="my-6 opacity-30">

<!-- Include CategoriesSelection component -->
<!-- <CategoriesSelection /> -->
<div>
  <!-- Loop through categories -->
  <div v-for="item in categories" :key="item.id" class="mb-4">
    <!-- Display category name -->
    <p class="text-sm text-red-500">{{ item.name }}</p>
    <!-- Loop through subcategories -->
    <div v-for="cat in item.subcategories" :key="cat.id" class="text-slate-600 text-sm font border-t-1 border rounded-lg px-4 py-2 m-2">
      <label>
        <input type="checkbox" v-model="cat.selected" @change="toggleCategory(cat.id)"> {{ cat.name }}
      </label>
    </div>
  </div>
</div>



  <!-- <p>{{ newdata  }}</p> -->
  
  
  <!-- {{ JSON.stringify(categories , 2 , 2) }} -->




        </div>
      </div>
  
      <!-- Job Listings -->
      <div class="md:col-span-3">
        <div class="flex space-x-3">
          <input v-model="query" type="search" placeholder="Find a job..." class="w-full px-6 py-4 border rounded-xl">
          <button class="px-6 py-4 bg-green-300 text-white rounded-xl" @click="performSearch">
            <!-- Search Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
          </button>
        </div>
        <!-- <p>selectedFilters {{ selectedFilters }}</p> -->
        <p class="py-3" >{{ newdata.total_jobs_count }} jobs </p>
        <div class="space-y-4">
          <Job v-for="job in jobs" :key="job.id" :job="job" />
        </div>
        <!-- <p class="py-3" >{{ JSON.stringify(newdata) }} </p> -->
  
        <div class="flex justify-between mt-8">
  <button @click="prevPage" :class="{ 'bg-green-500 text-white': currentPage > 1 }"
          :disabled="currentPage === 1"
          class="px-4 py-2 bg-gray-200 text-gray-600 rounded-md cursor-pointer">
    Previous
  </button>
  <span class="text-gray-600">Page {{ currentPage }} of {{ totalPages }}</span>
  <button @click="nextPage" :class="{ 'bg-green-500 text-white': currentPage < totalPages }"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 bg-gray-200 text-gray-600 rounded-md cursor-pointer">
    Next
  </button>
</div>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref } from 'vue';
import CountrySelection from '@/components/CountrySelection.vue';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import PriceRangeSlider from '@/components/PriceRangeSlider'



  // Query
  let queryRef = ref('');
  let query = '';
  
  function performSearch() {
    queryRef.value = query;
    fetchJobs();
  }
  
  // Sectors and Categories

  
  let selectedFilters = ref([]);
  
  function toggleCategory(sector, category) {
    const index = selectedFilters.value.findIndex(filter => filter.sector === sector && filter.category === category);
    if (index === -1) {
      selectedFilters.value.push({ sector, category });
    } else {
      selectedFilters.value.splice(index, 1);
    }
    fetchJobs();
  }
  

  
  // Jobs and Pagination
  let currentPage = ref(1);
  let totalPages = ref(1);
  let jobs = ref([]);
  let categories = ref([]);
  let newdata = ref([]);
  let date = ref("");




  
  function fetchJobs() {
    // Simulate API call - Replace with actual API endpoint
    let apiUrl = `http://127.0.0.1:8000/api/v1/jobs/?query=${queryRef.value}&page=${currentPage.value}`;
  
    // Add selected sectors and categories to API call
    if (selectedFilters.value.length > 0) {
      let categoriesQuery = selectedFilters.value.map(filter => encodeURIComponent(filter.sector)).join(',');
      apiUrl += `&categories=${categoriesQuery}`;
    }

    if (date.value) {
      const formattedDate = new Date(date.value).toISOString(); // Format date to ISO string
      
      apiUrl += `&dateLimite=${formattedDate}`;
    }
  
    // Perform fetch
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        
        jobs.value = data.results;
        newdata.value = data
        totalPages.value = data.total_pages
        
      })
      .catch(error => {
        console.error('Error fetching jobs:', error);
      });
  }

  watch(date, (newValue, oldValue) => {
    alert('Date changed:', newValue);
    // Perform any actions you want based on the new value of date
    // Example: Fetch data from backend based on the new date value
    fetchJobs(); // Assuming you have a function to fetch data
  });

  function fetchCategories() {
    // Simulate API call - Replace with actual API endpoint
    let apiUrl = `http://127.0.0.1:8000/api/v1/jobs/categories`;
  
    // Perform fetch
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {

        console.log("data",data);
        
        categories.value = data;
        
      })
      .catch(error => {
        console.error('Error fetching jobs:', error);
      });
  }
  
  // Initial fetch
  fetchJobs();
  fetchCategories();
  
  // Pagination methods
  function nextPage() {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
      fetchJobs();
    } 
  }
  
  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--;
      fetchJobs();
    }
  }
  </script>
  
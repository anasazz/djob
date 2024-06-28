<template>
    <div class="grid md:grid-cols-4 gap-3 py-5 px-1">
      <!-- Sidebar -->
      <div class="md:col-span-1 px-4 py-6 bg-white border shadow-sm rounded-xl">
        <!-- Search Input -->
        <div class="flex space-x-3">
          <input v-model="query" type="search" placeholder="Find a job..." class="w-full px-6 py-4 border rounded-xl">
          <button class="px-6 py-4 bg-slate-300 text-white rounded-xl" @click="performSearch">
            <!-- Search Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
          </button>
        </div>
        <!-- <p>filter params : {{ query }} {{ queryRef }}</p>
        <p>categories params : {{ query }} {{ queryRef }}</p>
   -->
        <hr class="my-6 opacity-30">
  
        <!-- Sectors and Categories -->
        <div class="mt-6 space-y-4">
            <!-- Country Selection -->
    <CountrySelection  />
          <!-- Sectors -->
          <hr class="my-6 opacity-30">

<!-- Include CategoriesSelection component -->
<CategoriesSelection />
        </div>
      </div>
  
      <!-- Job Listings -->
      <div class="md:col-span-3">
        <div class="space-y-4">
          <Job v-for="job in jobs" :key="job.id" :job="job" />
        </div>
  
        <!-- Pagination Controls -->
        <div class="flex justify-between mt-8">
          <button @click="prevPage" :disabled="currentPage === 1" class="px-4 py-2 bg-gray-200 text-gray-600 rounded-md cursor-pointer">Previous</button>
          <span class="text-gray-600">Page {{ currentPage }} of {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages" class="px-4 py-2 bg-gray-200 text-gray-600 rounded-md cursor-pointer">Next</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import CategoriesSelection from '@/components/CategoriesSelection.vue';
import CountrySelection from '@/components/CountrySelection.vue';

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
  
  function isSelected(sector, category) {
    return selectedFilters.value.some(filter => filter.sector === sector && filter.category === category);
  }
  
  // Jobs and Pagination
  let currentPage = ref(1);
  let totalPages = ref(1);
  let jobs = ref([]);
  
  function fetchJobs() {
    // Simulate API call - Replace with actual API endpoint
    let apiUrl = `http://127.0.0.1:8000/api/v1/jobs/?query=${queryRef.value}&page=${currentPage.value}`;
  
    // Add selected sectors and categories to API call
    if (selectedFilters.value.length > 0) {
      let categoriesQuery = selectedFilters.value.map(filter => encodeURIComponent(filter.category)).join(',');
      apiUrl += `&categories=${categoriesQuery}`;
    }
  
    // Perform fetch
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        
        jobs.value = data.results;
        totalPages.value = data.total_pages;
      })
      .catch(error => {
        console.error('Error fetching jobs:', error);
      });
  }
  
  // Initial fetch
  fetchJobs();
  
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
  
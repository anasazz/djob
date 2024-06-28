<template>
    <div class="mt-6">
      <p class="flex items-center text-slate-500 font-semibold mt-4 cursor-pointer" @click="toggleCountry('Morocco')">
        <img src="../assets/flags/flagma.png" alt="Morocco Flag" class="w-6 h-6 mr-2"> Maroc
      </p>
      <!-- <p class="flex items-center text-slate-500 font-semibold mt-4 cursor-pointer" @click="toggleCountry('France')">
        <img src="../assets/flags/fr.png" alt="France Flag" class="w-6 h-6 mr-2"> France
      </p> -->
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // Selected country
  const selectedCountry = ref('');
  
  // Function to toggle country selection
  const toggleCountry = (country) => {
    selectedCountry.value = selectedCountry.value === country ? '' : country;
    // Emit event to parent component or perform any required action
    // fetchJobs(); // Uncomment if you want to trigger job fetching
  };
  
  // Function to check if country is selected
  const isCountrySelected = (country) => {
    return selectedCountry.value === country;
  };
  
  // Export reactive variables and functions
  </script>
  
  <style scoped>
  /* Optional: Add styling for the flags */
  img {
    border-radius: 50%;
    border: 1px solid #ccc;
  }
  </style>
  
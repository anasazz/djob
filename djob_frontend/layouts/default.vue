<template>
    <div>
      <nav class="p-4 px-5 flex items-center justify-between bg-white shadow-md">
        <NuxtLink to="/" class="text-xl text-black">Djob</NuxtLink>
  
        <div class="flex items-center space-x-4">
          <div class="flex md:mt-0 items-center space-x-4">
            <template v-if="userStore.user.isAuthenticated">
              <NuxtLink to="/myjobs" class="py-2 px-6 bg-teal-900 hover:bg-teal-700 text-white rounded-xl">My jobs</NuxtLink>
              <NuxtLink to="/createjob" class="py-2 px-6 bg-teal-600 hover:bg-teal-700 text-white rounded-xl">Create job</NuxtLink>
              <a v-on:click="logout" class="py-2 px-6 bg-rose-600 hover:bg-rose-700 text-white rounded-xl">Log out</a>
            </template>
  
            <template v-else>
              <NuxtLink to="/" class="text-black hover:text-teal-300">Home</NuxtLink>
              <NuxtLink to="/browse" class="text-black hover:text-teal-300">Browse</NuxtLink>
              <NuxtLink to="/login" class="py-4 px-6 bg-teal-900 hover:bg-teal-700 text-white rounded-xl">Log in</NuxtLink>
              <NuxtLink to="/signup" class="py-4 px-6 bg-teal-600 hover:bg-teal-700 text-white rounded-xl">Sign up</NuxtLink>
            </template>
          </div>
        </div>
      </nav>
  
      <div class="flex">
        <!-- Sidebar -->
    <!-- Sidebar -->
<div class="w-1/6 h-screen shadow-lg bg-slate-50 p-4">
  <div class="text-gray-700">
    <h2 class="text-xl font-semibold mb-4">Sidebar</h2>
    <NuxtLink to="/distribution" class="block py-2 px-6 bg-white text-black shadow-md  hover:bg-teal-700 rounded-xl mb-2">My distributions</NuxtLink>
    <NuxtLink to="/employee" class="block py-2 px-6 bg-white text-black shadow-md  hover:bg-teal-700 rounded-xl mb-2">My employees</NuxtLink>
    

    <!-- Example of another sidebar link -->
  </div>
</div>

  
        <!-- Main Content -->
        <div class="w-3/4 p-4">
          <!-- Your slot content will go here -->
          <slot />
        </div>
      </div>
  
      <!-- <footer class="p-6 flex flex-wrap items-center justify-between bg-gray-900">
        <p class="text-gray-300">Copyright (c) 2023 </p>
      </footer> -->
    </div>
  </template>
  
  <script setup>
  import { useUserStore } from '@/stores/user'
  
  const userStore = useUserStore()
  
  function logout() {
    userStore.removeToken()
  }
  </script>
  
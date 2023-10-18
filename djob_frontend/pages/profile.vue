<template>
    <div class="py-10 px-6">
      <h1 class="mb-6 text-2xl font-semibold text-teal-700">{{$t('profile') }}</h1>
  
      <!-- Display user information -->
      <div class="bg-gray-100 p-4 rounded-lg">
        <!-- <h2 class="text-xl font-semibold text-gray-800">User Information</h2> -->
        <div class="flex flex-col md:flex-row md:items-center">
          <div class="mb-2 md:mb-0">
            <div class="font-semibold">Name:</div>
            <div class="text-teal-700">{{ user.name }}</div>
          </div>
          <div class="mb-2 md:mb-0 md:ml-4">
            <div class="font-semibold">Email:</div>
            <div class="text-teal-700">{{ user.email }}</div>
          </div>
        </div>
        <div class="mt-4">
          <div class="font-semibold text-teal-700">Subscribed Plan:</div>
          <div class="text-gray-600">Free Plan</div>
        </div>
      </div>
  
      <!-- Display user plans (dummy data) -->
      <div>
        <h2 class="text-xl font-semibold text-gray-800 mt-6">Available Plans:</h2>
        <ul>
          <li v-for="plan in plans" :key="plan.id" class="bg-gray-100 p-4 my-2 rounded-lg">
            <div class="text-teal-700 font-semibold">{{ plan.name }}</div>
            <div class="text-gray-600">{{ plan.description }}</div>
            <div class="text-teal-700 font-semibold">${{ plan.price.toFixed(2) }}</div>
            <button
              :disabled="plan.id !== 1"
              class="mt-2 py-2 px-4 bg-teal-700 text-white rounded hover:bg-teal-800"
            >
              {{ plan.id === 1 ? 'Subscribed' : 'Unvailable' }}
            </button>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const user = ref({
    name: '-----',
    email: '------',
  });
  
  const plans = ref([
    { id: 1, name: 'Free Plan', description: 'Basic free plan', price: 0.00 },
    { id: 2, name: 'Pro Plan', description: 'Upgrade to our Pro plan', price: 19.99 },
    { id: 3, name: 'Premium Plan', description: 'Get all the premium features', price: 29.99 },
]);
  
  // ... your other script code ...
  </script>
  
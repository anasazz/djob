<script setup>
import { onMounted, ref, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
let items = ref()
let search = ref('') // The search input value
let filteredItems = ref([]) // The filtered list of employees

onMounted(() => {
    if (!userStore.user.isAuthenticated) {
        router.push('/login')
    } else {
        getJobs()
    }
})

useSeoMeta({
    title: 'My Employees',
    ogTitle: 'My Employees',
    description: 'The description'
})

async function getJobs() {
    await $fetch('http://127.0.0.1:8000/api/v1/jobs/myemployees', {
        headers: {
            'Authorization': 'token ' + userStore.user.token,
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        items.value = response
        filteredItems.value = response
    })
    .catch(error => {
        console.log('error', error)
    })
}

function deleteJob(id) {
    console.log('id', id)

    items.value = items.value.filter(job => job.id !== id)
}

// Watch for changes in the search input
watch(search, (newSearch) => {
    if (!newSearch) {
        filteredItems.value = items.value // If search is empty, show all items
    } else {
        // Filter items based on the search input
        filteredItems.value = items.value.filter((item) =>
            item.name.toLowerCase().includes(newSearch.toLowerCase()) ||
            item.email.toLowerCase().includes(newSearch.toLowerCase())
        )
    }
})
</script>

<template>
    <div class="py-10 px-6">
      <h1 class="mb-6 text-2xl font-semibold text-slate-700">{{$t('employees')}}</h1>

      <NuxtLink to="/addEmployee" class="my-5  py-2 px-6 bg-black text-white shadow-md  hover:bg-teal-700 rounded-xl mb-2">
        {{$t('addemployees')}}
      </NuxtLink>

      <input v-model="search" type="text" placeholder="Search employees..." class="w-full mb-4 py-2 my-5 px-6 rounded-xl bg-slate-50 border">
      
      <div v-if="filteredItems && filteredItems.length === 0" class="text-gray-700 my-5 bg-gray-100 border-1 border-gray-400 rounded-lg p-4 text-center">
          <p>No data available.</p>
          <p class="text-sm text-gray-400">No employees found.</p>
      </div>

      <Employee
        v-for="item in filteredItems"
        :key="item.id"
        :item="item" 
        :my="true"
        v-on:deleteJob="deleteJob(item.id)"
      />
  </div>
</template>

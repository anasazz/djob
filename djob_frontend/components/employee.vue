<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const emit = defineEmits(['deleteJob'])

const props = defineProps({
    my: {
        type: [Boolean]
    },
    item: {
        type: [Object]
    }
})

async function deleteEmployee(id) {
    await $fetch('http://127.0.0.1:8000/api/v1/jobs/employeeDetails/' + id + '/delete/', {
        method: 'DELETE',
        headers: {
            'Authorization': 'token ' + userStore.user.token,
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        console.log('response', response)
        alert('employee deleted')

        emit('deleteJob', id)
    })
    .catch(error => {
        console.log(error)
    })
}
</script>

<template>
    <div class="px-3 shadow-sm py-2 my-5 flex items-center justify-between bg-gray-100 rounded-xl">
        <div>
            <h3 class="mb-2 text-xl font-semibold"> {{ item.name }}</h3>
            <p class="text-gray-600">{{ item.phone }}</p>
            <p class="text-gray-600">{{ item.description }}</p>
            <p class="mb-1"> {{ item.email }}</p>
        </div>

        <div>
            <!-- <p class="mb-2">{{ item.description }}</p> -->
    
            <p class="mb-1"> {{ item.matricule }}</p>
       
            <!-- <p>{{ job.position_salary }}</p> -->
        </div>

        <div>
            <!-- <p>Posted {{ job.created_at_formatted }}</p> -->
        </div>

        <div class="space-x-4">
            <!-- <NuxtLink v-bind:to="'/browse/' + item.id" class="py-4 px-6 bg-teal-700 text-white rounded-xl">Details</NuxtLink> -->
            <NuxtLink v-bind:to="'/editemployee/' + item.id" class="py-4 px-6 bg-slate-400 text-white rounded-xl font-bold">{{$t('edit')}}</NuxtLink>
            <button @click="deleteEmployee(item.id)" class="py-4 px-6 bg-red-500 text-white rounded-xl font-bold">{{$t('delete')}}</button>
        </div>
    </div>
</template>
<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
let jobs = ref()

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
        jobs.value = response
        console.log(response);
    })
    .catch(error => {
        console.log('error', error)
    })
}

function deleteJob(id) {
    console.log('id', id)

    jobs.value = jobs.value.filter(job => job.id !== id)
}
</script>

<template>
    <div class="py-10 px-6">
        <h1 class="mb-6 text-2xl">My Employees </h1>

        <NuxtLink to="/addEmployee" class="my-5  py-2 px-6 bg-black text-white shadow-md  hover:bg-teal-700 rounded-xl mb-2">add employees</NuxtLink>


        <div class="space-y-4 mt-5">
            <div v-for="job in jobs" :key="job.id"
                :job="job"  class=" c">

                <p>{{job.name}} -  {{job.email}} -  {{job.description}}  </p>

            </div>
            
        </div>
    </div>
</template>
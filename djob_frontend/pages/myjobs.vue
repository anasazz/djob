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
    title: 'My jobs',
    ogTitle: 'My jobs',
    description: 'The description'
})

async function getJobs() {
    await $fetch('https://cloud.lidiye.com/api/v1/jobs/my', {
        headers: {
            'Authorization': 'token ' + userStore.user.token,
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        jobs.value = response
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
        <h1 class="mb-6 text-2xl">Mon Business</h1>
        <NuxtLink to="/createjob" class="py-2 my-5 font-bold px-6 bg-slate-200 text-black hover:bg-slate-700  hover:text-white rounded-xl">

            {{$t('createBusiness')}}
        </NuxtLink>


        <div v-if="jobs && jobs.length === 0" class="text-gray-700 my-5 bg-gray-100  border-1 border-gray-400 rounded-lg p-4 text-center">
      <p>No data available.</p>
      <p class="text-sm  text-gray-400">Start adding your employees</p>
    </div>

        <div class="space-y-4 mt-4">
            <Job
                v-for="job in jobs"
                :key="job.id"
                :job="job" 
                :my="true"
                v-on:deleteJob="deleteJob(job.id)"
            />
        </div>
    </div>
</template>
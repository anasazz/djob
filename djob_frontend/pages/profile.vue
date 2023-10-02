<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'



const userStore = useUserStore()
const router = useRouter()
let plans = ref()

onMounted(() => {
    if (!userStore.user.isAuthenticated) {
        router.push('/login')
    } else {
        getPlans()
    }
})

useSeoMeta({
    title: 'Mon Profile',
    ogTitle: 'Mon Profile',
    description: 'The description'
})

async function getPlans() {
    await $fetch('http://127.0.0.1:8000/api/v1/jobs/plans', {
        headers: {
            'Authorization': 'token ' + userStore.user.token,
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        plans.value = response
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
        <h1 class="mb-6 text-2xl">Mon Profile</h1>

        <div class="space-y-4">
            <!-- <Job
                v-for="job in jobs"
                :key="job.id"
                :job="job" 
                :my="true"
                v-on:deleteJob="deleteJob(job.id)"
            /> -->
        </div>
    </div>
</template>
<script setup>
 const { data: jobs } = await useFetch('https://cloud.lidiye.com/api/v1/jobs/newest/')
</script>

<template>
    <div>
        <div class="py-20 px-6 rounded-2xl bg-slate-100 text-center ">
            <h1 class=" text-5xl text-black">Automate payroll sending</h1>

            <!-- <NuxtLink to="/browse" class="inline-block py-4 px-8 bg-teal-900 text-white rounded-xl">Browse</NuxtLink> -->
        </div>

        <div class="py-10 px-6">
            <!-- <h2 class="mb-8 text-2xl text-center">Newest jobs</h2> -->

            <!-- <div class="space-y-4">
                <Job 
                    v-for="job in jobs" 
                    v-bind:key="job.id"
                    v-bind:job="job" 
                />
            </div> -->
        </div>
    </div>
</template>
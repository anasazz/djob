<script setup>
const route = useRoute()

const {data: job} = await useFetch('http://127.0.0.1:8000/api/v1/jobs/' + route.params.id + '/')

useSeoMeta({
    // title: job.value.title,
    // ogTitle: job.value.title,
    // description: job.value.description
})
</script>

<template>
    <div class="py-10 px-6">
      <div class=" mx-auto bg-white shadow-sm border rounded-lg overflow-hidden">
        <!-- Header section -->
        <div class="p-6 bg-gray-200 border-b border-gray-300">
          <p class="text-gray-600">{{ job.acheteur_public }}</p>
        </div>

        <p class="text-lg font-semibold p-6">{{ job.objet }}</p>

  
        <!-- Main content section -->
        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Left column: Job details -->
          <div>
            <div class="mb-4">
              <span class="font-semibold">Procédure:</span>
              <span class="ml-2 text-gray-700">{{ job.procedure }}</span>
            </div>
            <div class="mb-4">
              <span class="font-semibold">Publié le:</span>
              <span class="ml-2 text-gray-700">{{ job.publie_le }}</span>
            </div>
            <div class="mb-4">
              <span class="font-semibold">Organisation:</span>
              <span class="ml-2 text-gray-700">{{ job.org }}</span>
            </div>
            <div class="mb-4">
              <span class="font-semibold">Référence:</span>
              <span class="ml-2 text-gray-700">{{ job.reference }}</span>
            </div>
            <div class="mb-4">
              <span class="font-semibold">Lieu d'exécution:</span>
              <span class="ml-2 text-gray-700">{{ job.lieu_execution }}</span>
            </div>
            <div class="mb-4">
              <span class="font-semibold">Date limite:</span>
              <span class="ml-2 text-gray-700">{{ job.date_limite }}</span>
            </div>
            <!-- Add more fields as needed -->
          </div>
  
          <!-- Right column: Company and actions -->
          <div class="p-4 bg-slate-700 text-white rounded-lg">
            <div class="mb-6">
              <h3 class="text-2xl font-semibold">Entreprise</h3>
              <p class="mt-2">{{ job.acheteur_public }}</p>
            </div>
            <div class="mb-6">
              <h3 class="text-2xl font-semibold">Actions</h3>
              <div class="mt-4 space-y-4">
                <!-- <NuxtLink
                  :to="'/editjob/' + job.id"
                  class="block py-2 px-6 bg-slate-400 text-white rounded-xl"
                  >Modifier</NuxtLink
                >
                <a
                  @click="deleteJob(job.id)"
                  href="#"
                  class="block py-2 px-6 bg-rose-700 text-white rounded-xl"
                  >Supprimer</a
                > -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
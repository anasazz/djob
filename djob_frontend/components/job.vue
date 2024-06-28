<template>
    <div class="px-3 py-2 flex items-start justify-between bg-white border rounded-xl">
      <!-- Left section: Job details -->
      <div class="flex-grow mr-4  w-2/3">
        <h3 class="text-sm truncate   font-semibold mb-1">{{ job.objet }}</h3>

        <!-- Title and Company Name -->
        <div>
          <p class="text-gray-600">{{ job.acheteur_public }}</p>
        </div>
  
        <!-- Description and other fields -->
        <div class="mt-2">
          <div class="mb-2">
            <span class="font-semibold">Lieu d'exécution:</span>
            <span class="ml-2 text-gray-700">{{ job.lieu_execution }}</span>
          </div>
          <div class="mb-2">
            <span class="font-semibold">Date limite:</span>
            <span class="ml-2 text-gray-700">{{ job.date_limite }}</span>
          </div>
          <div class="mb-2">
            <span class="font-semibold">Procédure:</span>
            <span class="ml-2 text-gray-700">{{ job.procedure }}</span>
          </div>
          <!-- Add more fields as needed -->
          <div class="mb-2" v-if="job.estimation">
            <span class="font-semibold">Estimation:</span>
            <span class="ml-2 text-gray-700">{{ job.estimation }}</span>
          </div>
          <div class="mb-2" v-if="job.reserve_tpe_pme">
            <span class="font-semibold">Réservé à la TPE et PME:</span>
            <span class="ml-2 text-gray-700">{{ job.reserve_tpe_pme }}</span>
          </div>
          <div class="mb-2" v-if="job.domaines_activite">
            <span class="font-semibold">Domaines d'activité:</span>
            <span class="ml-2 text-gray-700">{{ job.domaines_activite }}</span>
          </div>
          <div class="mb-2" v-if="job.adresse_retrait_dossiers">
            <span class="font-semibold">Adresse de retrait des dossiers:</span>
            <span class="ml-2 text-gray-700">{{ job.adresse_retrait_dossiers }}</span>
          </div>
          <div class="mb-2" v-if="job.adresse_depot_offres">
            <span class="font-semibold">Adresse de dépôt des offres:</span>
            <span class="ml-2 text-gray-700">{{ job.adresse_depot_offres }}</span>
          </div>
          <div class="mb-2" v-if="job.lieu_ouverture_plis">
            <span class="font-semibold">Lieu d'ouverture des plis:</span>
            <span class="ml-2 text-gray-700">{{ job.lieu_ouverture_plis }}</span>
          </div>
          <div class="mb-2" v-if="job.prix_acquisition_plans">
            <span class="font-semibold">Prix d'acquisition des plans:</span>
            <span class="ml-2 text-gray-700">{{ job.prix_acquisition_plans }}</span>
          </div>
          <div class="mb-2" v-if="job.caution_provisoire">
            <span class="font-semibold">Caution provisoire:</span>
            <span class="ml-2 text-gray-700">{{ job.caution_provisoire }}</span>
          </div>
          <div class="mb-2" v-if="job.qualifications">
            <span class="font-semibold">Qualifications:</span>
            <span class="ml-2 text-gray-700">{{ job.qualifications }}</span>
          </div>
          <div class="mb-2" v-if="job.agrements">
            <span class="font-semibold">Agréments:</span>
            <span class="ml-2 text-gray-700">{{ job.agrements }}</span>
          </div>
          <div class="mb-2" v-if="job.prospectus_notices_documents">
            <span class="font-semibold">Prospectus, notices ou autres documents:</span>
            <span class="ml-2 text-gray-700">{{ job.prospectus_notices_documents }}</span>
          </div>
          <div class="mb-2" v-if="job.reunion">
            <span class="font-semibold">Réunion:</span>
            <span class="ml-2 text-gray-700">{{ job.reunion }}</span>
          </div>
          <div class="mb-2" v-if="job.visites_lieux">
            <span class="font-semibold">Visites des lieux:</span>
            <span class="ml-2 text-gray-700">{{ job.visites_lieux }}</span>
          </div>
          <div class="mb-2" v-if="job.variante">
            <span class="font-semibold">Variante:</span>
            <span class="ml-2 text-gray-700">{{ job.variante }}</span>
          </div>
          <div class="mb-2" v-if="job.contact_administratif">
            <span class="font-semibold">Contact Administratif:</span>
            <span class="ml-2 text-gray-700">{{ job.contact_administratif }}</span>
          </div>
        </div>
      </div>
  
      <!-- Right section: Actions -->
      <div class="flex-shrink-0 space-y-2">
        <!-- Actions for authenticated users -->
        <div v-if="userStore.user.isAuthenticated">
          <!-- Navigation links -->
          <div class="space-y-2">
            <NuxtLink
              :to="'/browse/' + job.id"
              class="block py-2 px-6 bg-slate-700 text-white rounded-xl"
              >Détails</NuxtLink
            >
            <NuxtLink
              v-if="my"
              :to="'/editjob/' + job.id"
              class="block py-2 px-6 bg-slate-400 text-white rounded-xl"
              >{{ $t('edit') }}</NuxtLink
            >
            <a
              v-if="my"
              @click="deleteJob(job.id)"
              href="#"
              class="block py-2 px-6 bg-rose-700 text-white rounded-xl"
              >{{ $t('delete') }}</a
            >
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useUserStore } from '@/stores/user'
  import { defineProps, defineEmits } from 'vue'
  
  const emit = defineEmits(['deleteJob'])
  const userStore = useUserStore()
  
  const props = defineProps({
    my: {
      type: Boolean
    },
    job: {
      type: Object
    }
  })
  
  async function deleteJob(id) {
    try {
      const response = await $fetch(
        `http://127.0.0.1:8000/api/v1/jobs/${id}/delete/`,
        {
          method: 'DELETE',
          headers: {
            Authorization: 'token ' + userStore.user.token,
            'Content-Type': 'application/json'
          }
        }
      )
      console.log('response', response)
      emit('deleteJob', id)
    } catch (error) {
      console.error('Error deleting job:', error)
    }
  }
  </script>
  
  <style scoped>
  /* Add scoped styles here if needed */
  </style>
  
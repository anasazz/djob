<script setup>
const route = useRoute()
const { data: job, error, loading, fetch } = useFetch(`http://127.0.0.1:8000/api/v1/jobs/${route.params.id}/`)

const fetchMoreDetails = async () => {
  alert('clicked')
  try {
    const queryParam = 'additional=true'  // Example query parameter
    const {data: job, error, loading, fetch} = await useFetch(`http://127.0.0.1:8000/api/v1/jobs/${route.params.id}/?${queryParam}`)
    // Handle response and update job details or perform necessary actions
    // For example, update job with new data
    console.log("respo",job);
    
    
  } catch (err) {
    console.log('Error fetching more details:', err)
    // Handle error appropriately, e.g., show a notification
  }
}
</script>


<template>
  <div v-if="job" class="py-10 px-6">
    <div class="mx-auto bg-white shadow-sm border rounded-lg overflow-hidden">
      <!-- Header section -->
      <div class="p-6 bg-gray-200 border-b border-gray-300">
        <p class="text-gray-600">{{ job.acheteur_public }}</p>
      </div>

      <!-- Main content section -->
      <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Left column: Job details -->
        <div>
          <div class="mb-4">
            <span class="font-semibold">Procédure:</span>
            <!-- <span class="ml-2 text-gray-700">{{ job.json_raw['Procédure'] }}</span> -->
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
            <span class="ml-2 text-gray-700">{{ job.date_limite }} / {{ job.time_left }}</span>
          </div>
          <div v-if="!job.estimation " class="mt-6 text-center">
            <button @click="fetchMoreDetails" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg shadow-sm">
              Fetch More Details
            </button>
          </div>
          <div v-else>
            <div  class="mb-4">
            <span class="font-semibold">Estimation (en Dhs TTC):</span>
            <span class="ml-2 text-gray-700">{{ job.estimation }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Réservé à la TPE et PME:</span>
            <span class="ml-2 text-gray-700">{{ job.reserve_tpe_pme }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Adresse retrait dossiers:</span>
            <a class="ml-2 text-blue-600 underline" :href="job.adresse_retrait_dossiers">{{ job.adresse_retrait_dossiers }}</a>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Adresse dépôt offres:</span>
            <a class="ml-2 text-blue-600 underline" :href="job.adresse_depot_offres">{{ job.adresse_depot_offres }}</a>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Lieu ouverture plis:</span>
            <span class="ml-2 text-gray-700">{{ job.lieu_ouverture_plis }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Prix acquisition plans:</span>
            <span class="ml-2 text-gray-700">{{ job.prix_acquisition_plans }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Caution provisoire:</span>
            <span class="ml-2 text-gray-700">{{ job.caution_provisoire }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Qualifications:</span>
            <span class="ml-2 text-gray-700">{{ job.qualifications }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Agréments:</span>
            <span class="ml-2 text-gray-700">{{ job.agrements }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Prospectus, notices, documents:</span>
            <span class="ml-2 text-gray-700">{{ job.prospectus_notices_documents }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Réunion:</span>
            <span class="ml-2 text-gray-700">{{ job.reunion }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Visites lieux:</span>
            <span class="ml-2 text-gray-700">{{ job.visites_lieux }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Variante:</span>
            <span class="ml-2 text-gray-700">{{ job.variante }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Contact administratif:</span>
            <span class="ml-2 text-gray-700">{{ job.contact_administratif }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Téléphone:</span>
            <!-- <span class="ml-2 text-gray-700">{{ job.json_raw['Téléphone'] }}</span> -->
          </div>
          <div class="mb-4">
            <span class="font-semibold">Télécopieur:</span>
            <!-- <span class="ml-2 text-gray-700">{{ job.json_raw['Télécopieur'] }}</span> -->
          </div>

          </div>

          
          
          <!-- <div class="mb-4">
            <span class="font-semibold">Estimation (en Dhs TTC):</span>
            <span class="ml-2 text-gray-700">{{ job.json_raw['Estimation (en Dhs TTC)'] }}</span>
          </div>
          <div class="mb-4">
            <span class="font-semibold">Réservé à la TPE et PME installées au Maroc, jeunes entreprises innovantes, Coopératives et auto-entrepreneurs:</span>
            <span class="ml-2 text-gray-700">{{ job.json_raw['Réservé à la TPE et PME installées au Maroc, jeunes entreprises innovantes, Coopératives et auto-entrepreneurs'] }}</span>
          </div> -->
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
              <!-- Add edit/delete actions if needed -->
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Button to fetch more details -->
    
  </div>

  <div v-else>NO JOB</div>

  
</template>


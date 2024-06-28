<template>
    <div>
      <!-- Categories -->
      <template v-for="(categories, sector) in sectors_and_categories" :key="sector">
        <div class="border-b border-slate-200 mb-2">
          <p class="text-slate-500 font-semibold mt-4 cursor-pointer" @click="toggleSector(sector)">
            {{ sector }}
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 inline ml-1" :class="{ 'transform rotate-180': isSectorOpen(sector) }">
              <path fill-rule="evenodd" d="M10 18a1 1 0 01-.707-.293l-7-7a1 1 0 011.414-1.414L10 15.586l6.293-6.293a1 1 0 011.414 1.414l-7 7A1 1 0 0110 18z" clip-rule="evenodd" />
            </svg>
          </p>
          <div v-if="isSectorOpen(sector)">
            <p
              v-for="category in categories"
              :key="category"
              @click="toggleCategory(sector, category)"
              :class="{ 'bg-slate-200': isSelected(sector, category) }"
              class="py-1 my-1 px-4 text-teal-900 rounded-xl text-sm cursor-pointer"
            >
              {{ category }}
            </p>
          </div>
        </div>
      </template>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // Sectors and Categories data
  const sectors_and_categories = {
    'Travaux': [
      'Travaux de voiries, chemins et pistes',
      'Travaux hydrauliques, maritimes et fluviaux',
      'Travaux d’assainissement, d’eau potable et de réseaux divers',
      'Construction d\'ouvrages d\'art',
      'Travaux d’électricité',
      'Aménagement de jardins, d\'espaces verts',
      'Travaux de construction et d’aménagement',
      'Travaux d’installation',
      'Terrassements',
      'Fondations, injections, parois moulées, sondages et forages',
      'Travaux d’étanchéité, isolation, plomberie et menuiserie',
      'Travaux de revêtement, platerie et peinture',
      'Travaux forestiers'
    ],
    'Fournitures': [
      'Effets d’habillement et accessoires',
      'Matériel et fournitures électriques, électronique, électromécanique et pièces de rechange',
      'Matériel technique, de lutte contre l’incendie et pièces de rechange',
      'Matériel de transport, pièces de rechange et pneumatiques',
      'Matériel, mobilier et fournitures de bureau',
      'Matériel informatique, logiciels et pièces de rechanges',
      'Engins de chantier, matériel de manutention et de levage',
      'Documentation, manuels, fournitures scolaires et d’enseignement',
      'Equipements et produits médicaux, pharmaceutiques et de laboratoire',
      'Produits alimentaires, d’élevage, de la pêche, d’agriculture, d’horticulture et pépinière',
      'Matériaux de construction, plomberie, quincaillerie et outillages',
      'Imprimés, produits d’impression, de reproduction, et de photographie',
      'Produits chimiques, de nettoyage, insecticides',
      'Matériel et articles de literie, de couchage, de cuisine et de buanderie',
      'Produits pétroliers, carburants, lubrifiants et produits de chauffage',
      'Matériel et articles de sport, médailles, effigies et drapeaux',
      'Matières premières et produits de textile, cuir, caoutchouc et plastique',
      'Location avec option d’achat de biens, d’équipements de matériel et d’outillage',
      'Objets d’art, articles artistiques, de divertissement et de médiathèque'
    ],
    'Services': [
      'Services de location sans option d’achat',
      'Services d’assurance',
      'Services architecturales et topographiques',
      'Services courants',
      'Conseil, audit et assistance à maitrise d’ouvrage (à l’exception du domaine des nouvelles technologies)',
      'Nettoyage, gardiennage, entretien et maintenance',
      'Etudes d’ingénierie',
      'Prestations d’essais, de contrôle et de laboratoire',
      'Services d’hôtellerie, hébergement, restauration, événementiel et marketing',
      'Transport, collecte et services connexes',
      'Services de technologies de l\'information et télécommunications',
      'Services de santé, vétérinaire',
      'Services agricoles, d’élevage, de pêche'
    ]
  };
  
  // Selected filters
  let selectedFilters = ref([]);
  
  // Function to toggle category selection
  function toggleCategory(sector, category) {
    const index = selectedFilters.value.findIndex(filter => filter.sector === sector && filter.category === category);
    if (index === -1) {
      selectedFilters.value.push({ sector, category });
    } else {
      selectedFilters.value.splice(index, 1);
    }
    // Emit event to parent component or perform any required action
    // fetchJobs(); // Uncomment if you want to trigger job fetching
  }
  
  // Function to check if category is selected
  function isSelected(sector, category) {
    return selectedFilters.value.some(filter => filter.sector === sector && filter.category === category);
  }
  
  // Function to toggle sector open/close state
  let openSectors = ref([]);
  function toggleSector(sector) {
    if (openSectors.value.includes(sector)) {
      openSectors.value = openSectors.value.filter(s => s !== sector);
    } else {
      openSectors.value.push(sector);
    }
  }
  
  // Function to check if sector is open
  function isSectorOpen(sector) {
    return openSectors.value.includes(sector);
  }
  </script>
  
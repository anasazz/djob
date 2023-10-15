<template>
    <div class="relative">
      <div>
        <input class="bg-white w-full rounded-lg px-3 py-2" v-model="search" placeholder="Search employee..." />
      </div>
      <div>
        <select  @change="changeEmployee(file)" class="bg-slate-200 w-full rounded-lg px-3 py-2" v-model="selectedOption">
          <option value="" disabled >{{ filteredOptions.length }} Résultats</option>
          <option v-for="option in filteredOptions" :key="option.id" :value="option.id">{{ option.name }} </option>
        </select>
      </div>
      <!-- <p>{{JSON.stringify(file)}}</p> -->
      <!-- <p>selectedOption: {{selectedOption}} </p>
      <p>backend: {{file.employee}} </p>
      <p>file id: {{file.id}} </p> -->
    </div>
    
  </template>
  
  
  <script setup>
import { ref, computed, watch, defineProps, defineEmits } from 'vue';
  
import { useUserStore } from "@/stores/user";
import CustomSelect from '@/components/CustomSelect.vue';


const userStore = useUserStore();
  
  const changeEmployee = async (file) => {
    console.log("selected option ", selectedOption.value);
    console.log("selected file ", file.id);
  try {
    const response = await fetch(`https://cloud.lidiye.com/api/v1/jobs/change-employee/${file.id}/`, {
      method: "PUT",
      headers: {
        Authorization: "token " + userStore.user.token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        newEmployeeId: selectedOption.value,
      }),
    });

    if (response.ok) {
        console.log(response.data);
      // Successfully updated the selected employee on the backend
      alert("Employee changed successfully");
    } else {
      // Handle the error response here
      alert("Error changing employee");
    }
  } catch (error) {
    console.error("Error changing employee:", error);
  }
};
  const { options , file } = defineProps(['options','file']);
//   const { selectedEmployee } = defineProps(['selectedEmployee']);
  const emit  = defineEmits(['update:selectedEmployee']);
  
  const search = ref('');
  const selectedOption = ref(null);
  const initialOptions = ref([]); // Store the initial options
  
  // Initialize initialOptions with the options prop
  initialOptions.value = options;
  selectedOption.value = file.employee

  
  
  const filteredOptions = computed(() => {
    const query = search.value.toLowerCase();
    return initialOptions.value.filter(option =>
      option.name.toLowerCase().includes(query)
    );
  });
  
//   const updateSelectedEmployee = (event) => {
//     const newValue = event.target.value;
//     console.log("selectedEmployee newValue", newValue);
//     emit('update:selectedEmployee', newValue);
//   };
  watch(selectedOption, (newVal) => {
    console.log("watched ", newVal);
    emit('update:selectedEmployee', newVal);
  });
  </script>
  
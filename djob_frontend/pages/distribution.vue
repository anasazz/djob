<script setup>
import { onMounted, ref, reactive } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import CustomSelect from '@/components/CustomSelect.vue';


const userStore = useUserStore();
const router = useRouter();

// Modal related data
const isModalOpen = ref(false);
const selectedFiles = ref([]);
const userList = ref([]);
const errors = ref([]);
const documents = ref([]); // Track the uploaded documents
const documentList = ref([]);


// Function to open the modal
const openModal = () => {
  isModalOpen.value = true;
};

// Function to close the modal
const closeModal = () => {
  isModalOpen.value = false;
};

// Object to store select all states for each date group
const selectAll = ref({});

// Method to select all documents within a date group
const selectAllDocuments = (date) => {
  const group = groupedDocumentList.value[date];
  if (group) {
    group.forEach((file) => {
      if (!file.is_email_delivered) {
      
        file.isSelected = !file.isSelected;
      }
    });
  }
};




// Function to perform the file upload
const sendEmails = async () => {
  try {
    
    const response = await fetch("http://127.0.0.1:8000/api/v1/jobs/SendEmailsView/", {
      method: "POST",
      body: {},
      headers: {
        Authorization: "token " + userStore.user.token,
      },
    });

    if (response.ok) {
      return { status: "is sent" };
    } else {
      return { status: "failed" };
    }
  } catch (error) {
    console.error("Error  sending:", error);
    return { status: "failed" };
  }
};



// Function to perform the file upload
const performUpload = async (file) => {
  try {
    const formData = new FormData();
    formData.append("document", file);

    const response = await fetch("http://127.0.0.1:8000/api/v1/jobs/upload-files/", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: "token " + userStore.user.token,
      },
    });

    if (response.ok) {
      return { status: "is uploaded" };
    } else {
      return { status: "failed" };
    }
  } catch (error) {
    console.error("Error uploading file:", error);
    return { status: "failed" };
  }
};

// Function to handle file uploads
const handleFileUpload = (event) => {
  const files = event.target.files;
  selectedFiles.value = Array.from(files);

  // Add files to the documents list with an initial "is uploading" status
  selectedFiles.value.forEach((file) => {
    documents.value.push({
      name: file.name,
      status: "is uploading",
    });

    // Upload the file and update its status
    performUpload(file).then((status) => {
      const document = documents.value.find((doc) => doc.name === file.name);
      if (document) {
        document.status = status.status;
      }
    });
  });
};

// Function to fetch the list of employees from the API
const fetchEmployeeList = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/jobs/myemployees/", {
      method: "GET",
      headers: {
        Authorization: "token " + userStore.user.token,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const data = await response.json();
      userList.value = data;
    } else {
      // Handle the error response here
      alert("Error fetching employee list");
    }
  } catch (error) {
    alert("Error fetching employee list:");
  }
};

const fetchDocumentList = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/jobs/myDocuments/", {
      method: "GET",
      headers: {
        Authorization: "token " + userStore.user.token,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const data = await response.json();
      documentList.value = data;
      console.log("data",data);
    } else {
      // Handle the error response here
      console.error("Error fetching employee list");
    }
  } catch (error) {
    console.error("Error fetching employee list:", error);
  }
};

const selectedDocumentCount = computed(() => {
  return documentList.value.filter((file) => file.isSelected).length;
});

// Fetch the employee list when the component is mounted
onMounted(() => {
  fetchEmployeeList();
  fetchDocumentList()
});


const groupedDocumentList = computed(() => {
  const groupedData = {};
  documentList.value.forEach((file) => {
    const date = new Date(file.uploaded_at).toLocaleDateString(); // Convert the date to a string format
    if (!groupedData[date]) {
      groupedData[date] = [];
    }
    groupedData[date].push(file);
  });
  return groupedData;
});

</script>

<template>
  <div class="  ">
    <h1 class="mb-6 text-2xl">Distribution des bulletins de paie</h1>

    <!-- Add a button to trigger the modal -->
    <button
      @click="openModal"
      class="bg-teal-600 hover:bg-teal-700 text-white py-2 px-4 rounded-lg"
    >
      Importer des fiches de paie      

    </button>


    <button
      @click="sendEmails()"
      class="bg-slate-600 border border-dashed border-spacing-4 mx-4 hover:bg-blue-700 text-white py-2 px-4 rounded-lg"
    >
        Send emails ({{ selectedDocumentCount }} selected)
    </button>

    <!-- selectAll; {{JSON.stringify(selectAll)}} -->


    <div v-for="(group, date) in groupedDocumentList" :key="date">
      <h3 class="my-4 bg-slate-500 w-fit px-4 text-white font-bold py-1 rounded-full">{{ date }}</h3> <!-- Display the name of the day -->
      <input type="checkbox" v-model="selectAll[date]" @change="selectAllDocuments(date)" /> <span class="mx-3 text-center">selectionnez tout</span> 

      <ul>

        <li
          class="bg-slate-50 flex items-center text-center justify-between rounded-lg my-2 px-3 py-2"
          v-for="file in group"
          :key="file.id"
        >
        <input type="checkbox" v-model="file.isSelected" :disabled="file.is_email_delivered" />

          <p class="text-left font-semibold truncate w-1/4">{{ file.document.substring(file.document.lastIndexOf("/") + 1) }}</p>
          <!-- <p class="text-center font-semibold">  id: {{ file.id }}</p> -->
          <!-- <p class="text-center font-semibold">createdby  id: {{ file.created_by }}</p> -->
     
      
      <p
      class="text-center font-semibold"
        :class="{'fa-check text-green-500': file.is_email_delivered, 'fa-times text-red-500': !file.is_email_delivered}"
      >Email</p>


         
          <p class="text-center font-semibold">{{ file.uploaded_at }}</p>
          <CustomSelect  :file='file' v-model="file.employee" :options="userList" />

          <!-- <select :disabled="file.is_email_delivered" class="bg-slate-200 rounded-lg px-3 py-3" v-model="file.employee" @change="changeEmployee(file)">
            <option
              :value="employee.id"
              v-for="employee in userList"
              :key="employee.id"
            >
              {{ employee.name }}
            </option>
          </select>   -->
        </li>
      </ul>
    </div>

    
 
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center  justify-center z-50"
    >
      <div class="bg-white w-4/6 h-fit p-6 rounded-lg shadow-xl">
        <h2 class="text-lg font-semibold mb-4">Importer des fiches de paie</h2>
        <!-- {{JSON.stringify(documents)}} -->

        <!-- File input for PDF files -->
        <input type="file" multiple @change="handleFileUpload" accept=".pdf" />

        <!-- Display selected file names and allow assignment to employees -->
        

        <!-- Display the status of uploaded documents -->
        <ul>
          <li
            class="flex items-center text-center justify-between rounded-lg my-2 px-3 py-3"
            v-for="document in documents"
            :key="document.name"
          >
            <p class=" font-semibold truncate ">{{ document.name }}</p>
            <p :class="document.status === 'is uploaded' ? 'text-green-500' : 'text-red-500'">{{ document.status }}</p>
            
        </li>
        </ul>

        <!-- Close button for the modal -->
        <button
          @click="closeModal"
          class="bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 px-4 rounded-lg mt-4"
        >
          Fermer
        </button>
      </div>
    </div>
  </div>
</template>

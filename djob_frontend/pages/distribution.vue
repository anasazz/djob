<script setup>
import { onMounted, ref, reactive } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

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
      console.error("Error fetching employee list");
    }
  } catch (error) {
    console.error("Error fetching employee list:", error);
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

// Fetch the employee list when the component is mounted
onMounted(() => {
  fetchEmployeeList();
  fetchDocumentList()
});
</script>

<template>
  <div class="py-10 px-6">
    <h1 class="mb-6 text-2xl">Distribution des bulletins de paie</h1>

    <!-- Add a button to trigger the modal -->
    <button
      @click="openModal"
      class="bg-teal-600 hover:bg-teal-700 text-white py-2 px-4 rounded-lg"
    >
      Importer des fiches de paie 
    </button>

    <ul>
          <li
            class="bg-slate-50 flex items-center text-center justify-between rounded-lg my-2 px-3 py-3"
            v-for="file in documentList"
            :key="file.id"
          >
            <p class="text-center font-semibold">name: {{ file.document.substring(file.document.lastIndexOf("/") + 1) }}</p>
            <p class="text-center font-semibold">employee id: {{ file.created_by }}</p>
            <p class="text-center font-semibold">uploaded_at : {{ file.uploaded_at }}</p>
            <select class="bg-slate-200 rounded-lg px-3 py-3">
              <option
                :value="employee.id"
                v-for="employee in userList"
                :key="employee.id"
              >
                {{ employee.name }}
              </option>
            </select>  
          </li>
          
        </ul>

    <!-- Modal for uploading PDF files -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center justify-center z-50"
    >
      <div class="bg-white w-fit h-fit p-6 rounded-lg shadow-xl">
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
          Annuler
        </button>
      </div>
    </div>
  </div>
</template>

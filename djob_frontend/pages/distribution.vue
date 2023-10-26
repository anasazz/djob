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
const sendWhatsAppLoading = ref(false); // Add this
const sendEmailsLoading = ref(false); // Add this

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
      if (file) {
      
        file.isSelected = !file.isSelected;
      }
    });
  }
};




const sendWhatsApp = async () => {
  sendWhatsAppLoading.value = true; // Set loading state

  try {
    // Get the IDs of the selected documents
    const selectedDocumentIds = documentList.value
      .filter((file) => file.isSelected)
      .map((file) => file.id);

    // Check if at least one document is selected
    if (selectedDocumentIds.length === 0) {
      alert('No documents selected for WhatsApp.');
      sendWhatsAppLoading.value = false; // Set loading state

      return { status: 'failed' };
    }

    const response = await fetch("https://cloud.lidiye.com/api/v1/jobs/SendWhatsAppView/", {
      method: "POST",
      body: JSON.stringify({ document_ids: selectedDocumentIds }),
      headers: {
        Authorization: "token " + userStore.user.token,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      alert('WhatsApp messages sent successfully');
      fetchDocumentList();
      sendWhatsAppLoading.value = false; // Reset loading state

      return { status: "is sent" };
    } else {
      sendWhatsAppLoading.value = false; // Reset loading state

      return { status: "failed" };
    }
  } catch (error) {
    sendWhatsAppLoading.value = false; // Reset loading state

    console.error("Error sending WhatsApp messages:", error);
    return { status: "failed" };
  }
};

const sendEmails = async () => {
  sendEmailsLoading.value = true; // Set loading state

  try {
    // Get the IDs of the selected documents
    const selectedDocumentIds = documentList.value
      .filter((file) => file.isSelected)
      .map((file) => file.id);

    // Check if at least one document is selected
    if (selectedDocumentIds.length === 0) {
      alert('No documents selected for email.');
      sendEmailsLoading.value = false; // Set loading state

      return { status: 'failed' };
    }

    const response = await fetch("https://cloud.lidiye.com/api/v1/jobs/SendEmailsView/", {
      method: "POST",
      body: JSON.stringify({ document_ids: selectedDocumentIds }),
      headers: {
        Authorization: "token " + userStore.user.token,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      alert('Emails sent successfully');
      sendEmailsLoading.value = false; // Set loading state

      fetchDocumentList();
      return { status: "is sent" };
    } else {
      return { status: "failed" };
    }
  } catch (error) {
    sendEmailsLoading.value = false; // Set loading state

    console.error("Error sending emails:", error);
    return { status: "failed" };
  }
};




// Function to perform the file upload
const performUpload = async (file) => {
  try {
    const formData = new FormData();
    formData.append("document", file);

    const response = await fetch("https://cloud.lidiye.com/api/v1/jobs/upload-files/", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: "token " + userStore.user.token,
      },
    });

    if (response.ok) {
      fetchDocumentList()
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
    const response = await fetch("https://cloud.lidiye.com/api/v1/jobs/myemployees/", {
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
    const response = await fetch("https://cloud.lidiye.com/api/v1/jobs/myDocuments/", {
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

const emailButtonDisabled = computed(() => {
  // Check if all selected documents have is_email_delivered as true
  const selectedDocuments = documentList.value.filter((file) => file.isSelected);
  const allSelectedDelivered = selectedDocuments.every((file) => file.is_email_delivered);
  
  return allSelectedDelivered;
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
<div class="py-10 px-6">
      <h1 class="mb-6 text-2xl font-semibold text-slate-700"> {{$t('distributions')}}</h1>

    <!-- Add a button to trigger the modal -->
    <button
      @click="openModal"
      class="bg-black hover:bg-teal-700 text-white py-2 px-4 rounded-full"
    >
      {{$t('importFiles')}}
    </button>
    


    <button
  @click="sendEmails"
  :class="{
    'text-white bg-black': !sendEmailsLoading,
    'bg-red-100 text-white cursor-not-allowed': sendEmailsLoading
  }"
  class="border font-semibold border-dashed border-spacing-4 mx-4 hover:bg-slate-300 text-black py-2 px-4 rounded-lg"
  :disabled="sendEmailsLoading"
>
  {{$t('sendEmails')}}
  <template v-if="!sendEmailsLoading">
    ({{ selectedDocumentCount }} selected)
  </template>
</button>

<button
  @click="sendWhatsApp()"
  :class="{
    'text-white bg-black': !sendWhatsAppLoading,
    'bg-red-100 text-white cursor-not-allowed': sendWhatsAppLoading
  }"
  class="bg-green-300 font-semibold border border-dashed border-spacing-4 mx-4 hover:bg-green-400 text-black py-2 px-4 rounded-lg"
  :disabled="sendWhatsAppLoading"
>
  Send WhatsApp
  ({{ selectedDocumentCount }} selected)
</button>

    <!-- selectAll; {{JSON.stringify(selectAll)}} -->

    <!-- Styled "No data" message when there is no data -->
    <div v-if="Object.keys(groupedDocumentList).length === 0" class="text-gray-700 my-5 bg-gray-100  border-1 border-gray-400 rounded-lg p-4 text-center">
      <p>No data available.</p>
      <p class="text-sm  text-gray-400">Start uploading your pdfs</p>
    </div>


    <div v-for="(group, date) in groupedDocumentList" :key="date">
      <h3 class="my-4 bg-slate-500 w-fit px-4 text-white font-bold py-1 rounded-full">{{ date }}</h3> <!-- Display the name of the day -->
      <input type="checkbox" v-model="selectAll[date]" @change="selectAllDocuments(date)" /> <span class="mx-3 text-center">
        
        {{$t('selectAll')}}

      </span> 

      <ul>

        <li
          class=" border flex items-center text-center justify-between rounded-lg my-2 px-3 "
          v-for="file in group"
          :key="file.id"
        >
        <input type="checkbox" v-model="file.isSelected"  />

          <p class="text-left font-semibold truncate w-1/4">{{ file.document.substring(file.document.lastIndexOf("/") + 1) }}</p>
          <!-- <p class="text-center font-semibold">  id: {{ file.id }}</p> -->
          <!-- <p class="text-center font-semibold">createdby  id: {{ file.created_by }}</p> -->
     
      
    
      <p class="text-center font-semibold">
  <span class="text-green-500" v-if="file.is_email_delivered">      {{$t('emailSent')}}</span>
  <span class="text-red-500" v-else>      {{$t('emailFailed')}}  </span>
</p>

<p class="text-center font-semibold">
  <span class="text-green-500" v-if="file.is_whatsapp_delivered">     WhatsApp</span>
  <span class="text-red-500" v-else>  WhatsApp </span>
</p>


<!-- is_whatsapp_delivered -->
<!-- {{JSON.stringify(file)}} -->



         
          <p class="text-center font-semibold">{{ file.uploaded_at_formatted }}</p>
          <CustomSelect  :file='file' v-model="file.employee" :options="userList" />

        
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

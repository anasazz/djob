<script setup>
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

onMounted(() => {
    if (!userStore.user.isAuthenticated) {
        router.push('/login')
    }
})

let name = ref('')
let description = ref('')
let phone = ref('')
let email = ref('')
let errors = ref([])

async function submitForm() {
    console.log('submitForm')

    errors.value = []

    if (name.value == '') { errors.value.push('The name field is missing') }
    if (email.value == '') { errors.value.push('The email field is missing') }

    if (errors.value.length == 0) {
        await $fetch('https://cloud.lidiye.com/api/v1/jobs/createEmployee/', {
            method: 'POST',
            headers: {
                'Authorization': 'token ' + userStore.user.token,
                'Content-Type': 'application/json'
            },
            body: {
                name: name.value,
                description: description.value,
                phone: phone.value,
                email: email.value
            }
        })
        .then(response => {
            console.log('response', response)
            // Show an alert
            window.alert('Employee created successfully');

            // Reset form values
            name.value = '';
            description.value = '';
            phone.value = '';
            email.value = '';

            router.push({ path: '/employee' }) // Redirect to the employees list page
        })
        .catch(error => {
            if (error.response) {
                for (const property in error.response._data) {
                    errors.value.push(`${property}: ${error.response._data[property]}`)
                }
                console.log(JSON.stringify(error.response))
            } else if (error.message) {
                errors.value.push('Something went wrong. Please try again')

                console.log(JSON.stringify(error))
            }
        })
    }
}
</script>

<template>
    <div class="py-10 px-6">
        <h1 class="mb-6 text-2xl">Add Employee</h1>

        <form v-on:submit.prevent="submitForm" class="space-y-4">
            <!-- <div>
                <label>Category</label>

                <select v-model="category" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
                    <option value="">Select category</option>
                    <option
                        v-for="category in jobCategories"
                        :key="category.id"
                        :value="category.id"
                    >
                        {{ category.title }}
                    </option>
                </select>
            </div> -->

            <div>
                <label>Name</label>
                <input v-model="name" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>

            <div>
                <label>Description</label>
                <textarea v-model="description" class="w-full mt-2 p-4 rounded-xl bg-gray-100"></textarea>
            </div>

            <div>
                <label>Phone</label>
                <input type="text" v-model="phone" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>

            <div>
                <label>Email</label>
                <input type="email" v-model="email" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>

            <div
                v-if="errors.length" 
                class="mb-6 py-4 px-6 bg-rose-400 text-white rounded-xl"
            >
                <p v-for="error in errors" :key="error">
                    {{ error }}
                </p>
            </div>

            <button class="py-4 px-6 bg-teal-700 text-white rounded-xl">Submit</button>
        </form>
    </div>
</template>

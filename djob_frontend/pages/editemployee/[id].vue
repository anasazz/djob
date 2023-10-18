<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

onMounted(() => {
    if (!userStore.user.isAuthenticated) {
        router.push('/login')
    }
})

const {data: item} = await useFetch('https://cloud.lidiye.com/api/v1/jobs/employeeDetails/' + route.params.id + '/')

let name = ref(item.value.name)
let description = ref(item.value.description)
let email = ref(item.value.email)
let matricule = ref(item.value.matricule)
let phone = ref(item.value.phone)

let errors = ref([])

async function submitForm() {
    console.log('submitForm')

    errors.value = []

    if (name.value == '') { errors.value.push('The title field is missing')}
    if (description.value == '') { errors.value.push('The description field is missing')}

    if (errors.value.length == 0) {
        await $fetch('https://cloud.lidiye.com/api/v1/jobs/employeeUpdate/' + route.params.id + '/edit/', {
            method: 'PUT',
            headers: {
                'Authorization': 'token ' + userStore.user.token,
                'Content-Type': 'application/json'
            },
            body: {
                name: name.value,
                description: description.value,
                email: email.value,
                phone: phone.value,
                matricule: matricule.value,
        
            }
        })
        .then(response => {
            console.log('response', response)

            router.push({path: '/employee'})
        })
        .catch(error => {
            if (error.response) {
                if (errors.value.length < 5) {
                    errors.value.push(`${property}: ${error.response._data[property]}`);
                } else {
                    errors.value.push('Something went wrong. Please try again')

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
        <h1 class="mb-6 text-2xl">Edit Employee</h1>
        {{JSON.stringify(item)}}

        <form v-on:submit.prevent="submitForm" class="space-y-4">
            <div>
                <label>Title</label>
                <input v-model="name" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>

            <div>
                <label>Matricule</label>
                <input v-model="matricule" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>

            <div>
                <label>phone</label>
                <input v-model="phone" type="text" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>

            <div>
                <label>Description</label>
                <textarea v-model="description" class="w-full mt-2 p-4 rounded-xl bg-gray-100"></textarea>
            </div>


            <div>
                <label> e-mail</label>
                <input type="email" v-model="email" class="w-full mt-2 p-4 rounded-xl bg-gray-100">
            </div>

            <div
                v-if="errors.length" 
                class="mb-6 py-4 px-6 bg-rose-400 text-white rounded-xl"
            >
                <p v-for="error in errors" v-bind:key="error">
                    {{ error }}
                </p>
            </div>

            <button class="py-4 px-6 bg-slate-700 text-white rounded-xl">Save changes</button>
        </form>
    </div>
</template>
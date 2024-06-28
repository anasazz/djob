<script setup>
const router = useRouter()

let email = ref('')
let password1 = ref('')
let password2 = ref('')
let errors = ref([])

async function submitForm() {
    console.log('submitForm')

    errors.value = []

    await $fetch('http://127.0.0.1:8000/api/v1/users/', {
        method: 'POST',
        body: {
            username: email.value,
            password: password1.value
        }
    })
    .then(response => {
        console.log('response', response)

        router.push({path: '/login'})
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
</script>

<template>
    <div class="py-10 px-6">
        <div class="max-w-sm mx-auto py-10 px-6 bg-white border shadow-sm rounded-xl">
            <h1 class="mb-6 text-2xl text-center">Sign up</h1>

            <form v-on:submit.prevent="submitForm">
                <input v-model="email" type="email" placeholder="Your email address..." class="w-full mb-4 py-4 px-6 border rounded-xl">
                <input v-model="password1" type="password" placeholder="Your password..." class="w-full mb-4 py-4 px-6 border rounded-xl">
                <input v-model="password2" type="password" placeholder="Repeat password..." class="w-full mb-4 py-4 px-6 border rounded-xl">

                <div
                    v-if="errors.length" 
                    class="mb-6 py-4 px-6 bg-rose-400 text-white rounded-xl"
                >
                    <p v-for="error in errors" v-bind:key="error">
                        {{ error }}
                    </p>
                </div>

                <div class="flex justify-center">
                    <button class="py-2 px-6 mt-5 font-semibold bg-slate-700 text-white rounded-xl">Submit</button>
                </div> 

            </form>
        </div>
    </div>
</template>
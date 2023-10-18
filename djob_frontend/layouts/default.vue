<template>
  <div>
    <nav class="py-1 mb-5 px-5 flex items-center justify-between bg-white shadow-md">
      <NuxtLink to="/" class="text-xl text-black font-extrabold">lidiye.com</NuxtLink>

      <div class="flex items-center space-x-4">
        <div class="flex md:mt-0 items-center space-x-4">
          <form class="px-4 py-2 rounded-lg"> 
      <label for="locale-select">{{ $t('language') }}: </label> 
      <select class="bg-slate-50 border px-4 py-2 rounded-lg" id="locale-select" v-model="$i18n.locale"> 
        <option value="en">en</option> 
        <option value="fr">fr</option> 
      </select> 
    </form> 
          <template v-if="userStore.user.isAuthenticated">
            <NuxtLink to="/myjobs" class="py-2 font-semibold px-6 bg-slate-200 text-black hover:bg-slate-700 hover:text-white rounded-xl">Mon Business</NuxtLink>
            <a v-on:click="logout" class="py-2 px-6 bg-rose-600 hover:bg-rose-700 text-white rounded-xl">{{ $t('logout') }}</a>
          </template>

          <template v-else>
            
            <!-- <NuxtLink to="/" class="text-black hover:text-teal-300">Home</NuxtLink> -->
            <!-- <NuxtLink to="/browse" class="text-black hover:text-teal-300">Browse</NuxtLink> -->
            <NuxtLink to="/login" class="py-2 px-6 font-semibold bg-slate-900 hover:bg-teal-700 text-white rounded-xl">{{ $t('login') }}</NuxtLink>
            <NuxtLink to="/signup" class="py-2 px-6 font-semibold bg-white  hover:bg-slate-700 hover:text-white text-black border rounded-xl">{{ $t('signin') }}</NuxtLink>
          </template>
        </div>
      </div>
    </nav>

    <div class="flex">
      <!-- Sidebar -->
      <div v-if="userStore.user.isAuthenticated" class="w-1/6 h-screen p-4">
    <div class="text-gray-700">
        <h2 class="text-xl font-semibold mb-4">Menu</h2>
        <NuxtLink
            to="/distribution"
            class="block py-2 px-6  border text-black 
             rounded-xl mb-2"
            :class="{ 'text-white  bg-black': $route.path === '/distribution' }"
        >{{$t('distributions')}}
            
        </NuxtLink>
        <NuxtLink
            to="/employee"
            class="block py-2 px-6  text-black border  rounded-xl mb-2"
            :class="{ 'text-white bg-black': $route.path === '/employee' }"
        >{{$t('employees')}}
       
        </NuxtLink>
        <NuxtLink
            to="/profile"
            class="block py-2 px-6  text-black border  rounded-xl mb-2"
            :class="{ 'text-white bg-black': $route.path === '/profile' }"
        >{{$t('profile')}}
         
        </NuxtLink>
        <!-- Example of another sidebar link -->
    </div>
</div>


      <!-- Main Content -->
      <div :class="{'w-full': !userStore.user.isAuthenticated, 'w-5/6': userStore.user.isAuthenticated}" class="p-4 rounded-lg border shadow-sm">
        <!-- Your slot content will go here -->
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'


const userStore = useUserStore()
const router = useRouter()

function logout() {
  userStore.removeToken()
  router.push('/')
}
</script>

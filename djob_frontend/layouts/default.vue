<template>
  <div>
    <nav class="py-2 mb-5 px-5 flex items-center justify-between bg-white shadow-md">
      <NuxtLink to="/" class="text-xl text-black font-extrabold">masteroffre.com</NuxtLink>


      <div v-if="userStore.user.isAuthenticated" class="flex ">
    <div class="text-gray-700 flex">
        <!-- <NuxtLink
            to="/distribution"
            class="block py-2 px-6  text-black rounded-xl hover:bg-slate-100 font-bold   mr-2"
            :class="{ ' bg-slate-50 text-slate-600': $route.path === '/distribution' }"
        >{{$t('distributions')}}</NuxtLink>
         -->
        <!-- <NuxtLink
            to="/employee"
            class="block py-2 px-6 text-black font-bold hover:bg-slate-100 rounded-xl mr-2"
            :class="{ 'bg-slate-50 text-slate-600': $route.path === '/employee' }"
        >{{$t('employees')}}</NuxtLink>
        -->
        <NuxtLink
            to="/profile"
            class="block py-2 px-6 text-black font-bold  hover:bg-slate-100 rounded-xl mr-2"
            :class="{ 'bg-slate-50 text-slate-600': $route.path === '/profile' }"
        >{{$t('profile')}}</NuxtLink>
        <NuxtLink
            to="/browse"
            class="block py-2 px-6 text-black hover:bg-slate-100  font-bold  rounded-xl "
            :class="{ 'bg-slate-50 text-slate-600': $route.path === '/browse' }"
        >Rechercher</NuxtLink>
    </div>
</div>


      <div class="flex items-center space-x-4">
        <div class="flex md:mt-0 items-center space-x-4">
          <form class="px-4 py-2 rounded-lg"> 
      <select class="bg-slate-50 border px-4 py-2 rounded-lg" id="locale-select" v-model="$i18n.locale"> 
        <option value="en">En</option> 
        <option value="fr">Fr</option> 
      </select> 
    </form> 
          <!-- Sidebar -->
          

          <template v-if="userStore.user.isAuthenticated">
            <NuxtLink to="/myjobs" class="py-2 font-semibold px-6 bg-slate-200 text-black hover:bg-slate-700 hover:text-white rounded-xl">Mon Business</NuxtLink>
            <a v-on:click="logout" class="py-2 px-6 bg-rose-600 hover:bg-rose-700 text-white rounded-xl">{{ $t('logout') }}</a>
          </template>

          <template v-else>
            
            <!-- <NuxtLink to="/" class="text-black hover:text-slate-300">Home</NuxtLink> -->
            <!-- <NuxtLink to="/browse" class="text-black hover:text-slate-300">Browse</NuxtLink> -->
            <NuxtLink to="/login" class="py-2 px-6 font-semibold bg-slate-900 hover:bg-teal-700 text-white rounded-xl">{{ $t('login') }}</NuxtLink>
            <NuxtLink to="/signup" class="py-2 px-6 font-semibold bg-white  hover:bg-slate-700 hover:text-white text-black border rounded-xl">{{ $t('signup') }}</NuxtLink>
          </template>
        </div>
      </div>
    </nav>

    <div class="">



      <!-- Main Content -->
      <div :class="{'w-full': !userStore.user.isAuthenticated, 'w-6/6': userStore.user.isAuthenticated}" class="p-4 rounded-lg  shadow-sm">
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

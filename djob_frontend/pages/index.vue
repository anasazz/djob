<script setup>
</script>

<template>
    <div>

       
        <div class="py-20 border px-6 rounded-2xl bg-slate-50 text-center ">
            <h1 class=" text-5xl text-black">
                {{ $t('intro') }}
            </h1>

        </div>
        <form>

    </form>

        <div class="absolute bottom-0 right-3">
            <!-- <p>by browsing this website you agree to terms of services</p> -->
            <NuxtLink v-bind:to="'/politics/' " class="p-4 px-6 bg-slate-100 border  text-black rounded-xl font-bold">Privacy policy / terms of services</NuxtLink>

         
        </div>
    </div>
</template>
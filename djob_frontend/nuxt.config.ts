// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    css: ['~/assets/css/main.css'],
    postcss: {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        },
    },
    

    modules: [
      '@pinia/nuxt',
      'nuxt-icons',      
      ['@nuxtjs/google-fonts', {
          families: {
      
            Poppins: [100,200, 300,600, 900],
            Raleway: {
              wght: [100, 400],
              ital: [100]
            },
          }
      }],
    ],


})

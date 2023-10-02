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
      
      ['@nuxtjs/google-fonts', {
          families: {
      
            Inter: [400, 700],
             'Josefin+Sans': true,
            Lato: [100, 300],
            Raleway: {
              wght: [100, 400],
              ital: [100]
            },
          }
      }],
    ],

})

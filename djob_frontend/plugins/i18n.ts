import { createI18n } from 'vue-i18n';

export default defineNuxtPlugin(({ vueApp }) => {
  const i18n = createI18n({
    legacy: false,
    globalInjection: true,
    locale: 'en',
    messages: {
      en: {
        hello: 'Hello {name}!',
        login: 'Log In',
        signin: 'Create an Account',
        logout: 'Log Out',
        hide: 'Hide',
        see: 'See',
        confirm: 'Confirm',
        distributions: 'My Distributions',
        importFiles: 'Import Files',
        sendEmails: 'Send Emails',
        selectAll: 'Select All',
        employees: 'My Employees',
        addemployees: 'Add Employees',
        profile: 'My Profile',
        edit: 'Edit',
        delete: 'Delete',
        createBusiness: 'Create a Business',
        emailSent:'Email successfully delivered',
        emailFailed:"Email not sent yet or Email failed",

        intro: "Welcome to masteroffre!  Sign up and enjoy our services",
      },
      fr: {
        hello: 'Bonjour {name}!',
        login: 'Connexion',
        signin: 'Créer un Compte',
        logout: 'Déconnexion',
        hide: 'Masquer',
        see: 'Voir',
        confirm: 'Confirmer',
        distributions: 'Mes Distributions',
        importFiles: 'Importer des Fiches de Paie',
        sendEmails: 'Envoyer les Emails',
        selectAll: 'Tout Sélectionner',
        employees: 'Mes Employés',
        addemployees: 'Ajouter des Employés',
        profile: 'Mon Profil',
        edit: 'Modifier',
        delete: 'Supprimer',
        createBusiness: 'Créer un Business',
        emailSent:'Email a été bien envoyé',
        emailFailed:"Email non encore envoyé ou  n'a pas été envoyé",

        intro: "Bienvenue sur masteroffre ! Inscrivez-vous et profitez de nos services",
      },
    },
  });

  vueApp.use(i18n);
});

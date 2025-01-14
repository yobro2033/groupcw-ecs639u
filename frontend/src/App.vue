<template>
    <main class="container pt-4">
      <div id="app">
        <div v-if="userStore.username">
          <NavBar2 />
        </div>
        <div v-else>
          <NavBar />
        </div>
        <router-view/>
      </div>
    </main>
  </template>
  
  <script lang="ts">
  
  import { defineComponent } from "vue";
  import { RouterView } from "vue-router";
  import NavBar from './pages/components/NavBar.vue';
  import NavBar2 from './pages/components/NavBar2.vue';
  import { useUserStore } from "../stores/auth";
  
  
  export default defineComponent({
    components: {
      RouterView,
      NavBar,
      NavBar2,
    },
    setup() {
      const userStore = useUserStore();
      userStore.loadUser();
      return { userStore };
    },
    
  });
  </script>
  
  <style scoped>
  </style>
  
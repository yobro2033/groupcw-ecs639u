<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Home</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li><router-link class="nav-link" to="/Login">Login</router-link></li>
            <li><router-link class="nav-link" to="/Signup">Sign Up</router-link></li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
      import { useUserStore } from "../../../stores/auth";

      export default defineComponent({
          data() {
              return {
                  title: "Main Page",
              }
          },
          setup(){
            const userStore = useUserStore();
            return { userStore };
          }
      })
  </script>
  
  
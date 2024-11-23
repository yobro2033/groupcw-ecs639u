<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Home</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li><router-link class="nav-link" to="/ProfilePage">Profile Page</router-link></li>
            <li class="nav-item nav-link nav-bar-item" @click="logout()">Sign out</li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  <style>
    .nav-bar-item:hover {
      cursor: pointer;
    }
  </style>
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
          },
          methods:{
            async logout(){
              const requestOptions = {
              method: "POST",
              headers: {
                "Content-type": "application/json",
                Authorization: "Token " + this.userStore.token
              },
            }
            const loggedOut = await fetch('http://127.0.0.1:8000/api/logout/', requestOptions)
            var data = await loggedOut.json()
            if (data.done) {
              alert("logged out")
              this.userStore.login('','null');
            }
            }
          }
      })
  </script>
  
  
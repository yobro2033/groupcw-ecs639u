<template>
  <div class="h2">
    {{ title }}
  </div>
  <div class="container mt-5" v-if="userStore.username">
    <div class="alert alert-success" role="alert">
        Hello, {{ userStore.username }}!
      </div>
      <div class="card">
        <div class="card-header">
          Welcome to the Hobbies App
        </div>
        <div class="card-body">
          <p>
            Here you can add your hobbies and see other people's hobbies.
          </p>
          <p>
            You will be able to add friends by searching their username. The application will also show you people with the most common hobbies as you.
          </p>
        </div>
      </div>
    </div>
  <div class="container mt-5" v-else>
    You need to log in to see this page.
  </div>
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import { useUserStore } from "../../stores/auth";

    export default defineComponent({
        data() {
            return {
                title: "Hobbies app",
            }
        },
        setup(){
            const userStore = useUserStore();
            userStore.loadUser();
            return { userStore };
          }
    })
</script>

<style scoped>
</style>

<template>
    <div class="container mt-5">
      <form @submit.prevent="login()" class="border p-4 bg-light">
        <h2 class="mb-4 text-center">Log In!</h2>
  
        <div v-if="loginError" class="alert alert-danger">
          {{ loginErrorMessage }}
        </div>

        <!-- Username Field -->
        <div class="form-group mb-3">
          <label for="usernameInput" class="form-label">Email</label>
          <input type="text" v-model="username" class="form-control" id="usernameInput" placeholder="Enter email" required>
        </div>
  
        <!-- Password Field -->
        <div class="form-group mb-4">
          <label for="passwordInput" class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" id="passwordInput" placeholder="Password" required>
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-primary w-100">Submit</button>
      </form>
    </div>
  </template>

<script lang="ts">
    import { defineComponent } from "vue";
    import router from '../router/index'
    import { useUserStore } from '../../stores/auth';
    
    
    export default defineComponent({
        data() {
            return {
                username: '',
                password: '',
                token: '',
                loginError: false,
                loginErrorMessage: '',

            }
        },
        methods: {
          async login() {

            this.loginError = false;
            this.loginErrorMessage = '';


            const requestOptions = {
              method: "POST",
              headers: {
                "Content-type": "application/json",
              },
              body: JSON.stringify({ "username": this.username, "password": this.password})
            }

            const signup = await fetch('http://127.0.0.1:8000/api/login/', requestOptions)
            if (!signup.ok){
                this.loginError = true;
                this.loginErrorMessage  = 'Login failed. Please try again.'
                return;
            }
            var data = await signup.json() 
            const userStore = useUserStore();
            userStore.login(data.result.user, data.result.access_token)
            console.log(userStore.username)
            this.token = data.result.access_token
            router.push('/dashboard')
            alert('Login successful!')
          },
        },
    })
</script>

<style scoped>
</style>

<template>
    <div class="container mt-5">
      <form @submit.prevent="submit()" class="border p-4 bg-light">
        <h2 class="mb-4 text-center">Sign Up!</h2>
  
        <!-- First Name Field -->
        <div class="form-group mb-3">
          <label for="firstNameInput" class="form-label">First Name</label>
          <input type="text" v-model="first_name" class="form-control" id="firstNameInput" placeholder="Enter first name" required>
        </div>

        <!-- Last Name Field -->
        <div class="form-group mb-3">
          <label for="lastNameInput" class="form-label">Last Name</label>
          <input type="text" v-model="last_name" class="form-control" id="lastNameInput" placeholder="Enter last name" required>
        </div>

        <!-- Email Field -->
        <div class="form-group mb-3">
          <label for="emailInput" class="form-label">Email</label>
          <input type="email" v-model="email" class="form-control" id="emailInput" placeholder="Enter email" required>
        </div>

        <!-- Date of Birth Field -->
        <div class="form-group mb-3">
          <label for="dobInput" class="form-label">Date of Birth</label>
          <input type="date" v-model="date_of_birth" class="form-control" id="dobInput" placeholder="Enter date of birth" required>
        </div>

        <!-- Multichoice-box for hobbies-->
         <!-- The choices being fetched from an endpoint and display as dynamic multichoice options-->
        <div class="form-group mb-3">
          <label for="hobbiesInput" class="form-label">Hobbies</label>
          <select v-model="hobbies" class="form-control" id="hobbiesInput" multiple>
            <option v-for="hobby in hobbies" :key="hobby.id" :value="hobby.id">{{ hobby.name }}</option>
          </select>
        </div>
  
        <!-- Password Field -->
        <div class="form-group mb-4">
          <label for="passwordInput" class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control" id="passwordInput" placeholder="Password" required>
        </div>

        <div class="form-group mb-4">
          <label for="passwordInput2" class="form-label">Confirm Password</label>
          <input type="password" v-model="password2" class="form-control" id="passwordInput2" placeholder="Password" required>
        </div>
        <div v-if="passwordError" class="alert alert-danger">
            Passwords do not match.
        </div>
        <div v-if="userExistsError" class="alert alert-danger">
            Username already exists.
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
                    first_name: '',
                    last_name: '',
                    email: '',
                    date_of_birth: '',
                    hobbies: [],
                    password: '',
                    password2: '',
                    token: '',
                    passwordError: false,
                    userExistsError: false,
              }
          },
            async mounted() {
                const requestOptions = {
                method: "GET",
                headers: {
                    "Content-type": "application/json",
                },
                }
                const response = await fetch('http://127.0.0.1:8000/api/hobbies/', requestOptions)
                var data = await response.json()
                this.hobbies = data.result
            },
          methods: {
            async submit() {
                this.passwordError = false;
                this.userExistsError = false;

                if (this.password != this.password2) {
                    this.passwordError = true;
                    return;
                }

              const requestOptions = {
                method: "POST",
                headers: {
                  "Content-type": "application/json",
                },
                body: JSON.stringify({ "first_name": this.first_name, "last_name": this.last_name, "email": this.email, "date_of_birth": this.date_of_birth, "password": this.password, "password1": this.password, "password2": this.password2, "hobbies": this.hobbies})
              }
  
              const response = await fetch('http://127.0.0.1:8000/api/register/', requestOptions)
              const requestOptions2 = {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                },
                body: JSON.stringify({"username": this.email, "password": this.password})
                }

                if (response.status === 400) { 
                    this.userExistsError = true;
                    return;
                }


                const signup = await fetch('http://127.0.0.1:8000/api/login/', requestOptions2)
                var data = await signup.json() 
                const userStore = useUserStore();
                
                if (response.ok) {
                    userStore.login(data.result.user, data.result.access_token);
                    
                } else {
                    
                }

                this.token = data.token // Global store this
                router.push({ path: '/MainPage'})
            },
  
          },
      })
  </script>
  
  <style scoped>
  </style>
  
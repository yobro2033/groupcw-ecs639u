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

        <multiselect v-model="selectedHobbies" :options="hobbyOptions" label="name" track-by="id" multiple></multiselect>
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
import router from "../router/index";
import { useUserStore } from "../../stores/auth";
import Multiselect from 'vue-multiselect';

export default defineComponent({
  components: { Multiselect },
  data() {
    return {
      first_name: "",
      last_name: "",
      email: "",
      date_of_birth: "",
      hobbyOptions: [], // Stores the list of all available hobbies
      selectedHobbies: [], // Stores selected hobbies
      newHobby: "", // Holds the value of a new hobby being added
      password: "",
      password2: "",
      token: "",
      passwordError: false,
      userExistsError: false,
    };
  },
  async mounted() {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/hobbies/");
      const data = await response.json();
      this.hobbyOptions = data.result;
    } catch (error) {
      console.error("Failed to fetch hobbies:", error);
    }
  },
  methods: {
    async submit() {
      this.passwordError = false;
      this.userExistsError = false;

      if (this.password !== this.password2) {
        this.passwordError = true;
        return;
      }

      const requestBody = {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        date_of_birth: this.date_of_birth,
        password: this.password,
        password1: this.password,
        password2: this.password2,
        hobbies: this.selectedHobbies,
      };

      try {
        const response = await fetch("http://127.0.0.1:8000/api/register/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });

        if (response.status === 400) {
          this.userExistsError = true;
          return;
        }

        const loginResponse = await fetch("http://127.0.0.1:8000/api/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username: this.email, password: this.password }),
        });

        const loginData = await loginResponse.json();
        const userStore = useUserStore();

        if (loginResponse.ok) {
          userStore.login(loginData.result.user, loginData.result.access_token);
          router.push({ path: "/dashboard" });
        }
      } catch (error) {
        console.error("Failed to submit the form:", error);
      }
    },
    async addNewHobby() {
      if (!this.newHobby.trim()) return;

      try {
        const response = await fetch("http://127.0.0.1:8000/api/hobbies/add/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ name: this.newHobby }),
        });

        if (response.ok) {
          const newHobby = await response.json();
          this.hobbyOptions.push(newHobby);
          this.newHobby = ""; // Clear the input
        }
      } catch (error) {
        console.error("Failed to add new hobby:", error);
      }
    },
  },
});
</script>


<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

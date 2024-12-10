<template>
  <form @submit.prevent="submit" class="border p-4 bg-light">
    <div class="mb-3">
      <label for="firstNameInput" class="form-label">First Name</label>
      <input type="text" v-model="form.first_name" class="form-control" id="firstNameInput" placeholder="Enter first name" required>
    </div>
    <div class="mb-3">
      <label for="lastNameInput" class="form-label">Last Name</label>
      <input type="text" v-model="form.last_name" class="form-control" id="lastNameInput" placeholder="Enter last name" required>
    </div>
    <div class="mb-3">
      <label for="emailInput" class="form-label">Email</label>
      <input type="email" v-model="form.email" class="form-control" id="emailInput" placeholder="Enter email" required>
    </div>
    <div class="mb-3">
      <label for="dobInput" class="form-label">Date of Birth</label>
      <input type="date" v-model="form.date_of_birth" class="form-control" id="dobInput" placeholder="Enter date of birth" required>
    </div>
    <div class="mb-3">
      <label for="hobbiesInput" class="form-label">Hobbies</label>
      <multiselect v-model="selectedHobbies" :options="hobbyOptions" label="name" track-by="id" multiple></multiselect>
    </div>
    <div class="mb-3">
      <label for="passwordInput" class="form-label">Password</label>
      <input type="password" v-model="form.password" class="form-control" id="passwordInput" placeholder="Password" required>
    </div>
    <div class="mb-3">
      <label for="passwordInput2" class="form-label">Confirm Password</label>
      <input type="password" v-model="form.confirm_password" class="form-control" id="passwordInput2" placeholder="Confirm Password" required>
    </div>
    <div v-if="passwordError" class="alert alert-danger">
      Passwords do not match.
    </div>
    <div v-if="userExistsError" class="alert alert-danger">
      User already exists.
    </div>
    <button type="submit" class="btn btn-primary">Sign Up</button>
  </form>
</template>


<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";
import { useUserStore } from '../../stores/auth';
import router from '../router/index'

interface Hobby {
  id: string;
  name: string;
}

function getCookieCsrfToken(): string | null {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [name, value] = cookie.split('=');
    if (name.trim() === "csrftoken") {
      return value;
    }
  }
  return null;
}

export default defineComponent({
  components: { Multiselect },
  setup() {
    const form = ref({
      first_name: "",
      last_name: "",
      email: "",
      date_of_birth: "",
      password: "",
      confirm_password: "",
    });
    const selectedHobbies = ref<Hobby[]>([]);
    const hobbyOptions = ref<Hobby[]>([]);
    const passwordError = ref(false);
    const userExistsError = ref(false);

    const fetchHobbies = async () => {
      try {
        const response = await fetch(`/api/hobbies/`);
        const data = await response.json();
        hobbyOptions.value = data.result;
      } catch (error) {
        console.error("Failed to fetch hobbies:", error);
      }
    };

    onMounted(() => {
      console.log("Fetching hobbies...");
      fetchHobbies();
    });

    const submit = async () => {
      passwordError.value = false;
      userExistsError.value = false;

      if (form.value.password !== form.value.confirm_password) {
        passwordError.value = true;
        return;
      }

      const requestBody = {
        first_name: form.value.first_name,
        last_name: form.value.last_name,
        email: form.value.email,
        date_of_birth: form.value.date_of_birth,
        password: form.value.password,
        password1: form.value.password,
        password2: form.value.confirm_password,
        hobbies: selectedHobbies.value.map((hobby) => ({ id: hobby.id, name: hobby.name })),
      };

      try {
        const csrfToken = getCookieCsrfToken();
        const response = await fetch(`/api/register/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          body: JSON.stringify(requestBody),
        });
        const data = await response.json();
        if (data.success) {
          // login after signup
          const requestOptions = {
            method: "POST",
            headers: {
              "Content-type": "application/json",
              "X-CSRFToken": csrfToken || "",
            },
            body: JSON.stringify({ "username": requestBody.email, "password": requestBody.password})
          }

          const signup = await fetch(`/api/login/`, requestOptions)
          if (!signup.ok){
              alert("Signup successful, but login failed. Please try logging in.")
          }
          const data = await signup.json() 
          const userStore = useUserStore();
          userStore.login(data.result.user, data.result.access_token)
          router.push('/dashboard')
          alert("Signup successful");
        } else {
          if (data.error === "User already exists") {
            userExistsError.value = true;
          } else {
            alert("Signup failed: " + data.error);
          }
        }
      } catch (error) {
        console.error("Error during signup:", error);
      }
    };

    return {
      form,
      selectedHobbies,
      hobbyOptions,
      passwordError,
      userExistsError,
      submit,
    };
  },
});
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<template>
  <div class="container mt-5">
    <form @submit.prevent="login" class="border p-4 bg-light">
      <h2 class="mb-4 text-center">Log In</h2>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>

      <!-- Username Field -->
      <div class="form-group mb-3">
        <label for="usernameInput" class="form-label">Email</label>
        <input type="text" v-model="form.email" class="form-control" id="usernameInput" placeholder="Enter email" required>
      </div>

      <!-- Password Field -->
      <div class="form-group mb-4">
        <label for="passwordInput" class="form-label">Password</label>
        <input type="password" v-model="form.password" class="form-control" id="passwordInput" placeholder="Password" required>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary w-100">Submit</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import router from '../router/index';
import { useUserStore } from '../../stores/auth';

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
  setup() {
    const form = ref({
      email: "",
      password: "",
    });
    const errorMessage = ref<string | null>(null);
    const successMessage = ref<string | null>(null);

    const login = async () => {
      errorMessage.value = null;
      successMessage.value = null;

      const requestBody = {
        username: form.value.email,
        password: form.value.password,
      };

      try {
        const csrfToken = getCookieCsrfToken();
        const response = await fetch(`/api/login/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken || "",
          },
          body: JSON.stringify(requestBody),
        });
        const data = await response.json();
        if (data.success === "true") {
          const userStore = useUserStore();
          userStore.login(data.result.user);
          router.push('/dashboard');
          successMessage.value = "Login successful!";
        } else {
          errorMessage.value = data.error;
        }
      } catch (error) {
        console.error("Error during login:", error);
        errorMessage.value = "An error occurred during login. Please try again.";
      }
    };

    return {
      form,
      errorMessage,
      successMessage,
      login,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
}
.alert {
  margin-bottom: 20px;
}
</style>
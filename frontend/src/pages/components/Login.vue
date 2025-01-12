<template>
  <div class="container">
    <h1 class="text-center my-4">Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" class="form-control" placeholder="Enter username">
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" class="form-control" placeholder="Enter password">
      </div>
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      <button type="submit" class="btn btn-primary w-100">Submit</button>
    </form>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import {useUserStore} from '/stores/auth.ts';
import {useRouter} from "vue-router";
import {ref} from "vue";

export default defineComponent({
  setup() {
    const username = ref("");
    const password = ref("");
    const errorMessage = ref("");
    const userStore = useUserStore();
    const router = useRouter();

    const handleLogin = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/login/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({username: username.value, password: password.value}),
        });
        const data = await response.json();
        if (data.success === 'true') {
          // Successful login, update user store and navigate to homepage
          userStore.login(data.result.user);
          // Here you can add navigation logic, e.g. using a Vue Router for navigation
          router.push("/");
          console.log("登录成功，获取的 token:", data.result.access_token);
        } else if (data.success === 'false') {
          // Failed to log in, error message displayed
          errorMessage.value = data.error || "Invalid credentials";
        } else {
          errorMessage.value = "An unexpected error occurred during login.";
        }
      } catch (error) {
        errorMessage.value = "An error occurred during login.";
        console.error(error);
      }
    };

    return {
      username,
      password,
      errorMessage,
      handleLogin,
    };
  },
});
</script>


<style scoped>
.container {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.form-container h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

button.btn-primary {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

button.btn-primary:hover {
  background-color: #0056b3;
}
</style>
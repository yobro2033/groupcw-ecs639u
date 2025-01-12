<template>
  <div class="container">
    <h1 class="text-center my-4">Sign Up</h1>
    <form @submit.prevent="handleSignUp">
      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

      <!-- User input box -->
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" class="form-control">
      </div>
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input type="text" id="firstName" v-model="firstName" class="form-control">
      </div>
      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input type="text" id="lastName" v-model="lastName" class="form-control">
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" class="form-control">
      </div>
      <div class="form-group">
        <label for="dateOfBirth">Date of Birth</label>
        <input type="date" id="dateOfBirth" v-model="dateOfBirth" class="form-control"
               placeholder="Enter date of birth">
      </div>

      <!-- Password input box -->
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" class="form-control">
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" class="form-control">
      </div>

      <!-- Interests Multiple Choice Box -->
      <div class="form-group position-relative">
        <label for="hobbies">Hobbies</label>
        <!-- Show Selected -->
        <div class="selected-hobbies mb-2">
          <span
              v-for="(hobby, index) in selectedHobbies"
              :key="index"
              class="badge bg-primary me-1"
          >
            {{ hobby }}
            <button
                type="button"
                class="btn-close btn-close-white ms-1"
                @click="removeHobby(index)"
                aria-label="Remove"
            ></button>
          </span>
        </div>

        <!-- Show input box -->
        <div
            class="form-control"
            @click="toggleDropdown"
            :class="{ 'dropdown-active': dropdownVisible }"
        >
          <span class="text-muted">Select hobbies...</span>
        </div>

        <!-- pull-down option -->
        <ul v-if="dropdownVisible" class="dropdown-menu custom-dropdown">
          <li
              v-for="hobby in hobbies"
              :key="hobby"
              @click.stop="addHobby(hobby)"
          >
            {{ hobby }}
          </li>
        </ul>
      </div>

      <button type="submit" class="btn btn-primary w-100 mt-3">Sign Up</button>
    </form>
  </div>
</template>

<script lang="ts">
import {defineComponent, ref} from "vue";

export default defineComponent({
  setup() {
    const username = ref("");
    const firstName = ref("");
    const lastName = ref("");
    const email = ref("");
    const dateOfBirth = ref("");
    const selectedHobbies = ref<string[]>([]);
    const password = ref("");
    const confirmPassword = ref("");
    const errorMessage = ref("");
    const successMessage = ref("");
    const dropdownVisible = ref(false);

    const hobbies = ["Reading", "Traveling", "Cooking", "Gaming", "Sports"];

    // Toggles the display state of the drop-down box
    const toggleDropdown = () => {
      dropdownVisible.value = !dropdownVisible.value;
    };

    // Add interests to the selected list and close the drop-down box
    const addHobby = (hobby: string) => {
      if (!selectedHobbies.value.includes(hobby)) {
        selectedHobbies.value.push(hobby);
      }
      dropdownVisible.value = false;
    };

    // Remove Interests from Selected List
    const removeHobby = (index: number) => {
      selectedHobbies.value.splice(index, 1);
    };

    const handleSignUp = async () => {
      try {
        if (password.value !== confirmPassword.value) {
          errorMessage.value = "Passwords do not match.";
          return;
        }
        const response = await fetch('http://127.0.0.1:8000/api/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: username.value,
            first_name: firstName.value,
            last_name: lastName.value,
            email: email.value,
            date_of_birth: dateOfBirth.value,
            hobbies: selectedHobbies.value,
            password: password.value,
            confirm_password: confirmPassword.value
          })
        });
        const data = await response.json();
        if (data.success) {
          successMessage.value = data.result?.message || "Successfully created an account!";
        } else {
          errorMessage.value = data.error || "An error occurred during sign up.";
        }
      } catch (error) {
        errorMessage.value = "An error occurred during sign up.";
        console.error(error);
      }
    };


    return {
      username,
      firstName,
      lastName,
      email,
      dateOfBirth,
      selectedHobbies,
      password,
      confirmPassword,
      errorMessage,
      successMessage,
      dropdownVisible,
      hobbies,
      toggleDropdown,
      addHobby,
      removeHobby,
      handleSignUp,
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

.form-group {
  margin-bottom: 15px;
}

.selected-hobbies {
  display: flex;
  flex-wrap: wrap;
}

.selected-hobbies.badge {
  display: flex;
  align-items: center;
  padding: 0.5em 1em;
  font-size: 0.85em;
  margin-bottom: 5px;
}

.dropdown-menu {
  position: absolute;
  z-index: 1050;
  display: block;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  margin-top: 5px;
}

.custom-dropdown li {
  padding: 8px 12px;
  cursor: pointer;
}

.custom-dropdown li:hover {
  background-color: #f8f9fa;
}

.dropdown-active {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}
</style>
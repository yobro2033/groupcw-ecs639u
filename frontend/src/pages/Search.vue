<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Search Page</h1>

    <!-- Search Section -->
    <div class="search-section mb-4 p-4 shadow-sm rounded bg-white">
      <div class="search-bar mb-3">
        <input
          type="text"
          v-model="searchTerm"
          @input="searchUsers"
          placeholder="Search for a user"
          class="form-control mb-3"
        />
        <div class="age-slider">
          <label>Age Range: {{ l_age }} - {{ u_age }}</label>
          <input
            type="range"
            v-model="l_age"
            :min="minAge"
            :max="u_age"
            @input="debouncedSearchUsers"
            class="form-range"
          />
          <input
            type="range"
            v-model="u_age"
            :min="l_age"
            :max="maxAge"
            @input="debouncedSearchUsers"
            class="form-range"
          />
        </div>
      </div>
      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>
      <ul class="user-list list-group">
        <li v-for="user in users" :key="user.id" class="list-group-item d-flex justify-content-between align-items-center">
          <div class="user-info">
            <router-link :to="'/profile/' + user.id" class="profile-link">
              <img :src="user.profile_image" alt="Profile" class="profile-image" />
              <span>{{ user.first_name }} {{ user.last_name }}</span>
            </router-link>
            <p>Common hobbies: {{ user.common_hobby_count }}</p>
          </div>
          <div>
            <button
              v-if="user.isFriend"
              class="btn btn-danger"
              @click="removeFriend(user.id)"
            >
              Remove Friend
            </button>
            <button
              v-else-if="user.hasSentRequest"
              class="btn btn-warning"
              @click="cancelFriendRequest(user.id)"
            >
              Cancel Request
            </button>
            <button
              v-else-if="user.hasPendingRequest"
              class="btn btn-success"
              @click="acceptFriendRequest(user.id)"
            >
              Accept
            </button>
            <button
              v-else
              class="btn btn-primary"
              @click="sendFriendRequest(user.id)"
            >
              Add Friend
            </button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Pagination Section -->
    <div class="pagination-section mt-4 p-4 shadow-sm rounded bg-white d-flex justify-content-between align-items-center">
      <div>
        <button @click="prevPage" :disabled="currentPage === 1" class="btn btn-primary">
          Previous
        </button>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="btn btn-primary">
          Next
        </button>
      </div>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
//import { useUserStore } from "../../stores/auth";

interface User {
  id: string;
  profile_image: string;
  first_name: string;
  last_name: string;
  email: string;
  common_hobby_count: number;
  isFriend: boolean;
  hasSentRequest: boolean;
  hasPendingRequest: boolean;
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

function debounce(func: Function, wait: number) {
  let timeout: number | undefined;
  return (...args: any[]) => {
    clearTimeout(timeout);
    timeout = window.setTimeout(() => func.apply(null, args), wait);
  };
}

export default defineComponent({
  setup() {
    //const userStore = useUserStore();
    const searchTerm = ref<string>("");
    const l_age = ref<number>(12);
    const u_age = ref<number>(60);
    const users = ref<User[]>([]);
    const minAge = 12;
    const maxAge = 100;
    const errorMessage = ref<string | null>(null);
    const successMessage = ref<string | null>(null);
    const currentPage = ref<number>(1);
    const totalPages = ref<number>(1);

    const searchUsers = async () => {
      errorMessage.value = null;
      successMessage.value = null;
      if (searchTerm.value !== "" || searchTerm.value === "") {
        try {
          const response = await fetch(
            `/api/users/?search=${searchTerm.value}&l_age=${l_age.value}&u_age=${u_age.value}&page=${currentPage.value}`,
            {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                //Authorization: "Token " + userStore.token,
              },
            }
          );
          const data = await response.json();
          if (data.success === "true") {
            users.value = data.result.users || [];
            currentPage.value = data.result.current_page;
            totalPages.value = data.result.total_pages;
          } else {
            errorMessage.value = data.error;
          }
        } catch (error) {
          console.error("Error searching users:", error);
          errorMessage.value = "An error occurred while searching users.";
        }
      }
    };

    const debouncedSearchUsers = debounce(searchUsers, 100);

    const sendFriendRequest = async (userId: string) => {
      errorMessage.value = null;
      successMessage.value = null;
      try {
        const csrfToken = getCookieCsrfToken();
        const response = await fetch(
          `/api/friend_request/send/${userId}/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              //Authorization: "Token " + userStore.token,
              "X-CSRFToken": csrfToken || "",
            },
          }
        );
        const data = await response.json();
        if (data.success === "true") {
          successMessage.value = "Friend request sent!";
          searchUsers(); // Refresh the user list
        } else {
          errorMessage.value = data.error;
        }
      } catch (error) {
        console.error("Error sending friend request:", error);
        errorMessage.value = "An error occurred while sending friend request.";
      }
    };

    const cancelFriendRequest = async (userId: string) => {
      errorMessage.value = null;
      successMessage.value = null;
      try {
        const csrfToken = getCookieCsrfToken();
        const response = await fetch(
          `/api/sent_request/remove/${userId}/`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              //Authorization: "Token " + userStore.token,
              "X-CSRFToken": csrfToken || "",
            },
          }
        );
        const data = await response;
        if (data.status === 204) {
          successMessage.value = "Friend request canceled!";
          searchUsers(); // Refresh the user list
        } else {
          errorMessage.value = "An error occurred while canceling friend request.";
        }
      } catch (error) {
        console.error("Error canceling friend request:", error);
        errorMessage.value = "An error occurred while canceling friend request.";
      }
    };

    const acceptFriendRequest = async (userId: string) => {
      errorMessage.value = null;
      successMessage.value = null;
      try {
        const csrfToken = getCookieCsrfToken();
        const response = await fetch(
          `/api/friend_request/accept/${userId}/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              //Authorization: "Token " + userStore.token,
              "X-CSRFToken": csrfToken || "",
            },
          }
        );
        const data = await response.json();
        if (data.success === "true") {
          successMessage.value = "Friend request accepted!";
          searchUsers(); // Refresh the user list
        } else {
          errorMessage.value = data.error;
        }
      } catch (error) {
        console.error("Error accepting friend request:", error);
        errorMessage.value = "An error occurred while accepting friend request.";
      }
    };

    const removeFriend = async (userId: string) => {
      errorMessage.value = null;
      successMessage.value = null;
      try {
        const csrfToken = getCookieCsrfToken();
        const response = await fetch(
          `/api/friend/remove/${userId}/`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              //Authorization: "Token " + userStore.token,
              "X-CSRFToken": csrfToken || "",
            },
          }
        );
        const data = await response;
        if (data.status === 204) {
          successMessage.value = "Friend removed!";
          searchUsers(); // Refresh the user list
        } else {
          errorMessage.value = "An error occurred while removing friend.";
        }
      } catch (error) {
        console.error("Error removing friend:", error);
        errorMessage.value = "An error occurred while removing friend.";
      }
    };

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++;
        searchUsers();
      }
    };

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--;
        searchUsers();
      }
    };

    // Watch for changes in searchTerm, l_age, u_age, or currentPage and trigger search
    watch([searchTerm, currentPage], searchUsers, { immediate: true });

    return {
      searchTerm,
      l_age,
      u_age,
      users,
      minAge,
      maxAge,
      errorMessage,
      successMessage,
      currentPage,
      totalPages,
      searchUsers,
      debouncedSearchUsers,
      sendFriendRequest,
      cancelFriendRequest,
      acceptFriendRequest,
      removeFriend,
      nextPage,
      prevPage,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}
.alert {
  margin-bottom: 20px;
  margin-left: 5px;
  margin-right: 5px;
}
.search-section, .pagination-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}
.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-section .btn {
  margin: 0 10px;
}
</style>
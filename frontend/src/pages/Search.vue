<template>
  <div class="container mt-5">
    <h1>Search Page</h1>
    <div class="search-bar">
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
          @input="searchUsers"
        />
        <input
          type="range"
          v-model="u_age"
          :min="l_age"
          :max="maxAge"
          @input="searchUsers"
        />
      </div>
    </div>
    <ul class="user-list">
      <li v-for="user in users" :key="user.id" class="user-item">
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
</template>

  
  <style scoped>
  .container {
    max-width: 600px;
    margin: auto;
  }
  .search-bar {
    margin-bottom: 20px;
  }
  .age-slider {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
  }
  .age-slider input[type="range"] {
    width: 100%;
  }
  .user-list {
    list-style: none;
    padding: 0;
  }
  .user-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ccc;
    padding: 10px 0;
  }
  .user-info {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .profile-image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
  }
  .profile-link {
    text-decoration: none;
    font-weight: bold;
  }
  </style>
  
  <script lang="ts">
  import { defineComponent, ref, watch } from "vue";
  import { useUserStore } from "../../stores/auth";
  
  export default defineComponent({
    setup() {
      const searchTerm = ref("");
      const l_age = ref(18);
      const u_age = ref(60);
      const users = ref([]);
      const minAge = 18;
      const maxAge = 100;
  
      const searchUsers = async () => {
        const response = await fetch(
          `http://localhost:8000/api/users/?search=${searchTerm.value}&l_age=${l_age.value}&u_age=${u_age.value}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Token " + useUserStore().token,
            },
          }
        );
        const data = await response.json();
        users.value = data.result.users || [];
      };
  
      const sendFriendRequest = async (userId: number) => {
        await fetch(
          `http://localhost:8000/api/friend_request/send/${userId}/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Token " + useUserStore().token,
            },
          }
        );
        alert("Friend request sent!");
        searchUsers(); // Refresh the user list
      };
  
      const cancelFriendRequest = async (userId: number) => {
        // `http://127.0.0.1:8000/api/sent_request/remove/${id}/`
        await fetch(
          `http://localhost:8000/api/sent_request/remove/${userId}/`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Token " + useUserStore().token,
            },
          }
        );
        alert("Friend request canceled!");
        searchUsers(); // Refresh the user list
      };
  
      const acceptFriendRequest = async (userId: number) => {
        await fetch(
          `http://localhost:8000/api/friend_request/accept/${userId}/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Token " + useUserStore().token,
            },
          }
        );
        alert("Friend request accepted!");
        searchUsers(); // Refresh the user list
      };
  
      const removeFriend = async (userId: number) => {
        await fetch(
          `http://localhost:8000/api/friend/remove/${userId}/`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Token " + useUserStore().token,
            },
          }
        );
        alert("Friend removed!");
        searchUsers(); // Refresh the user list
      };
  
      // Watch for changes in searchTerm, l_age, or u_age and trigger search
      watch([searchTerm, l_age, u_age], searchUsers, { immediate: true });
  
      return {
        searchTerm,
        l_age,
        u_age,
        users,
        minAge,
        maxAge,
        sendFriendRequest,
        cancelFriendRequest,
        acceptFriendRequest,
        removeFriend,
      };
    },
  });
  </script>
  
  
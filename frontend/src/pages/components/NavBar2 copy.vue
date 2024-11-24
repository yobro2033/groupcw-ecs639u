<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">Home</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item">
            <div class="dropdown-container" v-click-outside="closeDropdown">
              <button @click="toggleDropdown" class="nav-link dropdown-button">
                Friend Requests
              </button>
              <div v-if="showDropdown" class="dropdown-box">
                <div class="tab-buttons">
                  <button
                    :class="{ active: activeTab === 'received' }"
                    @click="setTab('received')"
                  >
                    Received Requests
                  </button>
                  <button
                    :class="{ active: activeTab === 'sent' }"
                    @click="setTab('sent')"
                  >
                    Sent Requests
                  </button>
                </div>
                <ul>
                  <li
                    v-for="request in requests"
                    :key="request.id"
                    class="request-item"
                  >
                    <img
                      :src="request.profile_image"
                      alt="Profile"
                      class="profile-image"
                    />
                    <span>
                      {{ request.first_name }} {{ request.last_name }}
                    </span>
                    <div class="action-buttons">
                      <button
                        v-if="activeTab === 'received'"
                        @click="acceptRequest(request.id)"
                        class="btn btn-success"
                      >
                        Accept
                      </button>
                      <button
                        v-if="activeTab === 'received'"
                        @click="rejectRequest(request.id)"
                        class="btn btn-danger"
                      >
                        Reject
                      </button>
                      <button
                        v-if="activeTab === 'sent'"
                        @click="cancelRequest(request.id)"
                        class="btn btn-warning"
                      >
                        Cancel
                      </button>
                    </div>
                  </li>
                </ul>
                <p v-if="requests.length === 0">No requests available.</p>
              </div>
            </div>
          </li>
          <li>
            <router-link class="nav-link" to="/dashboard">Profile Page</router-link>
          </li>
          <li class="nav-item nav-link nav-bar-item" @click="logout()">Sign out</li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import router from "../../router";

export default defineComponent({
  data() {
    return {
      showDropdown: false,
      activeTab: "received",
      requests: [],
    };
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    closeDropdown() {
      this.showDropdown = false;
    },
    setTab(tab) {
      this.activeTab = tab;
      this.fetchRequests();
    },
    async fetchRequests() {
      const endpoint =
        this.activeTab === "received"
          ? "/api/friend_requests/"
          : "/api/sent_requests/";
      try {
        const response = await fetch(endpoint, {
          headers: {
            Authorization: "Token " + this.$store.state.token,
          },
        });
        const data = await response.json();
        if (data.success === "true") {
          this.requests = data.result;
        } else {
          console.error("Failed to fetch requests:", data.error);
        }
      } catch (error) {
        console.error("Error fetching requests:", error);
      }
    },
    async acceptRequest(id) {
      await this.handleRequest(`/api/friend_request/accept/${id}/`, "Accepted");
    },
    async rejectRequest(id) {
      await this.handleRequest(`/api/friend_request/reject/${id}/`, "Rejected");
    },
    async cancelRequest(id) {
      await this.handleRequest(`/api/sent_request/remove/${id}/`, "Canceled");
    },
    async handleRequest(url, action) {
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            Authorization: "Token " + this.$store.state.token,
          },
        });
        const data = await response.json();
        if (data.success === "true") {
          this.fetchRequests();
          alert(`${action} request successfully.`);
        } else {
          alert(`Failed to ${action.toLowerCase()} request.`);
        }
      } catch (error) {
        console.error("Error handling request:", error);
      }
    },
    async logout() {
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + this.$store.state.token, // Assuming Vuex store holds the token
        },
      };
      try {
        const response = await fetch("http://127.0.0.1:8000/api/logout/", requestOptions);
        const data = await response.json();
        if (data.done) {
          alert("Logged out successfully");
          router.push("/");
        } else {
          alert("Failed to log out");
        }
      } catch (error) {
        console.error("Logout error:", error);
      }
    },
  },
});
</script>

<style scoped>
.nav-bar-item:hover {
  cursor: pointer;
}
.dropdown-container {
  position: relative;
}
.dropdown-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}
.dropdown-box {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid #ddd;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 300px;
  padding: 10px;
}
.tab-buttons button {
  margin-right: 5px;
}
.tab-buttons .active {
  font-weight: bold;
}
.request-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
.action-buttons button {
  margin-left: 5px;
}
</style>

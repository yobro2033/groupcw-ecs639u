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
          <!-- Friend Requests Dropdown -->
          <li class="nav-item" @click="fetchRequests()">
            <div class="dropdown-container" v-click-outside="closeDropdown">
              <button @click="toggleDropdown" class="nav-link dropdown-button">
                Friend Requests
              </button>
              <div v-if="showDropdown" class="dropdown-box">
                <!-- Tab Buttons -->
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
                <!-- Requests List -->
                <div class="requests-list">
                  <div
                    v-for="request in requests"
                    :key="request.id"
                    class="request-card"
                  >
                    <img
                      :src="request.profile_image"
                      alt="Profile"
                      class="profile-image"
                    />
                    <div class="request-details">
                      <p class="name">
                        {{ request.first_name }} {{ request.last_name }}
                      </p>
                      <p class="email">{{ request.email }}</p>
                    </div>
                    <div class="action-buttons">
                      <button
                        v-if="activeTab === 'received'"
                        @click="acceptRequest(request.id)"
                        class="btn btn-success btn-sm"
                      >
                        Accept
                      </button>
                      <button
                        v-if="activeTab === 'received'"
                        @click="rejectRequest(request.id)"
                        class="btn btn-danger btn-sm"
                      >
                        Reject
                      </button>
                      <button
                        v-if="activeTab === 'sent'"
                        @click="cancelRequest(request.id)"
                        class="btn btn-warning btn-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>
                <!-- No Requests Message -->
                <p v-if="requests.length === 0" class="no-requests">
                  No requests available.
                </p>
              </div>
            </div>
          </li>

          <!-- Friend dropdown -->

          <li class="nav-item" @click="fetchFriends()">
            <div class="dropdown-container" v-click-outside="closeFriendsDropdown">
              <button @click="toggleFriendsDropdown" class="nav-link dropdown-button">
                Friends
              </button>
              <div v-if="showFriendsDropdown" class="dropdown-box">
                <div class="requests-list">
                  <div
                    v-for="friend in friends_list"
                    :key="friend.id"
                    class="request-card"
                  >
                    <img
                      :src="friend.profile_image"
                      alt="Profile"
                      class="profile-image"
                    />
                    <div class="request-details">
                      <p class="name">
                        {{ friend.first_name }} {{ friend.last_name }}
                      </p>
                      <p class="email">{{ friend.email }}</p>
                    </div>
                    <div class="action-buttons">
                      <button
                        @click="unfriendRequest(friend.id)"
                        class="btn btn-danger btn-sm"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
                <p v-if="friends_list.length === 0" class="no-requests">
                  No friends available.
                </p>
              </div>
            </div>
          </li>

          <!-- Other Links -->
          <li>
            <router-link class="nav-link" to="/dashboard">Profile Page</router-link>
          </li>
          <li>
            <router-link class="nav-link" to="/search">Search</router-link>
          </li>
          <li class="nav-item nav-link nav-bar-item" @click="logout()">
            Sign out
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import router from "../../router";
import { useUserStore } from "../../../stores/auth";

interface Request {
  id: string;
  profile_image: string;
  first_name: string;
  last_name: string;
  email: string;
}

interface Friend {
  id: string;
  profile_image: string;
  first_name: string;
  last_name: string;
  email: string;
}

function getCookieCsrfToken(): string | null {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [name, value] = cookie.split('=');
    if (name.trim() === "csrftoken") {
      return value;
    }
  }
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) {
    return meta.getAttribute('content');
  }
  return null;
}

export default defineComponent({
  directives: {
    clickOutside: {
      beforeMount(el, binding) {
        el.clickOutsideEvent = (event: Event) => {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value();
          }
        };
        document.body.addEventListener("click", el.clickOutsideEvent);
      },
      unmounted(el) {
        document.body.removeEventListener("click", el.clickOutsideEvent);
      },
    },
  },
  data() {
    return {
      showDropdown: false,
      showFriendsDropdown: false,
      activeTab: "received",
      requests: [] as Request[],
      friends_list: [] as Friend[],
      errorMessage: ref<string | null>(null),
      successMessage: ref<string | null>(null),
    };
  },
  setup() {
    const userStore = useUserStore();
    userStore.loadUser();
    return { userStore };
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    closeDropdown() {
      this.showDropdown = false;
    },
    toggleFriendsDropdown() {
      this.showFriendsDropdown = !this.showFriendsDropdown;
    },
    closeFriendsDropdown() {
      this.showFriendsDropdown = false;
    },
    setTab(activeTab: string) {
      this.activeTab = activeTab;
      this.fetchRequests();
    },
    async fetchRequests() {
      const endpoint =
        this.activeTab === "received"
          ? `/api/friend_requests/`
          : `/api/sent_requests/`;
      try {
        const response = await fetch(endpoint, {
          //headers: {
            //Authorization: "Token " + this.userStore.token,
          //},
        });
        const data = await response.json();
        if (data.success === "true") {
          this.requests = data.result;
        } else {
          this.errorMessage = data.error;
          setTimeout(() => {
            this.errorMessage = null;
          }, 5000);
        }
      } catch (error) {
        console.error("Error fetching requests:", error);
        this.errorMessage = "An error occurred while fetching requests.";
        setTimeout(() => {
          this.errorMessage = null;
        }, 5000);
      }
    },
    async fetchFriends() {
      try {
        const response = await fetch(`/api/friends/`, {
          //headers: {
          //  Authorization: "Token " + this.userStore.token,
          //},
        });
        const data = await response.json();
        if (data.success === "true") {
          this.friends_list = data.result;
        } else {
          this.errorMessage = data.error;
          setTimeout(() => {
            this.errorMessage = null;
          }, 5000);
        }
      } catch (error) {
        console.error("Error fetching friends:", error);
        this.errorMessage = "An error occurred while fetching friends.";
        setTimeout(() => {
          this.errorMessage = null;
        }, 5000);
      }
    },
    async acceptRequest(id: string) {
      await this.handleRequest(
        `/api/friend_request/accept/${id}/`,
        "Accepted",
        "POST"
      );
    },
    async unfriendRequest(id: string) {
      await this.handleRequest(
        `/api/friend/remove/${id}/`,
        "Unfriended",
        "DELETE"
      );
      this.fetchFriends();
    },
    async rejectRequest(id: string) {
      await this.handleRequest(
        `/api/friend_request/reject/${id}/`,
        "Rejected",
        "PUT"
      );
    },
    async cancelRequest(id: string) {
      await this.handleRequest(
        `/api/sent_request/remove/${id}/`,
        "Canceled",
        "DELETE"
      );
    },
    async handleRequest(url: string, action: string, method: string) {
      try {
        const csrfToken = getCookieCsrfToken();
        if (method === "DELETE") {
          const response = await fetch(url, {
            method,
            headers: {
            //  Authorization: "Token " + this.userStore.token,
              "X-CSRFToken": csrfToken || "",
            },
          });
          const data = await response;
          if (data.status === 204) {
            this.fetchRequests();
            this.fetchFriends();
            this.successMessage = `${action} request successfully.`;
            setTimeout(() => {
              this.successMessage = null;
            }, 5000);
          } else {
            this.errorMessage = "An error occurred while handling request.";
            setTimeout(() => {
              this.errorMessage = null;
            }, 5000);
          }
          return;
        } else {
          const response = await fetch(url, {
            method,
            headers: {
              //Authorization: "Token " + this.userStore.token,
              "X-CSRFToken": csrfToken || "",
            },
          });
          const data = await response.json();
          if (data.success === "true") {
            this.fetchRequests();
            this.successMessage = `${action} request successfully.`;
            setTimeout(() => {
              this.successMessage = null;
            }, 5000);
          } else {
            this.errorMessage = data.error;
            setTimeout(() => {
              this.errorMessage = null;
            }, 5000);
          }
        }
      } catch (error) {
        console.error("Error handling request:", error);
        this.errorMessage = `An error occurred while ${action.toLowerCase()} request.`;
        setTimeout(() => {
          this.errorMessage = null;
        }, 5000);
      }
    },
    async logout() {
      const csrfToken = getCookieCsrfToken();
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          //Authorization: "Token " + this.userStore.token,
          "X-CSRFToken": csrfToken || "",
        },
      };
      const loggedOut = await fetch(
        `/api/logout/`,
        requestOptions
      );
      const data = await loggedOut.json();
      if (data.success === "true") {
        this.successMessage = "Logged out successfully";
        setTimeout(() => {
          this.successMessage = null;
        }, 5000);
        this.userStore.logout();
        router.push("/");
      } else {
        this.errorMessage = "Error logging out";
        setTimeout(() => {
          this.errorMessage = null;
        }, 5000);
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
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 350px;
  padding: 15px;
}
.tab-buttons {
  display: flex;
  justify-content: space-around;
  margin-bottom: 10px;
}
.tab-buttons button {
  background-color: #f8f9fa;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}
.tab-buttons button:hover {
  background-color: #e2e6ea;
}
.tab-buttons .active {
  font-weight: bold;
  background-color: #e2e6ea;
}
.requests-list {
  max-height: 300px;
  overflow-y: auto;
}
.request-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f8f9fa;
  transition: box-shadow 0.3s ease;
}
.request-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}
.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}
.request-details {
  flex-grow: 1;
  margin-left: 10px;
}
.request-details .name {
  font-weight: bold;
  margin: 0;
}
.request-details .email {
  font-size: 0.9rem;
  color: #6c757d;
}
.action-buttons {
  display: flex;
  gap: 5px;
}
.no-requests {
  text-align: center;
  color: #6c757d;
  margin-top: 10px;
}
</style>
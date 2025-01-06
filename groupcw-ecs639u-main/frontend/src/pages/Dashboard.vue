<template>
  <div class="container mt-5">
    <h1>User Dashboard</h1>

    <!-- Profile Section -->
    <div class="profile-section mb-4">
      <h3>Your Profile</h3>
      <div v-if="userProfile">
        <img
          :src="userProfile.profile_image"
          alt="Profile Picture"
          class="profile-image mb-3"
        />
        <div>
          <label>First Name:</label>
          <input
            type="text"
            v-model="editProfile.first_name"
            class="form-control mb-2"
          />
        </div>
        <div>
          <label>Last Name:</label>
          <input
            type="text"
            v-model="editProfile.last_name"
            class="form-control mb-2"
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            v-model="editProfile.email"
            class="form-control mb-2"
          />
        </div>
        <div>
          <label>Date of Birth:</label>
          <input
            type="date"
            v-model="editProfile.date_of_birth"
            class="form-control mb-2"
          />
        </div>
        <div>
          <label>Hobbies:</label>
          <Multiselect
            v-model="editProfile.selectedHobbies"
            :options="hobbiesList"
            :multiple="true"
            :searchable="true"
            :taggable="true"
            label="name"
            track-by="id"
            placeholder="Select or add hobbies"
            @tag="addNewHobbyOption"
          ></Multiselect>
          <div v-if="showNewHobbyForm" class="mt-3">
            <label>New Hobby Name:</label>
            <input
              type="text"
              v-model="newHobby.name"
              placeholder="Enter hobby name"
              class="form-control mb-2"
            />
            <label>New Hobby Description:</label>
            <input
              type="text"
              v-model="newHobby.description"
              placeholder="Enter hobby description"
              class="form-control mb-2"
            />
            <button @click="addNewHobby" class="btn btn-primary">
              Add Hobby
            </button>
          </div>
        </div>
        <br />
        <button @click="updateProfile" class="btn btn-primary">
          Save Profile
        </button>
      </div>
    </div>

    <!-- Change Password Section -->
    <div class="change-password-section">
      <h3>Change Password</h3>
      <button class="btn btn-danger" @click="showPasswordModal = true">
        Change Password
      </button>
    </div>

    <!-- Change Password Modal -->
    <div
      v-if="showPasswordModal"
      class="modal"
      tabindex="-1"
      role="dialog"
      style="display: block"
    >
      <div class="modal-dialog" role="document">
          <div class="modal-header">
            <h5 class="modal-title">Update Password</h5>
          </div>
          <div class="modal-body">
            <div>
              <label>Old Password:</label>
              <input
                type="password"
                v-model="passwordForm.old_password"
                class="form-control mb-2"
              />
            </div>
            <div>
              <label>New Password:</label>
              <input
                type="password"
                v-model="passwordForm.new_password"
                class="form-control mb-2"
              />
            </div>
            <div>
              <label>Confirm New Password:</label>
              <input
                type="password"
                v-model="passwordForm.new_password_confirm"
                class="form-control mb-2"
              />
            </div>
          </div>
          <div v-if="modalErrorMessage" class="alert alert-danger">
            {{ modalErrorMessage }}
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-warning"
              @click="changePassword"
            >
              Update Password
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeChangePasswordModal"
            >
              Close
            </button>
          </div>
        </div>
    </div>

    <br>

    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";
import { useUserStore } from '../../stores/auth';

interface Hobby {
  id: string;
  name: string;
  description: string;
}

interface UserProfile {
  profile_image: string;
  first_name: string;
  last_name: string;
  email: string;
  date_of_birth: string;
  hobbies: Hobby[];
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
    const userStore = useUserStore();
    const userProfile = ref<UserProfile | null>(null);
    const hobbiesList = ref<Hobby[]>([]);
    const editProfile = ref({
      first_name: "",
      last_name: "",
      email: "",
      date_of_birth: "",
      selectedHobbies: [] as Hobby[],
    });
    const newHobby = ref({ name: "", description: "" });
    const showNewHobbyForm = ref(false);
    const passwordForm = ref({
      old_password: "",
      new_password: "",
      new_password_confirm: "",
    });
    const showPasswordModal = ref(false);
    const errorMessage = ref<string | null>(null);
    const modalErrorMessage = ref<string | null>(null);
    const successMessage = ref<string | null>(null);

    const loadProfile = async () => {
      try {
        const response = await fetch(`/api/my_profile`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + userStore.token,
          },
        });
        const data = await response.json();
        if (data.success === "true") {
          userProfile.value = data.result;
          if (userProfile.value) {
            editProfile.value = {
              first_name: userProfile.value.first_name,
              last_name: userProfile.value.last_name,
              email: userProfile.value.email,
              date_of_birth: userProfile.value.date_of_birth,
              selectedHobbies: userProfile.value.hobbies.map((hobby) => hobby),
            };
          }
        } else {
          errorMessage.value = data.error;
        }
      } catch (error) {
        console.error("Error loading profile:", error);
        errorMessage.value = "An error occurred while loading profile.";
      }
    };

    const loadHobbiesList = async () => {
      try {
        const response = await fetch(`/api/hobbies/`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        if (data.success === "true") {
          hobbiesList.value = data.result;
        } else {
          errorMessage.value = data.error;
        }
      } catch (error) {
        console.error("Error loading hobbies list:", error);
        errorMessage.value = "An error occurred while loading hobbies list.";
      }
    };

    const updateProfile = async () => {
      errorMessage.value = null;
      successMessage.value = null;
      try {
        const selectedHobbies = editProfile.value.selectedHobbies.filter(
          (hobby) => hobby && hobby.id !== "add_new"
        );
        const selectedHobbyIds = selectedHobbies.map((hobby) => hobby.id);

        const csrfToken = getCookieCsrfToken();
        const response = await fetch(`/api/profile/update/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + userStore.token,
            "X-CSRFToken": csrfToken || "",
          },
          body: JSON.stringify({
            first_name: editProfile.value.first_name,
            last_name: editProfile.value.last_name,
            email: editProfile.value.email,
            date_of_birth: editProfile.value.date_of_birth,
            hobbies: selectedHobbyIds,
          }),
        });
        const data = await response.json();
        if (data.success === "true") {
          successMessage.value = "Profile updated successfully!";
          loadProfile();
        } else {
          errorMessage.value = data.error;
        }
      } catch (error) {
        console.error("Error updating profile:", error);
        errorMessage.value = "An error occurred while updating profile.";
      }
    };

    const addNewHobbyOption = (newTag: string) => {
      newHobby.value.name = newTag;
      showNewHobbyForm.value = true;
    };

    const addNewHobby = async () => {
      errorMessage.value = null;
      successMessage.value = null;
      try {
        const csrfToken = getCookieCsrfToken();
        const response = await fetch(`/api/hobbies/add/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + userStore.token,
            "X-CSRFToken": csrfToken || "",
          },
          body: JSON.stringify(newHobby.value),
        });
        const data = await response.json();
        if (data.success === "true") {
          hobbiesList.value.push(data.result);
          editProfile.value.selectedHobbies.push(data.result);
          newHobby.value = { name: "", description: "" };
          showNewHobbyForm.value = false;
          successMessage.value = "New hobby added successfully!";
        } else {
          errorMessage.value = data.error;
        }
      } catch (error) {
        console.error("Failed to add new hobby:", error);
        errorMessage.value = "An error occurred while adding new hobby.";
      }
    };

    const showChangePasswordModal = () => {
      showPasswordModal.value = true;
    };

    const closeChangePasswordModal = () => {
      showPasswordModal.value = false;
    };

    const changePassword = async () => {
      modalErrorMessage.value = null;
      successMessage.value = null;
      try {
        if (passwordForm.value.new_password !== passwordForm.value.new_password_confirm) {
          modalErrorMessage.value = "New passwords do not match.";
          return;
        }

        if (passwordForm.value.new_password.length < 8) {
          modalErrorMessage.value = "New password must be at least 8 characters long.";
          return;
        }

        const csrfToken = getCookieCsrfToken();
        const response = await fetch(`/api/profile/change_password/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + userStore.token,
            "X-CSRFToken": csrfToken || "",
          },
          body: JSON.stringify(passwordForm.value),
        });
        const data = await response.json();
        if (data.success === "true") {
          successMessage.value = "Password changed successfully!";
          passwordForm.value = {
            old_password: "",
            new_password: "",
            new_password_confirm: "",
          };
          closeChangePasswordModal();
        } else {
          modalErrorMessage.value = data.error;
        }
      } catch (error) {
        console.error("Error changing password:", error);
        modalErrorMessage.value = "An error occurred while changing password.";
      }
    };

    onMounted(() => {
      loadProfile();
      loadHobbiesList();
    });

    return {
      userProfile,
      hobbiesList,
      editProfile,
      newHobby,
      showNewHobbyForm,
      passwordForm,
      showPasswordModal,
      errorMessage,
      modalErrorMessage,
      successMessage,
      updateProfile,
      addNewHobbyOption,
      addNewHobby,
      showChangePasswordModal,
      closeChangePasswordModal,
      changePassword,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
}
.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}
.alert {
  margin-bottom: 20px;
  margin-left: 5px;
  margin-right: 5px;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-dialog {
  margin: 10% auto;
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}
</style>

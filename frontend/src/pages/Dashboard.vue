<template>
  <div class="container mt-5">
    <h1>User Dashboard</h1>

    <!-- Profile Section -->
    <div class="profile-section mb-4">
      <h3>Your Profile</h3>
      <div v-if="userProfile">
        <img :src="userProfile.profile_image" alt="Profile Picture" class="profile-image mb-3" />
        <div>
          <label>First Name:</label>
          <input type="text" v-model="editProfile.first_name" class="form-control mb-2" />
        </div>
        <div>
          <label>Last Name:</label>
          <input type="text" v-model="editProfile.last_name" class="form-control mb-2" />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" v-model="editProfile.email" class="form-control mb-2" />
        </div>
        <div>
          <label>Date of Birth:</label>
          <input type="date" v-model="editProfile.date_of_birth" class="form-control mb-2" />
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
            <label>Description:</label>
            <textarea
              v-model="newHobby.description"
              placeholder="Enter hobby description"
              class="form-control mb-2"
            ></textarea>
            <button class="btn btn-primary" @click="addNewHobby">Add Hobby</button>
          </div>
        </div>
        <button class="btn btn-primary" @click="updateProfile">Save Profile</button>
      </div>
    </div>

    <!-- Change Password Section -->
    <div class="change-password-section">
      <h3>Change Password</h3>
      <button class="btn btn-warning" @click="showChangePassword = true">Change Password</button>
    </div>

    <!-- Change Password Modal -->
    <div v-if="showChangePassword" class="modal-overlay">
      <div class="modal-content">
        <h3>Change Password</h3>
        <div>
          <label>Old Password:</label>
          <input type="password" v-model="passwordForm.old_password" class="form-control mb-2" />
        </div>
        <div>
          <label>New Password:</label>
          <input type="password" v-model="passwordForm.new_password" class="form-control mb-2" />
        </div>
        <div>
          <label>Confirm New Password:</label>
          <input
            type="password"
            v-model="passwordForm.new_password_confirm"
            class="form-control mb-2"
          />
        </div>
        <button class="btn btn-primary" @click="changePassword">Submit</button>
        <button class="btn btn-secondary" @click="showChangePassword = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";
import { useUserStore } from "../../stores/auth";

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

function getCsrfToken(): string | null {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute('content') : null;
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
    const showChangePassword = ref(false);

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
        loadHobbiesList();
      } catch (error) {
        console.error("Error loading profile:", error);
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
        hobbiesList.value = data.result;
      } catch (error) {
        console.error("Error loading hobbies list:", error);
      }
    };

    const updateProfile = async () => {
      try {
        const selectedHobbies = editProfile.value.selectedHobbies.filter(
          (hobby) => hobby && hobby.id !== "add_new"
        );
        const selectedHobbyIds = selectedHobbies.map((hobby) => hobby.id);

        await fetch(`/api/profile/update/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + userStore.token,
          },
          body: JSON.stringify({
            first_name: editProfile.value.first_name,
            last_name: editProfile.value.last_name,
            email: editProfile.value.email,
            date_of_birth: editProfile.value.date_of_birth,
            hobbies: selectedHobbyIds,
          }),
        });

        alert("Profile updated successfully!");
        loadProfile();
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    };

    const addNewHobbyOption = (newTag: string) => {
      newHobby.value.name = newTag;
      showNewHobbyForm.value = true;
    };

    const addNewHobby = async () => {
      try {
        const response = await fetch(`/api/hobbies/add/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + userStore.token,
          },
          body: JSON.stringify(newHobby.value),
        });
        const data = await response.json();
        hobbiesList.value.push(data.result);
        editProfile.value.selectedHobbies.push(data.result);
        newHobby.value = { name: "", description: "" };
        showNewHobbyForm.value = false;
      } catch (error) {
        console.error("Failed to add new hobby:", error);
      }
    };

    const changePassword = async () => {
      try {
        const csrfToken = getCsrfToken();
        const response = await fetch(`/api/profile/change_password/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Token " + userStore.token,
            "X-CSRFToken": csrfToken || "",
          },
          body: JSON.stringify(passwordForm.value),
        });
        if (response.status === 200) {
          alert("Password changed successfully!");
          showChangePassword.value = false;
        } else {
          alert("Failed to change password. Please try again.");
        }
      } catch (error) {
        console.error("Error changing password:", error);
      }
    };

    onMounted(() => {
      loadProfile();
    });

    return {
      userProfile,
      hobbiesList,
      editProfile,
      newHobby,
      showNewHobbyForm,
      passwordForm,
      showChangePassword,
      updateProfile,
      addNewHobbyOption,
      addNewHobby,
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
.modal-overlay {
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
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}
</style>

import { defineStore } from 'pinia';

// Use the correct casing for the type
type Token = string;

export const useUserStore = defineStore('user', {
  state: () => ({
    username: null as string | null,
    token: null as Token | null,
  }),
  actions: {
    login(username: string) {
      // Use the correct casing for the type
      this.username = username;
    },
    logout() {
      this.username = null;
    },
    async loadUser() {
      const response = await fetch('/api/my_profile');
      if (response.ok) {
          const data = await response.json();
          if (data.success === 'true') {
              this.username = data.result.email || '';
          }
      }
  }
  },
});

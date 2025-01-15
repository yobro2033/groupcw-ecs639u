import { defineStore } from 'pinia';

// Use the correct casing for the type
type Token = string;

export const useUserStore = defineStore('user', {
  state: () => ({
    username: null as string | null,
    token: null as Token | null,
  }),
  actions: {
    login(username: string, token: Token) {
      // Use the correct casing for the type
      this.username = username;
      this.token = token;
    },
    logout() {
      this.username = null;
      this.token = null;
    },
  },
});

import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        username: null,
        token: null,
        isLoggedIn: false
    }),
    actions: {
        login(username, token) {
            this.username = username;
            this.token = token;
            this.isLoggedIn = true;
        },
        logout() {
            this.username = null;
            this.token = null;
            this.isLoggedIn = false;
        }
    }
});

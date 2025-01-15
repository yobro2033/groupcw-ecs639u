// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/other/', name: 'Other Page', component: OtherPage },
        //{ path: '/login', name: 'Login', component: () => window.location.href = '/login/' },
        //{ path: '/signup', name: 'Register', component: () => window.location.href = '/signup/' },
        { path: '/dashboard', name: 'Dashboard', component: () => import('../pages/Dashboard.vue') },
        { path: '/search', name: 'Search', component: () => import('../pages/Search.vue') },
    ]
})

export default router

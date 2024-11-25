<template>
  <div class="h1">
    {{ title }}
  </div>
  <div class="container mt-5" v-if="userStore.username">
    Hello, {{ userStore.username }}!
  </div>
  <div class="container mt-5" v-else>
    You need to log in to see this page.
  </div>
</template>

<script lang="ts">
    import { defineComponent } from "vue";
    import { useUserStore } from "../../stores/auth";

    export default defineComponent({
        data() {
            return {
                title: "Hobbies app",
            }
        },
        setup(){
            const userStore = useUserStore();
            return { userStore };
          }
    })
</script>

<style scoped>
</style>

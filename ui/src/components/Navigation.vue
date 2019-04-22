<template>
<div class="nav flex-column nav-pills mt-5" role="tablist" aria-orientation="vertical">
     <router-link
          class="nav-link bg-dark text-white mt-1"
          :to="{ name: 'Home' }">Home</router-link>
     <router-link
          class="nav-link bg-dark text-white mt-1"
          :to="{ name: 'Topics' }">Topics</router-link>
     <router-link
          class="nav-link bg-dark text-white mt-1"
          :to="{ name: 'Subscriptions' }">Subscriptions</router-link>
     <router-link
          v-if="this.$parent.isAuthenticated"
          class="nav-link bg-dark text-white mt-1"
          :to="{ name: 'logout' }">Logout</router-link>
</div>
</template>

<script>
    export default {
        name: "Navigation",
        props: {
          tabs: Array
        },
    }
</script>

<style scoped>

</style>
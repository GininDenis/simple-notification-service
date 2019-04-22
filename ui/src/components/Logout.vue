<template>

</template>

<script>
    import axios from 'axios';

    export default {
        name: "Logout",
        mounted() {
            if (confirm('Do you really want to logout?')) {
                 axios.get('/api/logout')
                .then(() => {
                    this.$parent.isAuthenticated = false;
                    this.$router.push('login');
                })
                .catch(error => {
                    console.log(error)
                });
            }
            else {
                this.$router.back()
            }
        }
    }
</script>

<style scoped>

</style>
<template>
    <div class="d-flex align-items-center flex-column justify-content-center h-100 bg-dark text-white">
        <h2 class="display-4">Login</h2>
        <form method="post" class="mt-5" id="login-form"
              v-on:submit.prevent="login()">
            <div class="form-group">
                <input type="text" name="email" v-model="email"  autocomplete="username"
                       placeholder="E-mail"/>
            </div>
            <div class="form-group">
                <input type="password" name="password" v-model="password"  autocomplete="current-password"
                       placeholder="Password"/>
            </div>
            <button class="btn btn-outline-light btn-lg btn-block">Login
            </button>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Login",
        data() {
            return {
                email: "",
                password: ""
            }
        },
        methods: {
            login() {
                if (this.email !== "" && this.password !== "") {
                    axios.post('/api/login/', {
                            email: this.email,
                            password: this.password
                        })
                        .then(response => {
                            this.$router.push('/');
                            this.$emit("authenticated", true);
                        })
                        .catch(error => {
                            console.log(error)
                        });

                }
            }
        }
    }
</script>

<style scoped>

</style>
<template>
    <div id="app" class="vh-100">
        <transition-group class="col-3 position-absolute message-container"
                          tag="div" name="flash-message">
        <FlashMessage v-for="message in messages"
                    :message=message
                    :key=message.id
                    class="flash-message-item"></FlashMessage>
        </transition-group>
            <div v-if="isLoading" class="d-flex justify-content-center mt-5">
            <div class="spinner-border text-primary"
                 role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>
        <div v-else class="vh-100">
            <div class="col-2 float-left" role="navigation">
                <Navigation v-if="isAuthenticated"
                            v-bind:tabs=items></Navigation>
            </div>
            <router-view @authenticated="setAuthenticated"
                        @showMessage="addMessage"></router-view>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import Navigation from './components/Navigation'
    import FlashMessage from './components/FlashMessage'


    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';

    export default {
        name: 'app',
        mounted() {
            this.isLoading = true;
            if (!this.isAuthenticated) {
                axios.get('/api/restore/session')
                    .then(response => {
                        if (response.data['is_authenticated'] === true) {
                            this.isAuthenticated = true
                        } else {
                            this.$router.push('login')
                        }
                    })
                    .catch(error => {
                        console.log(error);
                        this.$router.replace('login')
                    })
                    .then(() => {
                        console.log('Finally');
                        this.isLoading = false;
                    });
            }
        },

        data() {
            return {
                isLoading: false,
                isAuthenticated: false,
                items: [],
                messages: [],
                message_counter: 0
            }
        },
        components: {
            Navigation,
            FlashMessage
        },
        methods: {
            setAuthenticated(status) {
                this.isAuthenticated = status;
            },
            addMessage(type, message) {
                this.messages.push({
                    type: type,
                    message: message,
                    id: this.message_counter
                });
                this.message_counter++;
                let self = this;
                setTimeout(function () {
                    self.messages.shift()
                }, 6000)
            }
        }
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }
    .message-container {
        z-index: 1;
        right: 1rem;
    }

</style>

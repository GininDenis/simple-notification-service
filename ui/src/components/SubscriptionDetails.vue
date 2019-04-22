<template>
    <div class="col-10 float-right">
        <h1 class="display-4 text-center mb-3">{{ pageHeader }}</h1>
        <form class="col-5 m-auto" method="post" v-on:submit.prevent="addSubscription()">
            <div class="form-group">
                <label class="font-weight-bold mr-1"
                       for="endpoint">Endpoint</label>
                <input class="form-control" id="endpoint" v-model="endpoint" required/>
                <div class="invalid-feedback">
                    {{ invalidEndpointMessage }}
                </div>
            </div>
            <div class="form-group">
                <label class="font-weight-bold mr-1"
                       for="protocol">Protocol</label>
                <select class="form-control" id="protocol" v-model="protocol" required>
                    <option v-for="protocol in protocolChoises"
                            :value=protocol>{{ protocol }}
                    </option>
                </select>

            </div>
            <div class="form-group">
                <label class="font-weight-bold mr-1" for="topic">Topic</label>
                <v-select :options=topics
                          :filterable=false
                          v-model=topic
                          placeholder="Type Topic name to search"
                          @search="onSearch"
                          id="topic">
                    <template slot="no-options">
                        no topics..
                    </template>
                </v-select>
            </div>
            <button type="submit"
                    class="btn btn-outline-success">{{ buttonCaption }}
            </button>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';
    import {_} from 'vue-underscore';
    import $ from 'jquery';

    export default {
        name: "SubscriptionDetails",
        data() {
            return {
                protocolChoises: ['http', 'https'],
                topics: [],
                pageHeader: "Create Subscription",
                buttonCaption: "Create",
                successMessage: "Subscription Created",
                endpoint: "",
                protocol: "",
                topic: null,
                id: "",
                invalidEndpointMessage: ""
            }
        },
        mounted() {
            if (Object.keys(this.$route.params).length !== 0) {
                this.endpoint = this.$route.params.subscription.endpoint;
                this.id = this.$route.params.subscription.id;
                this.protocol = this.$route.params.subscription.protocol;
                this.topic = this.$route.params.subscription.topic_title;
                this.pageHeader = "Update Subscription";
                this.buttonCaption = "Update";
                this.successMessage = "Subscription Updated";
            }
        },
        methods: {
            onSearch(search, loading) {
                loading(true);
                this.search(loading, search, this);
                },
            search: _.debounce((loading, search, vm) => {
                axios.get(
                    `/api/topics/?title=${escape(search)}`
                ).then(response => {
                    let data = response.data.results;

                    data = data.map(topic => {
                        return {
                            label: topic.title,
                            value: topic.id
                        }
                    });
                    console.log(data);
                    vm.topics = data;
                    loading(false);
                });
            }, 350),
            addSubscription() {
                let method = (this.id !== "") ? 'patch' : 'post';
                let url = '/api/subscriptions/';
                if (this.id !== "") {
                    url = url + this.id + '/'
                }

                axios({
                    method: method,
                    url: url,
                    data: {
                        endpoint: this.endpoint,
                        topic: this.topic.value,
                        protocol: this.protocol
                    }
                })
                    .then(() => {
                        this.$emit('showMessage', 'success', this.successMessage);
                        this.$router.push({name: 'Subscriptions'})
                    })
                    .catch(error => {
                        let data = error.response.data;
                        this.invalidEndpointMessage = data.endpoint;
                        $('#endpoint').addClass('is-invalid')
                    });
            }
        }
    }
</script>

<style scoped>
    .v-select .dropdown li {
        border-bottom: 1px solid rgba(112, 128, 144, 0.1);
    }

    .v-select .dropdown li:last-child {
        border-bottom: none;
    }

    .v-select .dropdown li a {
        padding: 10px 20px;
        width: 100%;
        font-size: 1.25em;
        color: #3c3c3c;
    }

    .v-select .dropdown-menu .active > a {
        color: #fff;
    }
</style>
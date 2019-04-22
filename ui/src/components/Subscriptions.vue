<template>
    <div class="col-10 float-right">
        <h1 class="display-4 text-center mb-3">Subscriptions</h1>
        <table class="table table-sm table-hover">
            <thead class="thead-dark">
            <tr>
                <th>Protocol</th>
                <th>Endpoint</th>
                <th>Topic</th>
                <th>Edit</th>
                <th>Remove</th>
            </tr>
            </thead>
            <tr v-for="subscription in paginator.records" :key="subscription.id">
                <td>{{ subscription.protocol }}</td>
                <td>{{ subscription.endpoint }}</td>
                <td>{{ subscription.topic_title }}</td>
                <td>
                    <router-link
                            class="btn btn-sm btn-outline-warning"
                            :to="{ name: 'SubscriptionDetails', params: { subscription: subscription } }">
                        <i class="far fa-edit"></i>
                    </router-link>
                </td>
                <td>
                    <button
                            class="btn btn-sm btn-outline-danger"
                            v-on:click="showConfirm(subscription)"
                            type="button">
                        <i class="far fa-trash-alt"></i>
                    </button>
                </td>
            </tr>
        </table>
        <router-link
                class="btn btn-outline-success float-left"
                :to="{name: 'SubscriptionDetails'}">
            <i class="fas fa-plus">&nbsp</i>Add new subscription
        </router-link>
        <Pagination v-bind:paginator=paginator></Pagination>
    </div>
</template>

<script>
    import Pagination from './Pagination'
    import Paginator from '../assets/js/paginator'
    import axios from 'axios'

    export default {
        name: "Subscriptions",
        data() {
            return {
                paginator: new Paginator('/api/subscriptions')
            }
        },
        mounted() {
            this.paginator.fetch()
        },
        methods: {
            showConfirm (subscription) {
                let result = confirm('Remove subscription?');
                if (result) {
                    axios.delete(`/api/subscriptions/${subscription.id}/`)
                        .then(() => {
                            let pos = this.paginator.records.indexOf(subscription);
                            this.paginator.records.splice(pos, 1);
                            this.$emit('showMessage', 'warning', 'Topic Removed');
                        })
                        .catch(error => {
                            console.log(error);
                            alert('Error when remove topic')
                        })
                }
            }
        },
        components: {
            Pagination
        },

    }

</script>

<style scoped>

</style>
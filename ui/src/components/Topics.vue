<template>
    <div class="col-10 float-right">
        <h1 class="display-4 text-center mb-3">Topics</h1>
        <table class="table table-sm table-hover">
            <thead class="thead-dark">
            <tr>
                <th>Owner</th>
                <th>Title</th>
                <th>Edit</th>
                <th>Remove</th>
            </tr>
            </thead>
            <tr v-for="topic in paginator.records" :key="topic.id">
                <td>{{ topic.owner }}</td>
                <td>{{ topic.title }}</td>
                <td>
                    <router-link
                            class="btn btn-sm btn-outline-warning"
                            :to="{ name: 'TopicDetails', params: { topic: topic } }">
                        <i class="far fa-edit"></i>
                    </router-link>
                </td>
                <td>
                    <button
                            class="btn btn-sm btn-outline-danger"
                            v-on:click="showConfirm(topic)"
                            type="button">
                        <i class="far fa-trash-alt"></i>
                    </button>
                </td>
            </tr>
        </table>
        <router-link
                class="btn btn-outline-success float-left"
                :to="{ name: 'TopicDetails'}">
            <i class="fas fa-plus">&nbsp</i>Add new topic
        </router-link>
        <Pagination v-bind:paginator=paginator></Pagination>
    </div>
</template>

<script>
    import Pagination from './Pagination'
    import Paginator from '../assets/js/paginator'
    import axios from 'axios'

    export default {
        name: "Topics",
        data() {
            return {
                paginator: new Paginator('/api/topics')
            }
        },
        mounted() {
            this.paginator.fetch()
        },
        methods: {
            showConfirm (topic) {
                let result = confirm('Remove topic?');
                if (result) {
                    axios.delete(`/api/topics/${topic.id}/`)
                        .then(() => {
                            let pos = this.paginator.records.indexOf(topic);
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
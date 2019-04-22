<template>
    <div class="col-10 float-right">
        <h1 class="display-4 text-center mb-3">{{ pageHeader }}</h1>
        <form method="post" class="col-5 m-auto" v-on:submit.prevent="addTopic()">
            <div class="form-group">
                <label class="font-weight-bold mr-1" for="title">Title</label>
                <input class="form-control" id="title" v-model="title"/>
            </div>
            <button type="submit"
                    class="btn btn-outline-success">{{ buttonCaption }}
            </button>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "TopicDetails",
        data() {
            return {
                pageHeader: "Create topic",
                buttonCaption: "Create",
                successMessage: "Topic Created",
                title: "",
                id: "",
            }
        },
        mounted() {
            if (Object.keys(this.$route.params).length !== 0) {
                this.title = this.$route.params.topic.title;
                this.id = this.$route.params.topic.id;
                this.pageHeader = "Update topic";
                this.buttonCaption = "Update";
                this.successMessage = "Topic Updated";
            }
        },
        methods: {
            addTopic() {
                let method = (this.id !== "") ? 'patch': 'post';
                let url = '/api/topics/' ;
                if (this.id !== "") {
                    url = url + this.id + '/'
                }

                axios({
                    method: method,
                    url: url,
                    data: {
                        title: this.title
                    }})
                        .then(response => {
                            this.$emit('showMessage', 'success', this.successMessage);
                            this.$router.push({name: 'Topics'})
                        })
                        .catch(error => {
                            console.log(error)
                        });
            }
        }
    }
</script>

<style scoped>

</style>
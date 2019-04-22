<template>
    <nav>
        <ul class="pagination">
            <li class="page-item" v-if="paginator.prev">
                <a class="page-link text-dark"
                    :href="paginator.prev"
                    v-on:click.prevent="changePage"
                    aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            <li class="page-item" v-if="paginator.next">
                <a class="page-link text-dark"
                    :href="paginator.next"
                    v-on:click.prevent="changePage"
                    aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
        </ul>
    </nav>
</template>

<script>
    export default {
        name: "Pagination",
        props: ['paginator'],
        methods: {
            changePage(event) {
                this.paginator.fetch(event.target.href);
                event.target.blur()
            }
        }
    }
</script>

<style scoped>

</style>
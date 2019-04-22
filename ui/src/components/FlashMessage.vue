<template>
    <div role="alert"
         class="flash-message-item"
         v-bind:class=message.type
         aria-live="assertive" aria-atomic="true" data-delay="1000">
        {{ message.message }}
    </div>
</template>

<script>
    export default {
        name: "FlashMessage",
        props: ['message']
    }
</script>

<style scoped>
    .flash-message-item {
        transition: all 1s;
        border-radius: 0.2rem;
        margin: 0.1rem;
    }
    .flash-message-enter, .flash-message-leave-active {
        transform: translateY(-30px);
        opacity: 0;
    }
    .info {
        background: rgba(0, 100, 255, 0.3);
    }

    .success {
        background: rgba(0, 255, 100, 0.3);
    }

    .warning {
        background: rgba(255, 10, 10, 0.3);
    }

</style>
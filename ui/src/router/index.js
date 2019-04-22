import Vue from 'vue'
import Router from 'vue-router'
import Topics from '../components/Topics'
import TopicDetails from '../components/TopicDetails'
import Subscriptions from '../components/Subscriptions'
import SubscriptionDetails from '../components/SubscriptionDetails'
import Home from '../components/Home'
import Login from '../components/Login'
import Logout from '../components/Logout'

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home
        },
        {
            path: '/topics',
            name: 'Topics',
            component: Topics
        },
        {
            path: '/topics/details',
            name: 'TopicDetails',
            component: TopicDetails
        },
        {
            path: '/subscriptions',
            name: 'Subscriptions',
            component: Subscriptions
        },
         {
            path: '/subscriptions/details',
            name: 'SubscriptionDetails',
            component: SubscriptionDetails
        },
        {
            path: '/login',
            name: 'login',
            component: Login
        },
        {
            path: '/logout',
            name: 'logout',
            component: Logout
        }
    ]
})
var NotFound = {template: '<p>Page not found</p>'};
var Home = {template: '<p>home page</p>'};
var About = {template: '<p>about page</p>'};

var routes = {
    '': Home,
    '#about': About
};

var app = new Vue({
    el: '#app',
    data: {
        currentRoute: window.location.hash
    },
    computed: {
        ViewComponent: function () {
            return routes[this.currentRoute] || NotFound
        }
    },
    render: function (h) {
        return h(this.ViewComponent)
    }
});

window.addEventListener('popstate',function () {
    app.currentRoute = window.location.hash
});

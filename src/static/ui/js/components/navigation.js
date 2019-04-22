Vue.component('navigation', {
    props: ['tabs'],
    template: `
        <div class="nav flex-column nav-pills" role="tablist" aria-orientation="vertical">
            <a class="nav-link bg-dark text-white mt-1" href="{% url 'users:index' %}" role="tab">{% trans 'Home' %}</a>
        </div>
    `
});
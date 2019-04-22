import axios from 'axios';

export default class Paginator {

    constructor(url) {
        this.url = url;
        this.records = [];
        this.count = null;
        this.next = null;
        this.prev = null;
        this.paginated = false;
    }

    fetch(url) {
        axios.get(url || this.url)
            .then(response => {
                this.records = response.data.results;
                this.count = response.data.count;
                this.next = response.data.next;
                this.prev = response.data.previous;
                if (this.count > this.records.length) {
                    this.paginated = true
                }
            })
            .catch(error => {
                console.log(error)
            });
    }
}

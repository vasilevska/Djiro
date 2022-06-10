<template>
    <div class="card">
        <div class="card-body">
            <div class="d-flex flex-column align-items-center text-center">
            <img
                alt="Profile picture"
                class="rounded-circle"
                width="150"
                v-bind:src="thumbnail"
                @click="showProfile"
            />
            <div class="mt-3 text-center">
                <h4>{{ user.first_name + " " + user.last_name }}</h4>
                <p
                class="text-secondary mb-1"
                v-if="user['is_djiler']"
                >
                Điler
                </p>
                <p v-if="rating != null">
                {{ rating }} <font-awesome-icon icon="star" />
                </p>
                <p v-if="rating == null">Ovaj korisnik nema ocene</p>
            </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
img:hover {
    cursor: pointer;
}
</style>
<script>
import axios from 'axios';

export default {
    name: "UserCard",
    props: ['user'],
    data() {
        return {
            rating: null,
            id: -1,
            thumbnail: null,
        }
    },
    created() {
        if ('pk' in this.user) {
            this.id = this.user['pk'];
        }
        else {
            this.id = this.user['id'];
        }

        // Thumbnail needs to be fethced on its own
        axios({
            method: "get",
            url: `http://127.0.0.1:8000/api/get-user/?id=${this.id}`,
            })
            .then((response) => {
                // Get the first and only user from the response
                this.thumbnail = response.data.results[0].get_thumbnail;
            })
            .catch((err) => {
                console.log(err);
        });

        if (this.user["is_djiler"]) {
            axios({
                method: "get",
                url: `http://127.0.0.1:8000/api/rating/djiler/${this.id}`,
            })
                .then((response) => {
                // Get the first and only user from the response
                this.rating = response.data;
                })
                .catch((err) => {
                console.log(err);
                });
            } else {
                axios({
                    method: "get",
                    url: `http://127.0.0.1:8000/api/rating/driver/${this.id}`,
                })
                    .then((response) => {
                        // Get the first and only user from the response
                        this.rating = response.data;    
                    })
                        .catch((err) => {
                        console.log(err);
                    });
            }
    },
    methods: {
        showProfile() {
            this.$router.push({ path:`/profile/${this.id}`});
        }
    }
}
</script>
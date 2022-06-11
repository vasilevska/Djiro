<template>
<div class="card-body p-4">
    <div class="d-flex flex-start">
        <img class="rounded-circle shadow-1-strong me-3" :src="get_thumbnail" @click="toProfile" alt="avatar" width="60" height="60" />
        <div>
        <h6 class="fw-bold mb-1">{{ first_name + " " + last_name }}</h6>
        <div class="d-flex align-items-center mb-3">
            <p v-if="rating != null">
                {{ rating.car_rating }} <font-awesome-icon icon="star" />
            </p>
        </div>
        <p class="mb-0">
            {{ rating.descr }}
        </p>
        </div>
    </div>
</div>
</template>
<style scoped>
.rounded-circle {
    cursor: pointer;
}
</style>
<script>
import axios from 'axios';

export default {
    name: "ReviewComponent",
    props: ['rating'],
    data() {
        return {
            first_name:'',
            last_name:'',
            get_thumbnail: '',
            id: null,
        }
    },
    created() {
        console.log(this.rating);
        axios({
          method: "get",
          url: `http://127.0.0.1:8000/api/get-user/?id=${this.rating['idu']}`,
          headers: { "Content-Type": "application/json", "Authorization" : `Bearer ${this.$store.state.accessToken}` },
        })
          .then((response) => {
            console.log(response.data);
            this.id = response.data.results[0].pk;
            this.first_name= response.data.results[0].first_name;
            this.last_name = response.data.results[0].last_name;
            this.get_thumbnail = response.data.results[0].get_thumbnail;
            console.log(this.user);
          })
          .catch((err) => {
            console.log(err);
          });
    },
    methods: {
        toProfile() {
            this.$router.push({ path: `/profile/${this.id}`});
        }
    }
}
</script>
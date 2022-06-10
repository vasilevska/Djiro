<template>
<div class="card-body p-4">
    <div class="d-flex flex-start">
        <img class="rounded-circle shadow-1-strong me-3" :src="user.get_thumbnail" alt="avatar" width="60" height="60" />
        <div>
        <h6 class="fw-bold mb-1">{{user.first_name + " " + user.last_name }}</h6>
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
<script>
export default {
    name: "ReviewComponent",
    props: ['rating'],
    data() {
        return {
            user: null,
        }
    },
    created() {
        axios({
          method: "post",
          url: `http://127.0.0.1:8000/api/get-user/?id=${this.rating.idu}`,
          data: json,
          headers: { "Content-Type": "application/json" },
        })
          .then((response) => {
            console.log(response.data);
            this.user = response.data; 
            resolve();
          })
          .catch((err) => {
            console.log(err);
            resolve();
          });
    }
}
</script>
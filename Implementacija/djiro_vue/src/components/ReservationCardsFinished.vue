<template>
  <div class="row">
    <div class="col">
      <div
        class="col"
        v-for="reservation in reservations"
        :key="reservation.idr"
      >
        <div class="card" v-if="reservation['status'] == 'F'">
          <h2>{{ reservation.idr }}</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      reservations: [],
    };
  },
  created() {
    console.log(this.$store.state.id);
    if (this.$store.state.user["is_djiler"]) {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/reservations/djiler/${this.$store.state.id}`,
        headers: { "Authorization" : `Bearer ${this.$store.state.accessToken}` },
      })
        .then((response) => {
          this.reservations = response.data;
          console.log(response.data);
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/reservations/driver/${this.$store.state.id}`,
        headers: { "Authorization" : `Bearer ${this.$store.state.accessToken}` },
      })
        .then((response) => {
          this.reservations = response.data;
          console.log(response.data);
          console.log("nije djiler");
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
  components: {},
};
</script>

<template>
  <div class="row">
    <div class="col">
      <div
        class="col"
        v-for="reservation in reservations"
        :key="reservation.idr"
      >
        <div class="card" v-if="reservation['status'] == 'R'">
          <h2>{{ reservation.idr }}</h2>
          <button
            v-if="this.$store.state.user['is_djiler']"
            @click="requestRes(reservation.idr, true)"
          >
            Prihvati
          </button>
          <button
            v-if="this.$store.state.user['is_djiler']"
            @click="requestRes(reservation.idr, false)"
          >
            Odbij
          </button>
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
    console.log("id:");
    console.log(this.$store.state.id);
    console.log("user: ");
    console.log(this.$store.state.user);
    if (this.$store.state.user["is_djiler"]) {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/reservations/djiler/${this.$store.state.id}`,
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
      })
        .then((response) => {
          this.reservations = response.data;
          console.log(response.data);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
  methods: {
    requestRes(reservation, accepted) {
      axios({
        method: "post",
        url: `http://127.0.0.1:8000/api/reservations/djiler/${reservation}`,
        data: {
          accept: accepted,
        },
      })
        .then((response) => {
          this.reservations = response.data;
          console.log(response.data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

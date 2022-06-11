<template>
  <div class="row">
    <div class="col">
      <div
        class="col"
        v-for="reservation in reservations"
        :key="reservation.idr"
      >
        <div class="card-body p-4" v-if="reservation['status'] == 'P'">
          <div class="d-flex flex-start">
            <img
              class="rounded-circle shadow-1-strong me-3"
              :src="reservation.idc.get_thumbnail"
              @click="reservation.idc.get_absolute_url"
              width="80"
              height="80"
            />
            <div>
              <h6 class="fw-bold mb-1">{{ reservation.idc.model.slug }}</h6>
              <div class="d-flex align-items-center mb-3">
                {{
                  "od: " +
                  reservation["date_from"] +
                  " do: " +
                  reservation["date_to"]
                }}
              </div>
              <button  class="btn btn-dark px-3 m-2" @click="cancelRes(reservation)">Otkazi</button>
              
            </div>
          </div>
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
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
  methods: {
    cancelRes(reservation) {
      axios({
        method: "put",
        url: `http://127.0.0.1:8000/api/reservations/driver/${reservation.idr}`,
        headers: { "Authorization" : `Bearer ${this.$store.state.accessToken}` },
      })
        .then((response) => {
          this.reservations = response.data;
          console.log(response.data);
          window.location.reload();
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

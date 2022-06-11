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
          <button
            v-if="this.$store.state.user['is_djiler']"
            @click="showDriverModal = true; res = reservation;"
          >
            Oceni
          </button>
          <button
            v-if="!this.$store.state.user['is_djiler']"
            @click="showCarModal = true; res = reservation;"
          >
            Oceni
          </button>
        </div>
      </div>
    </div>
  </div>
  <Teleport to="body">
    <!-- use the modal component, pass in the prop -->
    <CarRatingModal
      :show="showCarModal"
      :reservation="res"
      @close="car_ocena_popup()"
    ></CarRatingModal>
  </Teleport>
  <Teleport to="body">
    <!-- use the modal component, pass in the prop -->
    <DriverRatingModal
      :show="showDriverModal"
      :reservation="res"
      @close="driver_ocena_popup()"
    ></DriverRatingModal>
  </Teleport>
</template>

<script>
import axios from "axios";
import CarRatingModal from "./CarRatingModal.vue";
import DriverRatingModal from "./DriverRatingModal.vue";

export default {
  components: {
    CarRatingModal,
    DriverRatingModal,
  },
  data() {
    return {
      reservations: [],
      showCarModal: false,
      showDriverModal: false,
      res: null,
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
  methods: {
    driver_ocena_popup() {
      this.showDriverModal = false;
    },
    car_ocena_popup() {
      this.showCarModal = false;
    },
  },
};
</script>

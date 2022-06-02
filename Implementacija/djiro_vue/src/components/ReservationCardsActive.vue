<template>
  <div class="row">
    <div class="col">
      <div
        class="col"
        v-for="reservation in reservations"
        :key="reservation.idr"
      >
        <ReservationCard
          v-if="reservation.status == 'P'"
          :resInfo="reservation"
        ></ReservationCard>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import ReservationCard from "./ReservationCard.vue";
export default {
  data() {
    return {
      reservations: [],
    };
  },
  created() {
    console.log(this.$store.state.id);
    axios({
      method: "get",
      //url: `http://127.0.0.1:8000/api/reservations/driver/${this.$store.state.id}`,
      url: `http://127.0.0.1:8000/api/reservations/driver/3`,
    })
      .then((response) => {
        this.reservations = response.data.results;
      })
      .catch((err) => {
        console.log(err);
      });
  },
  components: { ReservationCard },
};
</script>

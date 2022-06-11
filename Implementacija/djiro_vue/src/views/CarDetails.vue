<template>
  <div class="container">
    <div class="row">
      <div class="col-12" style="text-align: center">
        <figure class="image mb-6">
          <img v-bind:src="car.get_image" style="width: 70%; height: 70%" />
        </figure>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6 card" style="text-align: center">
        <h3>{{ car.year }}</h3>
        <hr />
        <div style="text-align: left">
          <h1>Opis:</h1>
          <h4>{{ car.descr }}</h4>
        </div>
      </div>
      <div class="col-sm-6">
        <UserCard :user="car['user']"/>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6 offset-sm-6">
        <div class="col-sm-12 card">
          <h2>Cena: {{ car.price_per_day }}€/dan</h2>
          <hr v-if="this.$store.state.id!=car.user.id && doc_verified==true" />
          <h3 v-if="this.$store.state.id!=car.user.id && doc_verified==true">Izaberite datume:</h3>
          <form v-if="this.$store.state.id!=car.user.id && doc_verified==true" style="margin: 10px" id="resform">
            Od: <input type="date" name="date_from" id="datumOd" /> Do:
            <input type="date" name="date_to" id="datumDo" />
            <input
              type="text"
              name="status"
              id="datumDo"
              value="R"
              class="d-none"
            />
            <input
              type="number"
              name="car"
              id="datumDo"
              :value="car.idc"
              class="d-none"
            />
            <input
              type="number"
              name="djiler"
              id="datumDo"
              :value="idd"
              class="d-none"
            />
            <input
              type="number"
              name="driver"
              id="datumDo"
              class="d-none"
              :value="this.$store.state.id"
            />
          </form>
          <div v-if="this.$store.state.id!=car.user.id && doc_verified==true"
           class="col-sm-3" style="margin-top: 40px">
            <button
              class="btn btn-primary"
              style="width: 150px"
              @click="makeReservation"
            >
              REZERVISI
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-for="rat in ratings" :key="rat.ido" class="row">
      <ReviewComponent :rating="rat"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserCard from "@/components/UserCard.vue";
import ReviewComponent from "@/components/ReviewComponent.vue";

export default {
  name: "CarDetails",
  components: { UserCard, ReviewComponent },
  data() {
    return {
      car: [],
      idd: null,
      ratings: null,
      doc_verified: false,
    };
  },
  created() {
    if (this.$store.state.user != null && this.$store.state.user != 'null') {
      this.doc_verified = this.$store.state.user.doc_verified;
    }
    this.getCar();
    this.getRatings();
  },
  methods: {
    getRatings() {
      axios
        .get(`ratings/car/${this.car.idc}`)
        .then((response) => {
          this.ratings = response.data;
          console.log(this.ratings);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getCar() {
      const idc = this.$route.params.car_slug;
      axios
        .get(`/api/car/${idc}`)
        .then((response) => {
          this.car = response.data;
          this.idd = this.car.user.id;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    makeReservation() {
      console.log("ovde");
      var formElement = document.querySelector("form");
      var formData = new FormData(formElement);
      var object = {};
      formData.forEach((value, key) => (object[key] = value));
      var json = JSON.stringify(object);
      console.log(object);
      new Promise((resolve) => {
        axios({
          method: "post",
          url: `http://127.0.0.1:8000/api/reservations/driver/${this.$store.state.id}`,
          data: json,
          headers: { "Content-Type": "application/json", "Authorization" : `Bearer ${this.$store.state.accessToken}`},
        })
          .then((response) => {
            console.log(response.data);
            alert("Kola su uspešno rezervisana.");
            resolve();
          })
          .catch((err) => {
            console.log(err);
            resolve();
          });
      });
    },
  },
};
</script>

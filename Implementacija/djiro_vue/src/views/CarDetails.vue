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
      <div class="col-6" style="text-align: center">
        <h3>{{ car.year }}</h3>
        <hr />
        <div style="text-align: left">
          <h1>Opis:</h1>
          <h4>{{ car.descr }}</h4>
        </div>
      </div>
      <div class="col-6">
        <h2>Cena: {{ car.price_per_day }}€/dan</h2>
        <hr />
        <h3>Izaberite datume:</h3>
        <form style="margin: 10px" id="resform">
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
        <div class="col-3" style="margin-top: 40px">
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
</template>

<script>
import axios from "axios";

export default {
  name: "CarDetails",
  data() {
    return {
      car: [],
      idd: null,
    };
  },
  mounted() {
    this.getCar();
  },
  methods: {
    getCar() {
      const car_slug = this.$route.params.car_slug;
      axios
        .get(`/api/car/${car_slug}`)
        .then((response) => {
          this.car = response.data;
          this.idd = this.car.idu.id;
          console.log(this.car.idu.id);
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
      new Promise((resolve) => {
        axios({
          method: "post",
          url: "http://127.0.0.1:8000/api/reservations/driver/0",
          data: json,
          headers: { "Content-Type": "application/json" },
        })
          .then((response) => {
            console.log(response.data);
            alert("uspesno rezervisano");
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

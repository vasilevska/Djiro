<template>
  <div class="container">
    <div class="row">
      <div class="col-12" style="text-align: center">
        <figure class="image mb-6">
          <img v-bind:src="car.get_image" style="width: 70%; height: 70%" />
        </figure>
      </div>
    </div>
    <div v-if="!sending">
      <div class="row justify-content-center">
        <div class="col-auto">
          <h2>Izmenite polja koja zelite</h2>
        </div>
        <div
          v-if="errors"
          id="error-div"
          class="alert alert-danger"
          role="alert"
        >
          Ispravite sledece greske:
          <ul>
            <li v-for="error in errors" v-bind:key="error">{{ error }}</li>
          </ul>
        </div>
        <div v-if="infos" id="info-div" class="info alert-info" role="alert">
          Poruke:
          <ul>
            <li v-for="info in infos" v-bind:key="info">{{ info }}</li>
          </ul>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-12">
          <div class="form-group my-3">
            <label for="adresaVozila">Gde se Vaše vozilo nalazi?</label>
            <input
              type="text"
              class="form-control"
              name="address"
              id="adresaVozila"
              placeholder="Unesite adresu"
              required
            />
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-6 col-sm-12">
          <div class="form-group my-3 mx-3">
            <div class="input-group">
              <label for="customRange2">Cena po danu (u &euro;): </label>
              <input
                type="number"
                min="10"
                max="205"
                class="form-control mx-3"
                size="3"
                id="rangeVal"
              />
            </div>
            <input
              type="range"
              class="form-range mt-2"
              min="10"
              max="205"
              id="customRange2"
              required
            />
          </div>
        </div>
        <div class="col-lg-6 col-sm-12">
          <div class="form-group my-3 mx-3">
            <label for="km">Kilometraža: </label
            ><input
              type="number"
              min="0"
              max="1000000"
              step="1"
              class="form-control"
              name="km"
              id="km"
              required
            />
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-12">
          <div class="form-group">
            <label for="opis-kola">Opis vozila</label>
            <textarea
              name="descr"
              class="form-control"
              id="opis-kola"
              rows="5"
              required
            ></textarea>
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-auto">
          <br />
          <button class="btn btn-dark" @click="update">Azuriraj</button>
          <br /><br />
        </div>
      </div>
    </div>
    <div v-else>
      <class class="row justify-content-center align-items-center">
        <div class="col-auto">
          <ring-loader :color="color1" :height="height"></ring-loader>
        </div>
      </class>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import $ from "jquery";
import RingLoader from "vue-spinner/src/RingLoader.vue";
export default {
  name: "UpdateCarDetails",
  data() {
    return {
      car: [],
      idd: null,
      infos: null,
      errors: null,
      sending: false,
      color1: "#3AB982",
      height: "50px",
    };
  },
  mounted() {
    this.getCar();

    $("#customRange2").on("input", function () {
      let val = $("#customRange2").val();
      $("#rangeVal").val(val);
    });
    $("#rangeVal").on("input", function () {
      let val = $("#rangeVal").val();
      $("#customRange2").val(val);
    });
  },
  updated() {
    $("#opis-kola").val(this.car.descr);
    $("#km").val(parseInt(this.car.km));
    $("#rangeVal").val(this.car.price_per_day);
    $("#customRange2").val(this.car.price_per_day);
  },
  methods: {
    getCar() {
      const car_slug = this.$route.params.car_slug;
      axios
        .get(`/api/car/${car_slug}`)
        .then((response) => {
          this.car = response.data;
          this.idd = this.car.idu.id;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    sendForm(formData) {
      const car_slug = this.$route.params.car_slug;
      axios({
        method: "post",
        url: "http://127.0.0.1:8000/api/update_car/" + car_slug + "/",
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${this.$store.state.accessToken}`,
        },
      })
        .then((response) => {
          this.dispalyInfo(response.data);
          this.sending = false;
          this.$router.push({
            name: "carDetails",
            params: { car_slug: car_slug },
          });
        })
        .catch((err) => {
          this.displayError(err.response.data);
          this.displayError(err.message);
          this.sending = false;
        });
    },
    dispalyInfo(info) {
      this.infos = [];
      for (let key in info) {
        this.infos.push(key + " : " + info[key]);
      }
    },
    resetInfo() {
      this.infos = null;
    },
    resetErrors() {
      this.errors = null;
    },
    displayError(err) {
      this.errors = [];
      for (let key in err) {
        this.errors.push(key + " : " + err[key]);
        console.log(err[key]);
      }
    },
    getForm() {
      var formData = new FormData();
      formData.append("descr", document.querySelector("#opis-kola").value);
      formData.append("km", parseInt(document.getElementById("km").value));
      formData.append(
        "price_per_day",
        document.querySelector("#rangeVal").value
      );
      return formData;
    },
    update() {
      this.resetInfo();
      this.resetErrors();
      this.sending = true;
      let self = this;
      var formData = self.getForm();
      var addressValue = document.querySelector("#adresaVozila").value;
      if (addressValue == "") {
        self.sendForm(formData);
      } else {
        axios({
          method: "get",
          url: `https://dev.virtualearth.net/REST/v1/Locations/${addressValue}?key=Al9hlQRWKffWXgWCo9DIxIenHGNvv7gkLztrBjFCJdInqHrVa2HXFyIdVoI8-DQ9`,
        })
          .then((response) => {
            var points =
              response.data.resourceSets[0].resources[0].point.coordinates;
            var dict = { lat: points[0], long: points[1] };
            console.log(dict);
            formData.append("coordinates", JSON.stringify(dict));
            self.sendForm(formData);
          })
          .catch((err) => {
            console.log(err);
            this.displayError(err);
            self.sending = false;
          });
      }
    },
  },
  components: {
    RingLoader,
  },
};
</script>

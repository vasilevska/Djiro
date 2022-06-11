<template>
  <div id="results" class="container pt-1 mt-2">
    <div class="row mt-2 pl-2">
      <div class="d-flex filteri mt-1">
        <h3>Sortiranje:&nbsp;&nbsp;</h3>
        <select
          name="sort"
          id="sortiranje"
          style="width: 350px"
          v-on:change="sortF($event)"
        >
          <option value="bez-sort" selected>Izaberite sortiranje</option>
          <option value="god_desc">
            Godiste vozila (Od najvece do najmanje)
          </option>
          <option value="god_asc">
            Godiste vozila (Od najmanje do najvece)
          </option>
          <option value="km_desc">
            Kilometraza vozila (Od najvece do najmanje)
          </option>
          <option value="km_asc">
            Kilometraza vozila (Od najmanje do najvece)
          </option>
        </select>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <h3>Filteri:&nbsp;&nbsp;</h3>
        <button
          class="btn btn-dark form-control pl-5"
          style="width: 200px"
          @click="filters()"
        >
          Filteri
        </button>
      </div>
    </div>
    <div class="d-flex filteri mt-1 d-none py-3" id="filteri">
      <hr />
      <input
        class="form-control me-2"
        type="text"
        placeholder="Godiste"
        style="width: 200px"
        id="godiste"
      />
      <select name="markaS" id="markaS" style="width: 200px" class="mx-2">
        <option value="" selected>Izaberi Marku</option>
        <option value="Peugeot">Peugeot</option>
        <option value="Volvo">Volvo</option>
        <option value="Toyota">Toyota</option>
        <option value="Suzuki">Suzuki</option>
        <option value="Ford">Ford</option>
        <option value="Jaguar">Jaguar</option>
        <option value="Alpha Romeo">Alpha Romeo</option>
        <option value="MINI">MINI</option>
        <option value="Nissan">Nissan</option>
        <option value="Porsche">Porsche</option>
        <option value="Volkswagen">Volkswagen</option>
        <option value="Škoda">Škoda</option>
      </select>
      <select name="tipS" id="tipS" style="width: 230px" class="mx-2">
        <option value="" selected>Izaberi tip Vozila</option>
        <option value="sedan">Sedan</option>
        <option value="kupe">Kupe</option>
        <option value="kabriolet">Kabriolet</option>
        <option value="karavan">Karavan</option>
        <option value="suv">SUV</option>
        <option value="kombi">Kombi</option>
        <option value="limuzina">Limuzina</option>
      </select>
      <select name="gorivoS" id="gorivoS" style="width: 200px" class="mx-2">
        <option value="" selected>Izaberi vrstu Gorivo</option>
        <option value="dizel">Dizel</option>
        <option value="benzin">Benzin</option>
        <option value="plin">Plin</option>
        <option value="hibrid">Hibrid</option>
        <option value="elektricni">Električni</option>
      </select>
      <button class="btn btn-dark mx-2" style="width: 150px" @click="f2()">
        Filtriraj
      </button>
    </div>
    <hr />
    <div v-if="!loading" class="columns is-multiline">
      <div class="column is-8">
        <h2 class="is-size-2 has-text-centered">Cars</h2>
      </div>

      <div class="coulmn is-4" v-for="car in cars" v-bind:key="car.idc">
        <div class="box" style="padding: 10px">
          <div class="container">
            <div class="row">
              <div class="col-4">
                <img v-bind:src="car.get_thumbnail" />
              </div>
              <div class="col-4">
                <h3 class="id-size-4">
                  <i>{{ car.model.manufacturer.name }} {{ car.model.name }}</i>
                </h3>
                <h4 class="id-size-4">Tip: {{ car.type }}</h4>
                <h4 class="id-size-4">Gorivo: {{ car.fuel }}</h4>
                <!-- Fali ocena -->

                <hr />
                <div class="row align-bottom">
                  <div class="col-3">
                    <router-link
                      class="btn btn-dark"
                      :to="car.get_absolute_url"
                      style="width: 150px"
                      >Vise detalja</router-link
                    >
                  </div>
                  <div class="col-3 align-right">
                    <h3 class="id-size-4">
                      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{
                        car.price_per_day
                      }}€/dan
                    </h3>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="mapa">
        <MapComponent
          :zoom="zoom"
          :cars="cars"
          :center="coordinates_center"
        ></MapComponent>
      </div>
    </div>
    <div v-else class="row justify-content-center">
      <div class="col-auto">
        <ring-loader :color="color1" :height="height"></ring-loader>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mapa {
  position: fixed;
  bottom: 10vh;
  right: 20px;
  width: 30vw;
  height: 30vw;
}
</style>

<script>
import RingLoader from "vue-spinner/src/RingLoader.vue";
import axios from "axios";
import MapComponent from "../components/Map/Map.vue";

export default {
  name: "ListingView",
  data() {
    return {
      cars: [],
      cars_unselected_filters: [],
      coordinates_center: null,
      loading: false,
      color1: "#3AB982",
      height: "50px",
      zoom: 12,
      ratings: [],
      tmp1: [],
    };
  },
  components: {
    RingLoader,
    MapComponent,
  },
  created() {
    this.loading = true;
    this.getCarList();
  },
  methods: {
    getRatings() {
      for (var i = 0; i < this.cars.length; i++) {
        var id = this.cars[i].idc;
        var ind = 0;
        axios
          .get(`/api/rating/car/${id}`)
          .then((response) => {
            this.tmp1 = response.data;
            console.log(this.tmp1);
            this.ratings.push({
              id: this.cars[ind++].idc,
              rating: this.tmp1.rating,
              count: this.tmp1.count,
            });
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    getCarList() {
      let self = this;
      var search_term = localStorage.getItem("_s_term");
      if (search_term == null || search_term == "") {
        this.zoom = 7;
        axios
          .get("/api/list_of_all_cars/")
          .then((response) => {
            this.cars = response.data;
            console.log(this.cars);
            self.getRatings();
            var dict = { lat: 44.0165, long: 21.0059 };
            self.coordinates_center = dict;
          })
          .catch((error) => {
            console.log(error);
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        axios({
          method: "get",
          url: `https://dev.virtualearth.net/REST/v1/Locations/${search_term}?key=Al9hlQRWKffWXgWCo9DIxIenHGNvv7gkLztrBjFCJdInqHrVa2HXFyIdVoI8-DQ9`,
        })
          .then((response) => {
            var points =
              response.data.resourceSets[0].resources[0].point.coordinates;
            var dict = { lat: points[0], long: points[1] };
            self.coordinates_center = dict;
            var coords = JSON.stringify(dict);
            axios({
              method: "get",
              url: "http://127.0.0.1:8000/api/get_car_by_location",
              params: {
                coordinates: coords,
                lat_factor: 0.4,
                long_factor: 0.4,
              },
            })
              .then((response) => {
                this.cars = response.data;
                console.log(this.cars);
                self.getRatings();
                this.loading = false;
              })
              .catch((err) => {
                console.log(err);
                this.loading = false;
              });
          })
          .catch((err) => {
            console.log(err);
            this.loading = false;
          });
      }
    },
    sortF: function (e) {
      console.log(e.target.value);
      console.log(this.ratings);
      var tmp = e.target.value;

      switch (tmp) {
        case "god_desc":
          console.log(this.cars);
          this.cars.sort(function (first, second) {
            return second.year - first.year;
          });
          console.log(this.cars);
          break;
        case "god_asc":
          this.cars.sort(function (first, second) {
            return -(second.year - first.year);
          });
          break;
        case "km_desc":
          this.cars.sort(function (first, second) {
            console.log(second.km);
            console.log(first.km);
            return second.km - first.km;
          });
          break;
        case "km_asc":
          this.cars.sort(function (first, second) {
            return -(second.km - first.km);
          });
          break;
        default:
          break;
      }
    },
    filters() {
      document.getElementById("filteri").classList.remove("d-none");
    },
    f2() {
      var e = document.getElementById("markaS");
      var marka = e.options[e.selectedIndex].value.toLowerCase();
      e = document.getElementById("tipS");
      var tip = e.options[e.selectedIndex].value.toLowerCase();
      e = document.getElementById("gorivoS");
      var gorivo = e.options[e.selectedIndex].value.toLowerCase();
      var godiste = document.getElementById("godiste").value;

      console.log(marka, tip, gorivo, godiste);

      var len = this.cars.length;

      var index_out = [];

      for (var i = 0; i < len; i++) {
        if (
          marka != "" &&
          this.cars[i].model.manufacturer.name.toLowerCase() != marka
        ) {
          this.cars_unselected_filters.push(this.cars[i]);
          //this.cars.splice(i, 1);
          index_out.push(i);
          continue;
        } else if (tip != "" && this.cars[i].type.toLowerCase() != tip) {
          this.cars_unselected_filters.push(this.cars[i]);
          //this.cars.splice(i, 1);
          index_out.push(i);
          continue;
        } else if (gorivo != "" && this.cars[i].fuel.toLowerCase() != gorivo) {
          this.cars_unselected_filters.push(this.cars[i]);
          //this.cars.splice(i, 1);
          index_out.push(i);
          continue;
        } else if (godiste != "" && parseInt(this.cars[i].year) != godiste) {
          this.cars_unselected_filters.push(this.cars[i]);
          //this.cars.splice(i, 1);
          index_out.push(i);
          continue;
        }
      }

      //izbacivanje iz liste auta
      for (i = index_out.length - 1; i >= 0; i--) {
        this.cars.splice(index_out[i], 1);
      }

      len = this.cars_unselected_filters.length;

      //predstavlja koliko moramo filteri proci da bi se vratio u listing
      var indikator = 0;
      if (marka != "") {
        indikator += 1;
      }
      if (gorivo != "") {
        indikator += 1;
      }
      if (godiste != "") {
        indikator += 1;
      }
      if (tip != "") {
        indikator += 1;
      }
      index_out = [];

      //ako su promenjena polja za filtriranje, pa mozda
      for (i = 0; i < len; i++) {
        var tmp = 0;
        if (
          marka != "" &&
          this.cars_unselected_filters[
            i
          ].model.manufacturer.name.toLowerCase() == marka
        ) {
          tmp += 1;
        }
        if (
          tip != "" &&
          this.cars_unselected_filters[i].type.toLowerCase() == tip
        ) {
          tmp += 1;
        }
        if (
          gorivo != "" &&
          this.cars_unselected_filters[i].fuel.toLowerCase() == gorivo
        ) {
          tmp += 1;
        }
        if (
          godiste != "" &&
          parseInt(this.cars_unselected_filters[i].year) == godiste
        ) {
          tmp += 1;
        }
        if (tmp == indikator) {
          this.cars.push(this.cars_unselected_filters[i]);
          index_out.push(i);
        }
      }

      //izbacivanje iz liste auta
      for (i = index_out.length - 1; i >= 0; i--) {
        this.cars_unselected_filters.splice(index_out[i], 1);
      }

      document.getElementById("filteri").classList.add("d-none");
    },
  },
};
</script>

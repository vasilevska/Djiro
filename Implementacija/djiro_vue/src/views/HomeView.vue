<template>
  <div class="fill-height home">
    <div
      class="row justify-content-center fixed-top pb-5 bg-black m-5"
      id="search_row"
      style="--bs-bg-opacity: 0.4; position: fixed; top: 5vh"
    >
      <div
        class="col-6 my-2 text-center py-2 mt-2 opacity-70"
        style="max-height: 90vh"
      >
        <h1
          class="text-white display-4 font-weight-bold mb-4"
          style="font-size: 11em; font-weight: 900"
        >
          Điro
        </h1>
        <h1
          class="text-white display-4 font-weight-bold mb-4"
          style="font-size: 3em"
        >
          Aplikacija za lako iznajmljivanje automobila
        </h1>
        <div class="d-flex">
          <input
            class="form-control me-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
            id="searchbar"
          />
          <input
            type="text"
            class="me-2"
            name="daterange"
            id="demo"
            value="01/01/2022 - 01/15/2022"
          />
          <button class="btn btn-light btn-outline-secondary" id="search">
            Search
          </button>
          <button
            class="btn btn-light btn-outline-secondary mx-2"
            id="filter"
            style="display: none"
          >
            Filter
          </button>
        </div>
        <div class="d-flex filteri mt-1 d-none">
          <input
            class="form-control me-2"
            type="text"
            placeholder="Godiste"
            id="godiste"
          />
          <input
            class="form-control me-2"
            type="text"
            placeholder="Marka"
            id="marka"
          />
          <input
            class="form-control me-2"
            type="text"
            placeholder="Model"
            id="model"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  background-image: url("@/assets/naslovna1a.jpeg");
  min-height: 91.5vh;
  background-size: cover !important;
  top: 10vh;
}
</style>

<script>
// import CarCard from '../components/CarCard.vue';
import { getAPI } from "@/axios-api";
import { mapState } from "vuex";

export default {
  name: "HomeView",
  components: {},
  computed: mapState(["APIData"]),
  mounted() {
    // TODO: Change this with car api and car cards, this only served for testing
    getAPI
      .get("/api/sample", {
        headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
      })
      .then((response) => {
        this.$store.state.APIData = response.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

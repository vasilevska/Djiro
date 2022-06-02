<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-sm-6">
        <p class="h1 my-5">Unesite informacije o Vašoj vozačkoj</p>
        <p class="error">
          {{ error }}
        </p>
        <p class="info">
          {{ info }}
        </p>
        <form enctype=”multipart/form-data” >
        <div class="form-group my-3 mx-3">
          <label for="datum-izdavanja">Datum izdavanja:</label>
          <input
            type="date"
            class="form-control"
            id="datum-izdavanja"
            name="issuing_date"
            placeholder="Datum izdavanja"
            required
            v-model="issuing_date"
          />
        </div>
        <div class="form-group my-3 mx-3">
          <label for="datum-isteka">Datum isteka:</label>
          <input
            type="date"
            class="form-control"
            id="datum-isteka"
            name="valid_date"
            placeholder="Datum isteka"
            required
            v-model="valid_date"
          />
        </div>
        <div class="form-group my-3 mx-3">
          <label for="broj-dokumenta">Broj dokumenta:</label>
          <input
            type="text"
            class="form-control"
            id="broj-dokumenta"
            name="reg_number"
            placeholder="Broj dokumenta"
            required
            v-model="reg_number"
          />
        </div>
        <div class="form-group my-3">
          <label for="vozacka-napred" class="mb-1"
            >Slike prednje strane vozačke:</label
          >
          <br />
          <input
            type="file"
            id="vozacka-napred"
            name="image1"
            accept="image/png, image/jpeg"
            multiple
            required
          />
        </div>
        <div class="form-group my-3">
          <label for="vozacka-pozadi" class="mb-1"
            >Slike zadnje strane vozačke:</label
          >
          <br />
          <input
            type="file"
            id="vozacka-pozadi"
            name="image2"
            accept="image/png, image/jpeg"
            multiple
            required
          />
        </div>
        <div class="form-group my-3">
          <input
            class="btn btn-dark"
            v-on:click.prevent="submit_formdata"
            type="submit"
            value="Pošalji"
          />
        </div>
        </form>
      </div>
    </div>
  </div>
</template>
<style scoped>
.container {
  justify-content: center;
}
</style>
<script>
import axios from "axios";

export default {
  name: "VerificationView",
  data() {
    return {
      info: "",
      error: "",
    };
  },
  methods: {
    submit_formdata() {
      var formElement = document.querySelector("form");
      var formData = new FormData(formElement);
      // Display the key/value pairs
      for (var pair of formData.entries()) {
        console.log(pair[0] + ", " + pair[1]);
      }
      new Promise((resolve, reject) => {
        axios({
          method: "post",
          url: "http://127.0.0.1:8000/api/verification/",
          data: formData,
          headers: { "Content-Type": "multipart/form-data" },
        })
          .then((response) => {
            this.info = response.data;
            resolve();
          })
          .catch((err) => {
            console.log(err);
            reject();
          });
      });
    },
  },
};
</script>

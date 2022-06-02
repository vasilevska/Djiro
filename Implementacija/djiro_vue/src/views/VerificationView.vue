<template>
  <div class="container">
    <div class="row justify-content-center">
      <div v-if="errors" id="error-div" class="alert alert-danger" role="alert">
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
      <div v-if="!sending" class="col-sm-6">
        <p class="h1 my-5">Unesite informacije o Vašoj vozačkoj</p>
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
      <div v-else class="col-sm-6">
          <ring-loader :color="color1" :height="height"></ring-loader>
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
import RingLoader from 'vue-spinner/src/RingLoader.vue'

export default {
  name: "VerificationView",
  data() {
    return {
      infos: null,
      errors: null,
      sending: false,
      color1: '#3AB982',
      height: '35px',
      width: '4px',
      margin: '2px',
      radius: '2px'
    };
  },
  methods: {
    submit_formdata() {
      this.errors = null;
      this.infos = null;
      let self = this;
      var formElement = document.querySelector("form");
      var formData = new FormData(formElement);
      this.sending = true;
      new Promise((resolve, reject) => {
        axios({
          method: "post",
          url: "http://127.0.0.1:8000/api/verification/",
          data: formData,
          headers: { 
            "Content-Type": "multipart/form-data" ,
            Authorization : `Bearer ${this.$store.state.accessToken}`
          },
        })
          .then((response) => {
            this.infos = []
            for (let key in response.data) {
              this.infos.push(key + " : " + response.data[key]);
            }
            resolve(response);
          })
          .catch((err) => {
            self.errors = [];
            self.errors.push("axios : " + err.message)
            for (let key in err.response.data) {
              self.errors.push(key + " : " + err.response.data[key]);
            }
            reject()
          });
      }).then(()=>{
        
        this.$router.push({name : "home"});
      }
      ).catch(()=>{
      }
      ).finally(()=>{
        self.sending = false;
      });
    },
  },
  components:{
    RingLoader
  }
};
</script>

<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-sm-6">
        <p class="h1 my-5">Unesite lične informacije</p>
        <div class="alert alert-danger" role="alert">
          Please correct the following errors:
        </div>
        <form enctype=”multipart/form-data”>
        <div class="input-group">
          <div class="form-group my-3 mr-3">
            <label for="ime">Ime</label>
            <input
              type="text"
              class="form-control"
              id="ime"
              name="first_name"
              placeholder="Unesite ime"
              required
              v-model="firstname"
            />
          </div>
          <div class="form-group my-3 mx-3">
            <label for="prezime">Prezime</label>
            <input
              type="text"
              class="form-control"
              id="prezime"
              name="last_name"
              placeholder="Unesite prezime"
              required
              v-model="lastname"
            />
          </div>
        </div>

        <div class="input-group">
          <div class="form-group my-3 mr-3">
            <label for="email">E-mail</label>
            <input
              type="email"
              class="form-control"
              id="email"
              name="email"
              placeholder="Unesite e-mail"
              required
              v-model="email"
            />
          </div>
          <div class="form-group my-3 mx-3">
            <label for="telefon">Broj telefona</label>
            <input
              type="tel"
              class="form-control"
              id="telefon"
              name="tel"
              placeholder="Broj telefona"
              required
              v-model="tel"
            />
          </div>
        </div>
        <div class="input-group">
          <div class="form-group my-3 mr-3">
            <label for="email">Lozinka</label>
            <input
              type="password"
              class="form-control"
              id="password1"
              name="password1"
              placeholder="Unesite lozinku"
              required
              v-model="password1"
            />
          </div>
          <div class="form-group my-3 mx-3">
            <label for="telefon">Ponovite lozinku</label>
            <input
              type="password"
              class="form-control"
              id="password2"
              name="password2"
              placeholder="Ponovite lozinku"
              required
              v-model="password2"
            />
          </div>
        </div>
        <div class="form-group my-3">
          <label for="profilna" class="mb-1">Profilna slika</label> <br />
          <!-- style="display: none" -->
          <input
            type="file"
            id="profilna"
            name="avatar"
            accept="image/png, image/jpeg"
          />
        </div>
        <div class="form-group">
          <label for="bio">Bio</label>
          <textarea
            class="form-control"
            id="bio"
            name="bio"
            rows="5"
            v-model="bio"
          ></textarea>
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
import { getAPI } from "@/axios-api";
import axios from "axios";

export default {
  name: "RegistrationView",
  data() {
    return {
      firstname: "",
      lastname: "",
      email: "",
      password1: "",
      password2: "",
      tel: "",
      bio: "",
      selectedDoc: null,
      errors: [],
    };
  },
  methods: {
    onDocSelected(event) {
      this.selectedFile = event.target.files[0];
    },
    submit() {
      new Promise((resolve, reject) => {
        getAPI
          .post("/api/registration/", {
            email: this.email,
            password1: this.password1,
            password2: this.password2,
            first_name: this.firstname,
            last_name: this.lastname,
            tel: this.tel,
            bio: this.bio,
          })
          .then((response) => {
            console.log(response.data);
            this.$store
              .dispatch("userLogin", {
                email: this.email,
                password: this.password1,
              })
              .then(() => {
                this.$router.push({ name: "home" });
              })
              .catch((err) => {
                console.log(err);
              });
            resolve();
          })
          .catch((err) => {
            console.log(err);
            reject();
          });
      });
    },
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
          url: "http://127.0.0.1:8000/api/registration/",
          data: formData,
          headers: { "Content-Type": "multipart/form-data" },
        })
          .then((response) => {
            console.log(response.data);
            this.$store
              .dispatch("userLogin", {
                email: this.email,
                password: this.password1,
              })
              .then(() => {
                this.$router.push({ name: "home" });
              })
              .catch((err) => {
                console.log(err);
              });
            resolve();
          })
          .catch((err) => {
            console.log(err);
            reject();
          });
      });
    },
  },
  setup() {},
};
</script>

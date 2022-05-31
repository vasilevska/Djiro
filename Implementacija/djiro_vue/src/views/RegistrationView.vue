<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-sm-6">
        <p class="h1 my-5">Unesite lične informacije</p>
        <form>
          <div class="input-group">
            <div class="form-group my-3 mr-3">
              <label for="ime">Ime</label>
              <input
                type="text"
                class="form-control"
                id="ime"
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
                placeholder="Ponovite lozinku"
                required
                v-model="password2"
              />
            </div>
          </div>
          <div class="form-group my-3">
            <label for="profilna" class="mb-1">Profilna slika</label> <br />
            <input
              style="display: none"
              type="file"
              id="profilna"
              accept="image/png, image/jpeg"
              required
              @change="onAvatarSelected"
              ref="avatarInput"
            />
            <button
              type="button"
              class="btn btn-dark"
              @click="$refs.avatarInput.click()"
            >
              Izaberi profilnu sliku
            </button>
          </div>
          <div class="form-group my-3">
            <label for="vozacka" class="mb-1">Slike vozačke</label> <br />
            <input
              style="display: none"
              type="file"
              id="vozacka"
              accept="image/png, image/jpeg"
              multiple
              required
              @change="onDocSelected"
              ref="docInput"
            />
            <button
              type="button"
              class="btn btn-dark"
              @click="$refs.docInput.click()"
            >
              Izaberi sliku dokumenta
            </button>
          </div>
          <div class="form-group">
            <label for="bio">Bio</label>
            <textarea
              class="form-control"
              id="bio"
              rows="5"
              required
            ></textarea>
          </div>
          <div class="form-group my-3">
            <button class="btn btn-dark" @click="submit">Pošalji</button>
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
// import axios from "axios";

export default {
  name: "RegistrationView",
  data() {
    return {
      firstname: "",
      lastname: "",
      email: "",
      tel: "",
      password1: "",
      password2: "",
      selectedDoc: null,
    };
  },
  methods: {
    onDocSelected(event) {
      this.selectedFile = event.target.files[0];
    },
    submit() {},
  },
  setup() {},
};
</script>

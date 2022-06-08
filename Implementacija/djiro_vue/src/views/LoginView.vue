<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-sm-6">
        <h1>Uloguj se</h1>
        <form id="login-form" action="profil.html">
          <input
            type="text"
            name="username"
            class="username form-control my-3"
            placeholder="Email adresa"
            v-model="username"
          />
          <input
            type="password"
            name="password"
            class="password form-control"
            placeholder="Šifra"
            v-model="password"
          />
          <p class="error">
            {{ error }}
          </p>
          <p>
            Novi Korisnik?&nbsp;<router-link to="/registration"
              >Napravi Nalog</router-link
            >
          </p>
          <input
            class="btn btn btn-outline-secondary"
            type="button"
            value="Loguj se"
            @click="login"
          />
        </form>
      </div>
    </div>
  </div>
</template>
<style>
h1 {
  padding: 10px;
}
p {
  padding-left: 6px;
  padding-top: 2px;
}
.error {
  color: red;
}
</style>
<script>
export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      pasword: "",
      incorrectAuth: false,
      error: "",
    };
  },
  setup() {},
  methods: {
    login() {
      this.$store
        .dispatch("userLogin", {
          email: this.username,
          password: this.password,
        })
        .then(() => {
          this.$router.push({ name: "home" });
        })
        .catch((err) => {
          console.log(err);
          this.error = "Neispravna šifra ili mail";
          this.incorrectAuth = true;
        });
    },
  },
};
</script>

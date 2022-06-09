<template>
  <div class="container">
    <div class="main-body">
      <div id="error-div" class="alert alert-danger" role="alert">
        Please correct the following errors:
        <ul>
          <li v-for="error in errors" v-bind:key="error">{{ error }}</li>
        </ul>
      </div>
      <div class="row gutters-sm">
        <div class="col-md-4 mb-3">
          <div class="card">
            <div class="card-body">
              <div class="d-flex flex-column align-items-center text-center">
                <img
                  alt="Profile picture"
                  class="rounded-circle"
                  width="150"
                  v-bind:src="user.get_thumbnail"
                />
                <div class="mt-3">
                  <h4>{{ user.first_name + " " + user.last_name }}</h4>
                  <p class="text-secondary mb-1">Điler</p>
                  <form
                    id="profilna-forma"
                    enctype="multipart/form-data"
                    type="post"
                    :action="
                      'http://127.0.0.1:8000/api/update-avatar/' +
                      this.$route.params.id
                    "
                  >
                    <input
                      type="file"
                      id="profilna"
                      name="avatar"
                      accept="image/png, image/jpeg"
                      ref="avatarImage"
                      class="btn btn-dark"
                      @change="submitImage"
                    />
                    <!-- <button class="btn btn-dark" @click="document.getElementById('profilna-forma').submit()">Upload image</button> -->
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-8">
          <div class="card mb-3">
            <div class="card-body">
              <form id="user-info">
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">First Name</h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    <input
                      name="first_name"
                      type="text"
                      class="form-control"
                      :value="user.first_name"
                    />
                  </div>
                </div>
                <hr />
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">Last Name</h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    <input
                      name="last_name"
                      type="text"
                      class="form-control"
                      :value="user.last_name"
                    />
                  </div>
                </div>
                <hr />
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">Email</h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    <!-- <input type="text" class="form-control" :value="user.email"> -->
                    {{ user.email }}
                  </div>
                </div>
                <hr />
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">Phone</h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    <input
                      name="tel"
                      type="text"
                      class="form-control"
                      :value="user.tel"
                    />
                  </div>
                </div>
                <hr />
                <div class="row">
                  <div class="col-sm-3">
                    <h6 class="mb-0">About me</h6>
                  </div>
                  <div class="col-sm-9 text-secondary">
                    <textarea
                      name="bio"
                      class="form-control"
                      rows="3"
                      cols="20"
                      :value="user.bio"
                    ></textarea>
                  </div>
                </div>
              </form>
              <hr />
              <div class="row">
                <div class="col-sm-12">
                  <button class="btn btn-dark" @click="submitUserInfo">
                    Update
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
body {
  margin-top: 20px;
  color: #1a202c;
  text-align: left;
  background-color: #e2e8f0;
}
.main-body {
  padding: 15px;
}
.card {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 0 solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
}

.card-body {
  flex: 1 1 auto;
  min-height: 1px;
  padding: 1rem;
}

.gutters-sm {
  margin-right: -8px;
  margin-left: -8px;
}

.gutters-sm > .col,
.gutters-sm > [class*="col-"] {
  padding-right: 8px;
  padding-left: 8px;
}
.mb-3,
.my-3 {
  margin-bottom: 1rem !important;
}

.bg-gray-300 {
  background-color: #e2e8f0;
}
.h-100 {
  height: 100% !important;
}
.shadow-none {
  box-shadow: none !important;
}

#error-div {
  display: none;
}
</style>
<script>
import axios from "axios";

export default {
  name: "ProfileView",
  data() {
    return {
      user: null,
      myProfile: false,
      errors: [],
    };
  },
  created() {
    // Check if you can edit user profile
    if (this.$route.params.id == this.$store.state.id) {
      this.myProfile = true;
    }
    axios({
      method: "get",
      url: `http://127.0.0.1:8000/api/get-user/?id=${this.$route.params.id}`,
    })
      .then((response) => {
        // Get the first and only user from the response
        this.user = response.data.results[0];
      })
      .catch((err) => {
        console.log(err);
      });
  },
  methods: {
    submitImage() {
      var formData = new FormData();
      formData.append("avatar", document.querySelector("#profilna").files[0]);
      axios({
        method: "post",
        url: `http://127.0.0.1:8000/api/update-avatar/${this.$route.params.id}`,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
      })
        .then((response) => {
          console.log(response);
          this.user.get_avatar = response.data.get_avatar;
          this.user.get_thumbnail = response.data.get_thumbnail;
          document.getElementById("error-div").style.display = "none";
        })
        .catch((err) => {
          console.log(err);
          this.errors = [];
          for (let key in err.response.data) {
            this.errors.push(key + " : " + err.response.data[key]);
          }
          document.getElementById("error-div").style.display = "block";
        });
    },
    submitUserInfo() {
      console.log("Usao");
      var formData = new FormData(document.querySelector("#user-info"));
      axios({
        method: "post",
        url: `http://127.0.0.1:8000/api/update-user/${this.$route.params.id}`,
        data: formData,
        headers: { "Content-Type": "multipart/form-data", Authorization : `Bearer ${this.$store.state.accessToken}`},
      })
        .then((response) => {
          console.log(response);
          this.user = response.data;
          this.$router.push({ path: `/profile/${this.$store.state.id}` });
        })
        .catch((err) => {
          console.log(err);
          this.errors = [];
          for (let key in err.response.data) {
            this.errors.push(key + " : " + err.response.data[key]);
          }
          document.getElementById("error-div").style.display = "block";
        });
    },
  },
};
</script>

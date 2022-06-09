import { getAPI } from "@/axios-api";
import { createStore } from "vuex";

export default createStore({
  state: {
    accessToken: null,
    refreshToken: null,
    id: null,
    user: null,
    APIData: "",
  },
  getters: {
    loggedIn(state) {
      return state.accessToken != null;
    },
  },
  mutations: {
    updateStorage(state, { access, refresh, id, user }) {
      state.accessToken = access;
      state.refreshToken = refresh;
      state.id = id;
      state.user = user;
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", access);
      localStorage.setItem("id", id);
      localStorage.setItem("user", JSON.stringify(user));
    },
    destroyToken(state) {
      state.accessToken = null;
      state.refreshToken = null;
      state.id = null;
      state.user = null;
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("id");
      localStorage.removeItem("user");
    },
  },
  actions: {
    userLogout(context) {
      if (context.getters.loggedIn) {
        context.commit("destroyToken");
      }
    },
    userLogin(context, userCredentials) {
      return new Promise((resolve, reject) => {
        getAPI
          .post("/api/api-token/", {
            email: userCredentials.email,
            password: userCredentials.password,
          })
          .then((response) => {
            var access = response.data.access;
            var refresh = response.data.refresh;
            getAPI
              .get("/api/get-id/", {
                headers: { Authorization: `Bearer ${access}` },
              })
              .then((response) => {
                // TODO: Obrisi odmah posle testiranja
                console.log(response.data);
                console.log(response.data.id);
                context.commit("updateStorage", {
                  access: access,
                  refresh: refresh,
                  id: response.data["pk"],
                  user: response.data,
                });
              })
              .catch((err) => {
                console.log(err);
                reject();
              });
            resolve();
          })
          .catch((err) => {
            console.log(err);
            reject();
          });
      });
    },
    fetchAccessToken({ commit }) {
      commit("updateStorage", {
        access: localStorage.getItem("access"),
        refresh: localStorage.getItem("refresh"),
        id: localStorage.getItem("id"),
        user: localStorage.getItem("user"),
      });
    },
  },
  modules: {},
});

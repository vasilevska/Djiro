import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegistrationView from "../views/RegistrationView.vue";
import LoginView from "../views/LoginView.vue";

//Test
import MapaTest from "../views/MapaTest.vue";
//endTest

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/registration",
    name: "registration",
    component: RegistrationView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/mapa",
    name: "mapa",
    component: MapaTest,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

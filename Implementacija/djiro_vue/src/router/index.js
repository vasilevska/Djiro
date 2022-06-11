import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegistrationView from "../views/RegistrationView.vue";
import LoginView from "../views/LoginView.vue";
import ListingView from "../views/ListingView.vue";
import CarDetails from "@/views/CarDetails.vue";
import LogoutView from "../views/LogoutView.vue";
import VerificationView from "../views/VerificationView.vue";
import ProfileView from "../views/ProfileView.vue";
import EditProfile from "../views/EditProfile.vue";
import CreateListing from "../views/CreateListing.vue";
import UpdateListing from "../views/UpdateListingView.vue";
import Reservations from "../views/ReservationsView.vue"

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    // *** If you want to make page available ONLY if user is logged in, add below option to any of the routes: ***
    // meta: {
    //   requiresLogin: true,
    // },
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
    path: "/verification",
    name: "verification",
    component: VerificationView,
    meta: {
      requiresLogin: true,
    },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/listing",
    name: "listing",
    component: ListingView,
  },
  {
    path: "/:car_slug/",
    name: "carDetails",
    component: CarDetails,
  },
  {
    path: "/logout",
    name: "logout",
    component: LogoutView,
  },
  {
    path: "/profile/:id",
    name: "profile",
    component: ProfileView,
    props: true,
    // meta: {
    //   requiresLogin: true,
    // },
  },
  {
    path: "/edit-profile/:id",
    name: "edit-profile",
    component: EditProfile,
    props: true,
    meta: {
      requiresLogin: true,
      restrictedToUser: true,
    },
  },
  {
    path: "/reservations",
    name: "reservations",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Reservations,
  },
  {
    path: "/create-listing",
    name: "create-listing",
    component: CreateListing,
  },
  {
    path: "/update-listing/:car_slug",
    name: "UpdateCar",
    component: UpdateListing
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

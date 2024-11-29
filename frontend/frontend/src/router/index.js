import Vue from "vue";
import VueRouter from "vue-router";
import DashComponent from "../components/DashComponent.vue";
import LandingComponent from "../components/LandingComponent.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/dash",
    name: "Dash",
    component: DashComponent,
  },
  {
    path: "/Landing",
    name: "Landing",
    component: LandingComponent,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;

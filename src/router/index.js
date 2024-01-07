import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import DataView from "../views/DataView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        title: "Home",
      },
    },
    {
      path: "/data",
      name: "data",
      component: DataView,
      meta: {
        title: "Data",
      },
    }
  ],
});

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} | BI Project`;
  next();
});

export default router;

import { route } from "quasar/wrappers";
import { useAuthStore } from "src/stores/auth";
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import routes from "./routes";

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === "history"
    ? createWebHistory
    : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });
  const store = useAuthStore();

  Router.beforeEach(async (to, from, next) => {
    const isAuthorized = store.isAuthenticated
    const isAdmin = store.isAdmin
    const isManager = store.isManager
    store.pageLoading = true
    // console.debug("To: ", to, isAuthorized)

    if (isAuthorized && !store.account) {
      await store
        .loadAccountInfo()
        .then((resp) => {
          console.debug("Loaded account info: ", resp)
        })
        .catch((err) => {
          if (!store.account) {
            console.warn("Authorized but no accountInfo! Performing logout...", err)

            void store.logout().then(() => {
              void Router.push({
                name: "login",
                query: { next: to.fullPath },
              })
            })
          }
        })
    }

    const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin) || to.path.startsWith("admin")
    const requiresManager = to.matched.some((record) => record.meta.requiredManager) || to.path.startsWith("manage")

    if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthorized) {
      next({ name: "login", query: { next: to.fullPath } })
    } else if (requiresAdmin && !isAdmin) {
      console.debug("Admin required, redirected to login")
      next("/")
    } else if (requiresManager && !isManager) {
      console.debug("Manager required, redirected to login")
      next("/")
    } else if (to.name === "login" && isAuthorized) {
      console.debug("Already authorized")
      next({ name: "index" })
    } else {
      next()
    }
  })

  Router.afterEach(() => {
    store.pageLoading = false;
  });

  return Router;
});

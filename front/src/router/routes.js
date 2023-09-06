const routes = [
  // Manager
  {
    path: "/manager",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("pages/manager/IndexPage.vue"),
        name: "manager_index",
      },
    ],
  },
  // User
  {
    path: "/user",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("pages/user/IndexPage.vue"),
        name: "user_index",
      },
    ],
  },

  {
    path: "/",
    component: () => import("pages/IndexPage.vue"),
  },


  // Common
  {
    path: "/auth",
    component: () => import("layouts/EmptyLayout.vue"),
    children: [
      {
        path: "/login",
        component: () => import("pages/AccountLogin.vue"),
        name: "login",
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;

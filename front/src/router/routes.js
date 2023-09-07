const routes = [
  // Manager
  {
    path: "/manager",
    component: () => import("layouts/MainLayout.vue"),
    meta: {
      requiresManager: true,
    },
    children: [
      {
        path: "",
        component: () => import("pages/manager/IndexPage.vue"),
        name: "manager_index",
      },
      {
        path: "user",
        children: [
          {
            path: "",
            component: () => import("pages/admin/UserList.vue"),
            name: "admin_users"
          },
          {
            path: ":id",
            component: () => import("pages/admin/UserView.vue"),
            name: "admin_user"
          }
        ]
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
      {
        path: "product",
        children: [
          {
            path: "",
            component: () => import("pages/user/ProductList.vue"),
            name: "user_products"
          },
          {
            path: ":id",
            component: () => import("pages/user/ProductView.vue"),
            name: "user_product"
          }
        ]
      },
      {
        path: "category",
        children: [
          {
            path: "",
            component: () => import("pages/user/CategoryList.vue"),
            name: "user_categories"
          },
          {
            path: ":id",
            component: () => import("pages/user/CategoryView.vue"),
            name: "user_category"
          }
        ]
      },
      {
        path: "tasks",
        children: [
          {
            path: "",
            component: () => import("pages/user/TaskList.vue"),
            name: "user_tasks"
          },
          {
            path: ":id",
            component: () => import("pages/user/TaskView.vue"),
            name: "user_task"
          }
        ]
      },
    ],
  },

  {
    path: "",
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

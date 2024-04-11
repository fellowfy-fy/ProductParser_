const routes = [
  // Manager
  {
    path: "/manager",
    component: () => import("layouts/MainLayout.vue"),
    meta: {
      requiresManager: true,
      requiresAuth: true,
    },
    children: [
      {
        path: "",
        component: () => import("pages/manager/IndexPage.vue"),
        name: "manager_index",
      },
      {
        path: "user",
        meta: {
          requiresAdmin: true,
        },
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
      {
        path: "parse_settings",
        meta: {
          requiresAdmin: true,
        },
        children: [
          {
            path: "",
            component: () => import("pages/admin/TaskSettingsList.vue"),
            name: "admin_parse_settings"
          },
          {
            path: ":id",
            component: () => import("pages/admin/TaskSettingsView.vue"),
            name: "admin_parse_setting"
          }
        ]
      },
      {
        path: "preferences",
        meta: {
          requiresAdmin: true,
        },
        children: [
          {
            path: "",
            component: () => import("pages/admin/PreferencesList.vue"),
            name: "admin_preferences"
          },
          {
            path: ":id",
            component: () => import("pages/admin/PreferenceView.vue"),
            name: "admin_preference"
          }
        ]
      },
    ],
  },
  // User
  {
    path: "/user",
    component: () => import("layouts/MainLayout.vue"),
    meta: {
      requiresAuth: true,
    },
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
        path: "statusproduct",
        children: [
          {
            path: "",
            component: () => import("pages/user/StatusProductList.vue"),
            name: "user_statusproducts"
          },
          {
            path: ":id",
            component: () => import("pages/user/StatusProductView.vue"),
            name: "user_statusproduct"
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
          },
          {
            path: ":id/test",
            component: () => import("pages/user/TaskTest.vue"),
            name: "user_task_test"
          }
        ]
      },
      {
        path: "prices",
        children: [
          {
            path: "",
            component: () => import("pages/user/PriceHistory.vue"),
            name: "user_prices"
          },
        ]
      },
      {
        path: "reports",
        children: [
          {
            path: "",
            component: () => import("pages/user/ReportsList.vue"),
            name: "user_reports"
          },
        ]
      },
    ],
  },

  {
    path: "",
    name: "index",
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

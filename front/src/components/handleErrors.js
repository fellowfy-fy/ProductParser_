export const handleErrors = {
  data() {
    return { isOnLine: navigator.onLine };
  },
  mounted() {
    this.httpErrors = {};
    window.addEventListener("online", () => {
      this.isOnLine = true;
    });
    window.addEventListener("offline", () => {
      this.isOnLine = false;
    });
  },
  methods: {
    handleErrors(err, title) {
      console.warn(err, err.response, title);

      if (!title) {
        title = "Ошибка загрузки данных";
      }

      const data = err.response?.data || {};
      let respText;

      if (
        !err.response &&
        (!err.code ||
          err.code === "ERR_NETWORK" ||
          err.code == "ERR_INTERNET_DISCONNECTED")
      ) {
        respText = "Ошибка подключения к серверу";
      } else {
        respText = [err.response?.status, err.response?.statusText].join(" ");
      }

      let errValidation = "";

      if (typeof data === "object") {
        console.debug("Err data: ", data);
        try {
          for (const [key, val] of Object.entries(data)) {
            // console.debug(key, val);

            const errJoin = val.join(", ");
            errValidation += `${key}: ${errJoin}<br/>`;
          }
        } catch (err) {
          const errJoin = JSON.stringify(data);
        }
      }
      this.$q.notify({
        type: "negative",
        message: title,
        caption:
          data.detail ||
          data.code ||
          errValidation ||
          respText ||
          // data ||
          "Неизвестная ошибка",
        progress: true,
        html: true,
      });
    },
  },
};

export default handleErrors;

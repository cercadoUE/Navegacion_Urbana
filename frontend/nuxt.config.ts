export default defineNuxtConfig({
  compatibilityDate: "2026-06-21",
  devtools: { enabled: false },
  css: ["~/assets/css/main.css"],
  nitro: {
    preset: "static",
  },
  app: {
    head: {
      link: [
        {
          rel: "stylesheet",
          href: "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
        },
      ],
    },
  },
});

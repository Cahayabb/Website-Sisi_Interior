import axios from "axios";

const API = axios.create({
  baseURL: "https://rent-installation-utc-remedy.trycloudflare.com/api",
});

export default API;
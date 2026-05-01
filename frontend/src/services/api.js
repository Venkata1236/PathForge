import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: API_BASE });

export const generatePath = (payload) =>
  api.post("/generate-path", payload);

export const getHistory = () =>
  api.get("/history");

export default api;

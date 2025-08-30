import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000", // Flask backend URL
});

// Export your API functions
export const predict = (value) => API.post("/predict", { value });

export const getAlerts = () => API.get("/alerts"); // optional, for later use
export function getSeries() {
  return axios.get('/api/series')  // adjust endpoint
}
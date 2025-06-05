import axios from "axios";

// Set base URL for the API

export const axiosi = axios.create({
  withCredentials: true,
  // baseURL: "http://localhost:8000/",
  // baseURL: process.env.REACT_APP_BASE_URL,
  // baseURL: "https://ecomm-app-1.onrender.com",
  baseURL: "https://e-comm-app-leslie-23.vercel.app/",
  headers: {
    "Content-Type": "application/json",
  },
});

import axios from 'axios';

// Create a pre-configured instance of Axios
const api = axios.create({
  // This baseURL will change to your Render backend URL after deployment
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000, // Optional: Set a request timeout
});

// Optional: Add interceptors for requests (e.g., to add auth tokens) or responses (e.g., to handle errors)
// api.interceptors.request.use(...);
// api.interceptors.response.use(...);

export { api };
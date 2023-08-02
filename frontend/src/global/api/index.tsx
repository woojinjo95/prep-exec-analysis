import axios, { AxiosError } from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || `${window.location.protocol}//${window.location.hostname}:5000`,
})

API.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (!error.response) {
      throw error
    }

    throw error
  },
)

export default API

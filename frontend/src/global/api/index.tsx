import axios, { AxiosError } from 'axios'
import { AppURL } from '@global/constant'

const API = axios.create({
  baseURL: AppURL.backendURL,
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

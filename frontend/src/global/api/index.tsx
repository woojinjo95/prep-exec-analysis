import AppURL from '@global/constant/appURL'
import axios, { AxiosError } from 'axios'

const API = axios.create({
  baseURL: AppURL.baseURL,
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

import { AxiosError } from 'axios'
import API from '@global/api'
import { Response, ServiceState } from '@global/api/entity'
import apiUrls from './url'

/**
 * 서비스 상태 조회 api
 */
export const getServiceState = async () => {
  try {
    const result = await API.get<Response<{ state: ServiceState }>>(apiUrls.service_state)

    return result.data.items.state
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

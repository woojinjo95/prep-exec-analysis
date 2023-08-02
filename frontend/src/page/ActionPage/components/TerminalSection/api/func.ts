import { AxiosError } from 'axios'

import API from '@global/api'
import { Response } from '@global/api/entity'
import apiUrls from './url'
import { HardwareConfiguration } from './entity'

/**
 * 하드웨어 설정 조회 api
 */
export const getHardwareConfiguration = async () => {
  try {
    const result = await API.get<Response<HardwareConfiguration>>(apiUrls.hardware_configuration)

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

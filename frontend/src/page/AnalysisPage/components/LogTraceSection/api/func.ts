import API from '@global/api'
import { AxiosError } from 'axios'
import { Response } from '@global/api/entity'
import apiUrls from './url'
import { Logcat, Network } from './entity'

export const getLogcat = async ({ start_time, end_time }: { start_time: string; end_time: string }) => {
  try {
    const result = await API.get<Response<Logcat[]>>(apiUrls.logcat, {
      params: {
        start_time,
        end_time,
      },
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const getNetwork = async ({ start_time, end_time }: { start_time: string; end_time: string }) => {
  try {
    const result = await API.get<Response<Network[]>>(apiUrls.network, {
      params: {
        start_time,
        end_time,
      },
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

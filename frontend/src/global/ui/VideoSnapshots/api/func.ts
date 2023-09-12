import { AxiosError } from 'axios'
import API from '@global/api'
import { Response } from '@global/api/entity'
import { VideoSnapshot } from './entity'
import apiUrls from './url'

/**
 * 비디오 스냅샷 리스트 조회 api
 */
export const getVideoSnapshots = async (params: { scenario_id?: string; testrun_id?: string }) => {
  try {
    const result = await API.get<Response<VideoSnapshot[]>>(apiUrls.video_snapshot, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

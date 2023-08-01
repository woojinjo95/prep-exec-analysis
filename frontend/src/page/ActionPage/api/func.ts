import API from '@global/api'
import { AxiosError } from 'axios'
import { BlockData, ScenarioData } from '../entity/intex'
import apiUrls from './url'

export const getScenario = async () => {
  try {
    const result = await API.get<ScenarioData>(apiUrls.scenario)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const putScenario = async ({ newScenario }: { newScenario: ScenarioData }) => {
  try {
    const result = await API.put<{ msg: string }>(apiUrls.scenario, newScenario)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const postBlock = async ({ newBlock }: { newBlock: Omit<BlockData, 'id'> }) => {
  try {
    const result = await API.post<{ msg: string; id: string }>(apiUrls.block, newBlock)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const deleteBlock = async ({ block_ids }: { block_ids: string[] }) => {
  try {
    const result = await API.delete<{ msg: string }>(apiUrls.block, {
      data: {
        block_ids,
      },
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const putBlock = async ({ block_id, newBlock }: { block_id: string; newBlock: Omit<BlockData, 'id'> }) => {
  try {
    const result = await API.put<{ msg: string; id: string }>(`${apiUrls.block}/${block_id}`, newBlock)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const putBlockGroup = async ({ block_group_id, repeat_cnt }: { block_group_id: string; repeat_cnt: number }) => {
  try {
    const result = await API.put<{ msg: string }>(`${apiUrls.block_group}/${block_group_id}`, {
      repeat_cnt,
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

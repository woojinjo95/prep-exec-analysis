import API from '@global/api'
import { AxiosError } from 'axios'
import { Block, BlockGroup, Scenario } from '@page/ActionPage/components/ActionSection/api/entity'
import { Response } from '@global/api/entity'
import apiUrls from './url'

export const getScenarioById = async ({ scenario_id }: { scenario_id: string }) => {
  try {
    const result = await API.get<Response<Scenario>>(`${apiUrls.scenario}/${scenario_id}`)

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const putScenario = async ({ block_group, scenario_id }: { block_group: BlockGroup[]; scenario_id: string }) => {
  try {
    const result = await API.put<{ msg: string }>(`${apiUrls.scenario}/${scenario_id}`, { block_group })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

// post scenario
// TODO: 추후 구현 필요

// export const postScenario = async ({ newBlock }: { newBlock: Omit<Block, 'id'> }) => {
//   try {
//     const result = await API.post<{ msg: string; id: string }>(apiUrls.block, newBlock)

//     return result.data
//   } catch (err) {
//     const er = err as AxiosError
//     throw er
//   }
// }

export const postBlock = async ({ newBlock, scenario_id }: { newBlock: Omit<Block, 'id'>; scenario_id: string }) => {
  try {
    const result = await API.post<{ msg: string; id: string }>(`${apiUrls.block}/${scenario_id}`, newBlock)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const deleteBlock = async ({ block_ids, scenario_id }: { block_ids: string[]; scenario_id: string }) => {
  try {
    const result = await API.delete<{ msg: string }>(`${apiUrls.block}/${scenario_id}`, {
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

export const putBlock = async ({
  block_id,
  newBlock,
  scenario_id,
}: {
  block_id: string
  newBlock: Omit<Block, 'id'>
  scenario_id: string
}) => {
  try {
    const result = await API.put<{ msg: string; id: string }>(`${apiUrls.block}/${scenario_id}/${block_id}`, newBlock)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const putBlockGroup = async ({
  block_group_id,
  repeat_cnt,
  scenario_id,
}: {
  block_group_id: string
  repeat_cnt: number
  scenario_id: string
}) => {
  try {
    const result = await API.put<{ msg: string }>(`${apiUrls.block_group}/${scenario_id}/${block_group_id}`, {
      repeat_cnt,
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

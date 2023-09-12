import API from '@global/api'
import { AxiosError } from 'axios'
import { Block } from '@global/api/entity'
import apiUrls from './url'

export const postBlock = async ({ newBlock, scenario_id }: { newBlock: Omit<Block, 'id'>; scenario_id: string }) => {
  try {
    const result = await API.post<{ msg: string; id: string }>(`${apiUrls.block}/${scenario_id}`, newBlock)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const postBlocks = async ({
  newBlocks,
  scenario_id,
}: {
  newBlocks: Omit<Block, 'id'>[]
  scenario_id: string
}) => {
  try {
    const result = await API.post<{ msg: string; id: string }>(`${apiUrls.blocks}/${scenario_id}`, {
      blocks: newBlocks,
    })

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
    const result = await API.put<{ msg: string; id: string }>(
      `${apiUrls.block_group}/${scenario_id}/${block_group_id}`,
      {
        repeat_cnt,
      },
    )

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

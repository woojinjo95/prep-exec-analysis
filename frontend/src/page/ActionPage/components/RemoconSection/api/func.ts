import API from '@global/api'
import { AxiosError } from 'axios'
import { Response } from '@global/api/entity'
import apiUrls from './url'
import { CustomKey, Remocon } from './entity'

export const getRemocon = async () => {
  try {
    const result = await API.get<Response<Remocon[]>>(apiUrls.remocon)

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const putRemocon = async ({ remocon_id }: { remocon_id: string }) => {
  try {
    const result = await API.put<{ msg: string; id: string }>(`${apiUrls.remocon}/${remocon_id}`)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const postCustomKey = async ({
  newCustomKey,
}: {
  newCustomKey: { name: string; custom_code: string[]; remocon_id: string }
}) => {
  try {
    const result = await API.post<{ msg: string; id: string }>(apiUrls.custom_key, newCustomKey)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const deleteCustomKey = async ({
  remocon_id,
  custom_key_ids,
}: {
  remocon_id: string
  custom_key_ids: string[]
}) => {
  try {
    const result = await API.delete<{ msg: string }>(`${apiUrls.custom_key}/${remocon_id}`, {
      data: {
        custom_key_ids,
      },
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const putCustomKey = async ({
  remocon_id,
  custom_key_id,
  newCustomKey,
}: {
  remocon_id: string
  custom_key_id: string
  newCustomKey: {
    name: string
    custom_code: string[]
  }
}) => {
  try {
    const result = await API.put<{ msg: string; id: string }>(
      `${apiUrls.custom_key}/${remocon_id}/${custom_key_id}`,
      newCustomKey,
    )

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

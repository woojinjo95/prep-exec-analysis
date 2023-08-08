import API from '@global/api'
import { AxiosError } from 'axios'
import { Response } from '@global/api/entity'
import apiUrls from './url'
import { Remocon } from './entity'

export const getRemocon = async () => {
  try {
    const result = await API.get<Response<Remocon[]>>(apiUrls.remocon)

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const putRemocon = async ({ remocon_name }: { remocon_name: string }) => {
  try {
    const result = await API.put<{ msg: string; id: string }>(`${apiUrls.remocon}/${remocon_name}`)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

export const postCustomKey = async ({
  newCustomKey,
}: {
  newCustomKey: { name: string; custom_code: string[]; remocon_name: string }
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
  remocon_name,
  custom_key_ids,
}: {
  remocon_name: string
  custom_key_ids: string[]
}) => {
  try {
    const result = await API.delete<{ msg: string }>(`${apiUrls.custom_key}/${remocon_name}`, {
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
  remocon_name,
  custom_key_id,
  newCustomKey,
}: {
  remocon_name: string
  custom_key_id: string
  newCustomKey: {
    name: string
    custom_code: string[]
  }
}) => {
  try {
    const result = await API.put<{ msg: string; id: string }>(
      `${apiUrls.custom_key}/${remocon_name}/${custom_key_id}`,
      newCustomKey,
    )

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

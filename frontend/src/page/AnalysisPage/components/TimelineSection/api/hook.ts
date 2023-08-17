import { useQuery } from 'react-query'
import { getCPUAndMemory, getColorReferences, getEventLogs } from './func'

/**
 * CPU, Memory 사용률 리스트 조회 hook
 */
export const useCPUAndMemory = (params: Parameters<typeof getCPUAndMemory>[0]) => {
  const { data, isLoading, refetch } = useQuery(['cpu_and_memory', params], () => getCPUAndMemory(params))

  return { cpuAndMemory: data, isLoading, refetch }
}

/**
 * 이벤트 로그 리스트 조회 hook
 */
export const useEventLogs = (params: Parameters<typeof getEventLogs>[0]) => {
  const { data, isLoading, refetch } = useQuery(['event_log', params], () => getEventLogs(params))

  return { eventLogs: data, isLoading, refetch }
}

/**
 * Color Reference 리스트 조회 hook
 */
export const useColorReferences = (params: Parameters<typeof getColorReferences>[0]) => {
  const { data, isLoading, refetch } = useQuery(['color_reference', params], () => getColorReferences(params))

  return { colorReferences: data, isLoading, refetch }
}

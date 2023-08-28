import { useQuery } from 'react-query'
import { getCPU, getColorReferences, getEventLogs, getFreeze, getLogLevelFinders, getMemory } from './func'

/**
 * CPU 사용률 리스트 조회 hook
 */
export const useCPU = (params: Parameters<typeof getCPU>[0]) => {
  const { data, isLoading, refetch } = useQuery(['cpu', params], () => getCPU(params))

  return { cpu: data, isLoading, refetch }
}

/**
 * Memory 사용률 리스트 조회 hook
 */
export const useMemory = (params: Parameters<typeof getMemory>[0]) => {
  const { data, isLoading, refetch } = useQuery(['memory', params], () => getMemory(params))

  return { memory: data, isLoading, refetch }
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

/**
 * Freeze 리스트 조회 hook
 */
export const useFreeze = (params: Parameters<typeof getFreeze>[0]) => {
  const { data, isLoading, refetch } = useQuery(['freeze', params], () => getFreeze(params))

  return { freeze: data, isLoading, refetch }
}

/**
 * Log Level Finder 리스트 조회 hook
 */
export const useLogLevelFinders = (params: Parameters<typeof getLogLevelFinders>[0]) => {
  const { data, isLoading, refetch } = useQuery(['log_level_finder', params], () => getLogLevelFinders(params))

  return { logLevelFinders: data, isLoading, refetch }
}

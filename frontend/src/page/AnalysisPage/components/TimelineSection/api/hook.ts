import { useQuery } from 'react-query'
import { useWebsocket } from '@global/hook'
import { getCPU, getColorReferences, getEventLogs, getFreeze, getLogLevelFinders, getMemory } from './func'

/**
 * CPU 사용률 리스트 조회 hook
 */
export const useCPU = (params: Parameters<typeof getCPU>[0]) => {
  // TODO: 서비스 상태가 analysis이면 -> enabled: false
  const { data, isLoading, refetch } = useQuery(['cpu', params], () => getCPU(params))

  // FIXME: cpu 분석이 완료되면 refetch
  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'analysis_response') {
        refetch()
      }
    },
  })

  return { cpu: data, isLoading, refetch }
}

/**
 * Memory 사용률 리스트 조회 hook
 */
export const useMemory = (params: Parameters<typeof getMemory>[0]) => {
  const { data, isLoading, refetch } = useQuery(['memory', params], () => getMemory(params))

  // FIXME: memory 분석이 완료되면 refetch
  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'analysis_response') {
        refetch()
      }
    },
  })

  return { memory: data, isLoading, refetch }
}

/**
 * 이벤트 로그 리스트 조회 hook
 */
export const useEventLogs = (params: Parameters<typeof getEventLogs>[0]) => {
  const { data, isLoading, refetch } = useQuery(['event_log', params], () => getEventLogs(params))

  // FIXME: event log 분석이 완료되면 refetch
  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'analysis_response') {
        refetch()
      }
    },
  })

  return { eventLogs: data, isLoading, refetch }
}

/**
 * Color Reference 리스트 조회 hook
 */
export const useColorReferences = (params: Parameters<typeof getColorReferences>[0]) => {
  const { data, isLoading, refetch } = useQuery(['color_reference', params], () => getColorReferences(params))

  // FIXME: color reference 분석이 완료되면 refetch
  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'analysis_response') {
        refetch()
      }
    },
  })

  return { colorReferences: data, isLoading, refetch }
}

/**
 * Freeze 리스트 조회 hook
 */
export const useFreeze = (params: Parameters<typeof getFreeze>[0]) => {
  const { data, isLoading, refetch } = useQuery(['freeze', params], () => getFreeze(params))

  // FIXME: freeze 분석이 완료되면 refetch
  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'analysis_response') {
        refetch()
      }
    },
  })

  return { freeze: data, isLoading, refetch }
}

/**
 * Log Level Finder 리스트 조회 hook
 */
export const useLogLevelFinders = (params: Parameters<typeof getLogLevelFinders>[0]) => {
  const { data, isLoading, refetch } = useQuery(['log_level_finder', params], () => getLogLevelFinders(params))

  // FIXME: log level finder 분석이 완료되면 refetch
  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'analysis_response') {
        refetch()
      }
    },
  })

  return { logLevelFinders: data, isLoading, refetch }
}

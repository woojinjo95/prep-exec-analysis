import { useQuery } from 'react-query'
import { getCPUAndMemory } from './func'

/**
 * CPU, Memory 사용률 리스트 조회 hook
 */
export const useCPUAndMemory = (params: Parameters<typeof getCPUAndMemory>[0]) => {
  const { data, isLoading, refetch } = useQuery(['cpu_and_memory', params], () => getCPUAndMemory(params))

  return { cpuAndMemory: data, isLoading, refetch }
}

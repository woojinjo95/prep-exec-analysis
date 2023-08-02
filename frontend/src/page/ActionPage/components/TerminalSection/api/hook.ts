import { useQuery } from 'react-query'
import { getHardwareConfiguration } from './func'
import { HardwareConfiguration } from './entity'

/**
 * 하드웨어 설정 조회 hook
 */
export const useHardwareConfiguration = () => {
  const { data, isLoading, refetch } = useQuery<HardwareConfiguration>(['hardware-configuration'], () =>
    getHardwareConfiguration(),
  )

  return {
    hardwareConfiguration: data,
    isLoading,
    refetch,
  }
}

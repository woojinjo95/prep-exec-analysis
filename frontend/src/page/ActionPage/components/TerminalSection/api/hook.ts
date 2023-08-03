import { useQuery } from 'react-query'
import { useEffect } from 'react'
import { getHardwareConfiguration } from './func'
import { HardwareConfiguration } from './entity'

/**
 * 하드웨어 설정 조회 hook
 */
export const useHardwareConfiguration = ({ onSuccess }: { onSuccess?: (data: HardwareConfiguration) => void } = {}) => {
  const { data, isLoading, refetch } = useQuery<HardwareConfiguration>(
    ['hardware-configuration'],
    () => getHardwareConfiguration(),
    {
      onSuccess,
    },
  )

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  return {
    hardwareConfiguration: data,
    isLoading,
    refetch,
  }
}

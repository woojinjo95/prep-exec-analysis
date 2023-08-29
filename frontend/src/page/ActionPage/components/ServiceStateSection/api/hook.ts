import { useQuery } from 'react-query'
import { useEffect } from 'react'
import { ServiceState } from '@global/api/entity'
import { useWebsocket } from '@global/hook'
import { getServiceState } from './func'

/**
 * 서비스 상태 조회 hook
 */
export const useServiceState = ({
  onSuccess,
}: {
  onSuccess?: (data: ServiceState) => void
} = {}) => {
  const { data, isLoading, refetch } = useQuery(['service_state'], getServiceState, {
    onSuccess,
  })

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'service_state') {
        refetch()
      }
    },
  })

  return {
    serviceState: data,
    isLoading,
    refetch,
  }
}

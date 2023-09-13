import { useQuery } from 'react-query'
import { useEffect } from 'react'
import { useWebsocket } from '@global/hook'
import { getRunBlock } from './func'

/**
 * 실행중인 블럭 조회 hook
 */
export const useRunBlock = ({
  onSuccess,
}: {
  onSuccess?: (data: { id: string }) => void
} = {}) => {
  const { data, isLoading, refetch } = useQuery(['run_block'], getRunBlock, {
    onSuccess,
  })

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'next_playblock') {
        refetch()
      }
    },
  })

  return {
    runBlock: data,
    isLoading,
    refetch,
  }
}

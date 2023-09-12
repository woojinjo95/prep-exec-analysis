import { useQuery } from 'react-query'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useWebsocket } from '@global/hook'
import { getVideoSnapshots } from './func'

/**
 * 비디오 스냅샷 리스트 조회 hook
 */
export const useVideoSnapshots = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(
    ['video_snapshot', { scenarioId, testRunId }],
    () => getVideoSnapshots({ scenario_id: scenarioId!, testrun_id: testRunId! }),
    {
      enabled: !!scenarioId && !!testRunId,
    },
  )

  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'video_snapshots_response') {
        refetch()
      }
    },
  })

  return { videoSnapshots: data, isLoading, refetch }
}

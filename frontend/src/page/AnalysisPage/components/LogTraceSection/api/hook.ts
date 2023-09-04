import { useQuery } from 'react-query'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { getLogcat, getNetwork } from './func'

/**
 * Logcat 로그 조회 hook
 */
export const useLogcat = ({ enabled, ...params }: Parameters<typeof getLogcat>[0] & { enabled?: boolean }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(
    ['logcat', params],
    () => getLogcat({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
    { enabled },
  )

  return { logcats: data, isLoading, refetch }
}

/**
 * Network 로그 조회 hook
 */
export const useNetwork = ({ enabled, ...params }: Parameters<typeof getNetwork>[0] & { enabled?: boolean }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(
    ['network', params],
    () => getNetwork({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
    { enabled },
  )

  return { networks: data, isLoading, refetch }
}

import { useQuery } from 'react-query'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { getLogcat, getNetwork, getShellLogs, getShells } from './func'

/**
 * Logcat 로그 조회 hook
 */
export const useLogcat = ({ enabled, ...params }: Parameters<typeof getLogcat>[0] & { enabled?: boolean }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(
    ['logcat', { ...params, scenarioId, testRunId }],
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
    ['network', { ...params, scenarioId, testRunId }],
    () => getNetwork({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
    { enabled },
  )

  return { networks: data, isLoading, refetch }
}

/**
 * 쉘 탭 리스트 조회 hook
 */
export const useShells = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['shells', { scenarioId, testRunId }], () =>
    getShells({ scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  return { shells: data, isLoading, refetch }
}

/**
 * 쉘 로그 리스트 조회 hook
 */
export const useShellLogs = ({ enabled, ...params }: Parameters<typeof getShellLogs>[0] & { enabled?: boolean }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(
    ['shell_logs', { ...params, scenarioId, testRunId }],
    () => getShellLogs({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
    { enabled },
  )

  return { shellLogs: data, isLoading, refetch }
}

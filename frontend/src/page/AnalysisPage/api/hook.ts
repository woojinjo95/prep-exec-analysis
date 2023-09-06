import { scenarioIdState, testRunIdState } from '@global/atom'
import { useRecoilValue } from 'recoil'
import { useQuery } from 'react-query'
import { useEffect } from 'react'
import { AnalysisConfig } from './entity'
import { getAnalysisConfig } from './func'

/**
 * 분석 설정 조회 hook
 */
export const useAnalysisConfig = ({ onSuccess }: { onSuccess?: (data: AnalysisConfig) => void }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(
    ['analysis_config', { scenarioId, testRunId }],
    () => getAnalysisConfig({ scenario_id: scenarioId!, testrun_id: testRunId! }),
    {
      onSuccess,
      enabled: !!scenarioId && !!testRunId,
    },
  )

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  return { analysisConfig: data, isLoading, refetch }
}

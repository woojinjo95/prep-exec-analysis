import { useQuery } from 'react-query'
import { useEffect } from 'react'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useRecoilValue } from 'recoil'
import { getAnalysisConfig, getAnalysisResultSummary } from './func'
import { AnalysisConfig, AnalysisResultSummary } from './entity'

/**
 *
 * 분석 설정 조회 hook
 */
export const useAnalysisConfig = ({ onSuccess }: { onSuccess?: (data: AnalysisConfig) => void } = {}) => {
  const { data, isLoading, refetch } = useQuery(['analysis_config'], getAnalysisConfig, {
    onSuccess,
  })

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  return { analysisConfig: data, isLoading, refetch }
}

/**
 * 분석 결과(요약 데이터) 조회 api
 */
export const useAnalysisResultSummary = ({
  onSuccess,
  enabled,
  ...params
}: Parameters<typeof getAnalysisResultSummary>[0] & {
  onSuccess?: (data: AnalysisResultSummary) => void
  enabled?: boolean
}) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(
    ['analysis_result_summary', params],
    () =>
      getAnalysisResultSummary({
        ...params,
        scenario_id: scenarioId || undefined,
        testrun_id: testRunId || undefined,
      }),
    {
      onSuccess,
      enabled,
    },
  )

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  return { analysisResultSummary: data, isLoading, refetch }
}

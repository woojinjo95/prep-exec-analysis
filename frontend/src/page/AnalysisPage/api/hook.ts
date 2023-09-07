import { scenarioIdState, testRunIdState } from '@global/atom'
import { useRecoilValue } from 'recoil'
import { useQuery } from 'react-query'
import { useEffect } from 'react'
import { useVideoSummary } from '@global/api/hook'
import { AnalysisConfig, AnalysisResultSummary } from './entity'
import { getAnalysisConfig, getAnalysisResultSummary } from './func'

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

/**
 * 분석 결과(요약 데이터) 조회 api
 */
export const useAnalysisResultSummary = ({
  onSuccess,
}: {
  start_time: string | null
  end_time: string | null
  onSuccess?: (data: AnalysisResultSummary) => void
}) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const { data, isLoading, refetch } = useQuery(
    ['analysis_result_summary', { scenarioId, testRunId, ...videoSummary }],
    () =>
      getAnalysisResultSummary({
        start_time: videoSummary?.start_time!,
        end_time: videoSummary?.end_time!,
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      onSuccess,
      enabled: !!scenarioId && !!testRunId && !!videoSummary,
    },
  )

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  return { analysisResultSummary: data, isLoading, refetch }
}

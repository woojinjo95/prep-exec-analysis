import { useMutation } from 'react-query'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { AnalysisConfig } from '@page/AnalysisPage/api/entity'
import { AnalysisType } from '@global/constant'
import { deleteAnalysisConfig, putAnalysisConfig } from './func'

/**
 * 분석 설정 변경 hook
 */
export const useUpdateAnalysisConfig = ({
  onSuccess,
}: {
  onSuccess?: (
    data: void,
    variables: {
      scenario_id: string
      testrun_id: string
    } & AnalysisConfig,
    context: unknown,
  ) => void
}) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { mutate } = useMutation(putAnalysisConfig, {
    onSuccess,
  })

  const updateAnalysisConfig = (data: AnalysisConfig) => {
    if (!scenarioId || !testRunId) return
    mutate({ scenario_id: scenarioId, testrun_id: testRunId, ...data })
  }

  return {
    updateAnalysisConfig,
  }
}

/**
 * 분석 설정 삭제 hook
 */
export const useRemoveAnalysisConfig = ({
  onSuccess,
}: {
  onSuccess?: (
    data: void,
    variables: {
      scenario_id: string
      testrun_id: string
      analysis_type: keyof typeof AnalysisType
    },
    context: unknown,
  ) => void
}) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { mutate } = useMutation(deleteAnalysisConfig, {
    onSuccess,
  })

  const removeAnalysisConfig = (analysis_type: keyof typeof AnalysisType) => {
    if (!scenarioId || !testRunId) return
    mutate({ scenario_id: scenarioId, testrun_id: testRunId, analysis_type })
  }

  return {
    removeAnalysisConfig,
  }
}

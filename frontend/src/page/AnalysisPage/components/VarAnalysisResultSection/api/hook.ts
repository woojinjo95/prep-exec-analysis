import { useQuery } from 'react-query'
import { useEffect } from 'react'
import { getAnalysisConfig } from './func'
import { AnalysisConfig } from './entity'

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

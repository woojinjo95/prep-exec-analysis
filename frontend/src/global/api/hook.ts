import { useEffect } from 'react'
import { useQuery } from 'react-query'
import { PAGE_SIZE_FIFTEEN } from '@global/constant'
import { getScenarios } from './func'
import { PaginationResponse, ScenarioSummary } from './entity'

export const useScenarios = ({
  onSuccess,
  onError,
}: {
  onSuccess?: (data: PaginationResponse<ScenarioSummary[]>) => void
  onError?: (err: unknown) => void
}) => {
  const { data, isLoading, refetch } = useQuery(
    ['scenario_summary'],
    () =>
      getScenarios({
        page: 1,
        page_size: PAGE_SIZE_FIFTEEN,
      }),
    {
      onSuccess,
      onError,
    },
  )

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  return { scenarios: data, isLoading, refetch }
}

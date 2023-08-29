import { useEffect } from 'react'
import { useQuery } from 'react-query'
import { PAGE_SIZE_FIFTEEN } from '@global/constant'
import { getHardwareConfiguration, getScenarioById, getScenarios } from './func'
import { HardwareConfiguration, PaginationResponse, Scenario, ScenarioSummary } from './entity'

/**
 * 시나리오 리스트 조회 hook
 */
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

/**
 * 하드웨어 설정 조회 hook
 */
export const useHardwareConfiguration = ({ onSuccess }: { onSuccess?: (data: HardwareConfiguration) => void } = {}) => {
  const { data, isLoading, refetch } = useQuery<HardwareConfiguration>(
    ['hardware_configuration'],
    getHardwareConfiguration,
    {
      onSuccess,
    },
  )

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  return {
    hardwareConfiguration: data,
    isLoading,
    refetch,
  }
}

/**
 * 단건 시나리오 조회 Hook
 */

export const useScenarioById = ({
  onSuccess,
  scenarioId,
}: {
  onSuccess?: (data: Scenario) => void
  scenarioId: string | null
}) => {
  const { data, refetch, isLoading } = useQuery<Scenario>(
    ['scenario', scenarioId],
    () => getScenarioById({ scenario_id: scenarioId! }),
    {
      onSuccess,
      onError: (err) => {
        console.error(err)
      },
      enabled: !!scenarioId,
    },
  )

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  return {
    scenario: data,
    isLoading,
    refetch,
  }
}

import { useEffect } from 'react'
import { useQuery } from 'react-query'
import { PAGE_SIZE_FIFTEEN } from '@global/constant'
import { useWebsocket } from '@global/hook'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useRecoilValue } from 'recoil'
import {
  getHardwareConfiguration,
  getLogConnectionStatus,
  getServiceState,
  getScenarios,
  getScenarioById,
  getVideoSummary,
} from './func'
import {
  HardwareConfiguration,
  LogConnectionStatus,
  ServiceState,
  PaginationResponse,
  ScenarioSummary,
  Scenario,
  VideoSummary,
} from './entity'

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

/**
 * 서비스 상태 조회 hook
 */
export const useServiceState = ({
  onSuccess,
}: {
  onSuccess?: (data: ServiceState) => void
} = {}) => {
  const { data, isLoading, refetch } = useQuery(['service_state'], getServiceState, {
    onSuccess,
  })

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'service_state') {
        refetch()
      }
    },
  })

  return {
    serviceState: data,
    isLoading,
    refetch,
  }
}

/**
 * 로그 연결여부 조회 hook
 */
export const useLogConnectionStatus = ({
  onSuccess,
}: {
  onSuccess?: (data: LogConnectionStatus) => void
} = {}) => {
  const { data, isLoading, refetch } = useQuery(['log_connection_status'], getLogConnectionStatus, {
    onSuccess,
  })

  useEffect(() => {
    if (data) {
      onSuccess?.(data)
    }
  }, [data])

  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'log_connection_status') {
        refetch()
      }
    },
  })

  return {
    logConnectionStatus: data,
    isLoading,
    refetch,
  }
}

/**
 * 특정 시나리오의 테스트런이 수행한 시작시간 및 종료시간 조회 hook
 */
export const useVideoSummary = ({
  onSuccess,
}: {
  onSuccess?: (data: VideoSummary) => void
} = {}) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(
    ['video_summary', { scenarioId, testRunId }],
    () =>
      getVideoSummary({
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
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

  return {
    videoSummary: data,
    isLoading,
    refetch,
  }
}

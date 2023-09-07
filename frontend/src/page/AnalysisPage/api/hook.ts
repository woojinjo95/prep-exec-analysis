import { scenarioIdState, testRunIdState } from '@global/atom'
import { useRecoilValue } from 'recoil'
import { useQuery } from 'react-query'
import { useEffect, useMemo } from 'react'
import { useVideoSummary } from '@global/api/hook'
import { AnalysisType } from '@global/constant'
import { useWebsocket } from '@global/hook'
import { AnalysisConfig, AnalysisResultSummary } from './entity'
import {
  getAnalysisConfig,
  getAnalysisResultSummary,
  getBoot,
  getCPU,
  getColorReferences,
  getEventLogs,
  getFreeze,
  getLogLevelFinders,
  getLogPatternMatching,
  getLoudness,
  getMemory,
  getResume,
} from './func'

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

type AnalysisResponseMessageBody = {
  measurement: keyof typeof AnalysisType | 'color_reference'
}

/**
 * Log Level Finder 리스트 조회 hook
 */
export const useLogLevelFinders = (params: Pick<Parameters<typeof getLogLevelFinders>[0], 'log_level'>) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['log_level_finder', params],
    () =>
      getLogLevelFinders({
        ...params,
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (enabled && message.msg === 'analysis_response' && message.data.measurement === 'log_level_finder') {
        refetch()
      }
    },
  })

  return { logLevelFinders: data, isLoading, refetch }
}

/**
 * CPU 사용률 리스트 조회 hook
 */
export const useCPU = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['cpu'],
    () =>
      getCPU({
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  return { cpu: data, isLoading, refetch }
}

/**
 * Memory 사용률 리스트 조회 hook
 */
export const useMemory = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['memory'],
    () =>
      getMemory({
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  return { memory: data, isLoading, refetch }
}

/**
 * 이벤트 로그 리스트 조회 hook
 */
export const useEventLogs = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['event_log'],
    () =>
      getEventLogs({
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  return { eventLogs: data, isLoading, refetch }
}

/**
 * Color Reference 리스트 조회 hook
 */
export const useColorReferences = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['color_reference'],
    () =>
      getColorReferences({
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (enabled && message.msg === 'analysis_response' && message.data.measurement === 'color_reference') {
        refetch()
      }
    },
  })

  return { colorReferences: data, isLoading, refetch }
}

/**
 * Freeze 리스트 조회 hook
 */
export const useFreeze = (params: Pick<Parameters<typeof getFreeze>[0], 'freeze_type'>) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['freeze', params],
    () =>
      getFreeze({
        ...params,
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (enabled && message.msg === 'analysis_response' && message.data.measurement === 'freeze') {
        refetch()
      }
    },
  })

  return { freeze: data, isLoading, refetch }
}

/**
 * Loudness 리스트 조회 hook
 */
export const useLoudness = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['loudness'],
    () =>
      getLoudness({
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  return { loudness: data, isLoading, refetch }
}

/**
 * Resume 리스트 조회 hook
 */
export const useResume = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['resume'],
    () =>
      getResume({
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (enabled && message.msg === 'analysis_response' && message.data.measurement === 'resume') {
        refetch()
      }
    },
  })

  return { resume: data, isLoading, refetch }
}

/**
 * Boot 리스트 조회 hook
 */
export const useBoot = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['boot'],
    () =>
      getBoot({
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (enabled && message.msg === 'analysis_response' && message.data.measurement === 'boot') {
        refetch()
      }
    },
  })

  return { boot: data, isLoading, refetch }
}

/**
 * Log Pattern Matching 리스트 조회 hook
 */
export const useLogPatternMatching = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const enabled = useMemo(() => !!videoSummary && !!scenarioId && !!testRunId, [videoSummary, scenarioId, testRunId])

  const { data, isLoading, refetch } = useQuery(
    ['log_pattern_matching'],
    () =>
      getLogPatternMatching({
        start_time: new Date(videoSummary?.start_time!).toISOString(),
        end_time: new Date(videoSummary?.end_time!).toISOString(),
        scenario_id: scenarioId!,
        testrun_id: testRunId!,
      }),
    {
      enabled,
    },
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (enabled && message.msg === 'analysis_response' && message.data.measurement === 'log_pattern_matching') {
        refetch()
      }
    },
  })

  return { logPatternMatching: data, isLoading, refetch }
}

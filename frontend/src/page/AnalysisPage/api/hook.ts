import { scenarioIdState, testRunIdState } from '@global/atom'
import { useRecoilValue } from 'recoil'
import { useInfiniteQuery, useQuery } from 'react-query'
import { useEffect } from 'react'
import { useVideoSummary } from '@global/api/hook'
import { AnalysisType } from '@global/constant'
import { useIntersect, useWebsocket } from '@global/hook'
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
export const useLogLevelFinders = (params: Parameters<typeof getLogLevelFinders>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { videoSummary } = useVideoSummary()
  const { data, isLoading, refetch } = useQuery(
    ['log_level_finder', params],
    () => getLogLevelFinders({ ...params, scenario_id: scenarioId!, testrun_id: testRunId! }),
    {
      enabled: !!videoSummary && !!scenarioId && !!testRunId,
    },
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'log_level_finder') {
        refetch()
      }
    },
  })

  return { logLevelFinders: data, isLoading, refetch }
}

/**
 * CPU 사용률 리스트 조회 hook
 */
export const useCPU = (params: Parameters<typeof getCPU>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['cpu', params], () =>
    getCPU({ ...params, scenario_id: scenarioId!, testrun_id: testRunId || undefined }),
  )

  return { cpu: data, isLoading, refetch }
}

/**
 * Memory 사용률 리스트 조회 hook
 */
export const useMemory = (params: Parameters<typeof getMemory>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['memory', params], () =>
    getMemory({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  return { memory: data, isLoading, refetch }
}

/**
 * 이벤트 로그 리스트 조회 hook
 */
export const useEventLogs = (params: Parameters<typeof getEventLogs>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['event_log', params], () =>
    getEventLogs({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  return { eventLogs: data, isLoading, refetch }
}

/**
 * Color Reference 리스트 조회 hook
 */
export const useColorReferences = (params: Parameters<typeof getColorReferences>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['color_reference', params], () =>
    getColorReferences({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'color_reference') {
        refetch()
      }
    },
  })

  return { colorReferences: data, isLoading, refetch }
}

/**
 * Freeze 리스트 조회 hook
 */
export const useFreeze = (params: Parameters<typeof getFreeze>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['freeze', params], () =>
    getFreeze({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'freeze') {
        refetch()
      }
    },
  })

  return { freeze: data, isLoading, refetch }
}

/**
 * Loudness 리스트 조회 hook
 */
export const useLoudness = (params: Parameters<typeof getLoudness>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['loudness', params], () =>
    getLoudness({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  return { loudness: data, isLoading, refetch }
}

/**
 * Resume 리스트 조회 hook
 */
export const useResume = (params: Parameters<typeof getResume>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['resume', params], () =>
    getResume({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'resume') {
        refetch()
      }
    },
  })

  return { resume: data?.items, isLoading, refetch }
}

/**
 * Resume 무한스크롤 조회 hook
 */
export const useInfiniteResume = (params: Parameters<typeof getResume>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, hasNextPage, isFetching, fetchNextPage } = useInfiniteQuery(
    ['infinite_resume', params],
    ({ pageParam = 1 }) => {
      return getResume({
        ...params,
        page: pageParam as number,
        scenario_id: scenarioId || undefined,
        testrun_id: testRunId || undefined,
      })
    },
    {
      getNextPageParam: (lastPage) => {
        const nextPage = lastPage.next
        if (nextPage <= lastPage.pages) {
          return nextPage
        }

        return undefined
      },
    },
  )

  const ref = useIntersect((entry, observer) => {
    observer.unobserve(entry.target)
    if (hasNextPage && !isFetching) {
      fetchNextPage()
    }
  })

  return {
    resume: data?.pages.flatMap(({ items }) => items) || [],
    total: data?.pages.length ? data.pages[0].total : 0,
    loadingRef: ref,
    hasNextPage,
  }
}

/**
 * Boot 리스트 조회 hook
 */
export const useBoot = (params: Parameters<typeof getBoot>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['boot', params], () =>
    getBoot({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'boot') {
        refetch()
      }
    },
  })

  return { boot: data?.items, isLoading, refetch }
}

/**
 * Boot 무한스크롤 조회 hook
 */
export const useInfiniteBoot = (params: Parameters<typeof getBoot>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, hasNextPage, isFetching, fetchNextPage } = useInfiniteQuery(
    ['infinite_boot', params],
    ({ pageParam = 1 }) => {
      return getBoot({
        ...params,
        page: pageParam as number,
        scenario_id: scenarioId || undefined,
        testrun_id: testRunId || undefined,
      })
    },
    {
      getNextPageParam: (lastPage) => {
        const nextPage = lastPage.next
        if (nextPage <= lastPage.pages) {
          return nextPage
        }

        return undefined
      },
    },
  )

  const ref = useIntersect((entry, observer) => {
    observer.unobserve(entry.target)
    if (hasNextPage && !isFetching) {
      fetchNextPage()
    }
  })

  return {
    boot: data?.pages.flatMap(({ items }) => items) || [],
    total: data?.pages.length ? data.pages[0].total : 0,
    loadingRef: ref,
    hasNextPage,
  }
}

/**
 * Log Pattern Matching 리스트 조회 hook
 */
export const useLogPatternMatching = (params: Parameters<typeof getLogPatternMatching>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['log_pattern_matching', params], () =>
    getLogPatternMatching({ ...params, scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'log_pattern_matching') {
        refetch()
      }
    },
  })

  return { logPatternMatching: data?.items, isLoading, refetch }
}

/**
 * Log Pattern Matching 무한스크롤 조회 hook
 */
export const useInfiniteLogPatternMatching = (params: Parameters<typeof getLogPatternMatching>[0]) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, hasNextPage, isFetching, fetchNextPage } = useInfiniteQuery(
    ['infinite_log_pattern_matching', params],
    ({ pageParam = 1 }) => {
      return getLogPatternMatching({
        ...params,
        page: pageParam as number,
        scenario_id: scenarioId || undefined,
        testrun_id: testRunId || undefined,
      })
    },
    {
      getNextPageParam: (lastPage) => {
        const nextPage = lastPage.next
        if (nextPage <= lastPage.pages) {
          return nextPage
        }

        return undefined
      },
    },
  )

  const ref = useIntersect((entry, observer) => {
    observer.unobserve(entry.target)

    if (hasNextPage && !isFetching) {
      fetchNextPage()
    }
  })

  return {
    logPatternMatching: data?.pages.flatMap(({ items }) => items) || [],
    total: data?.pages.length ? data.pages[0].total : 0,
    loadingRef: ref,
    hasNextPage,
  }
}

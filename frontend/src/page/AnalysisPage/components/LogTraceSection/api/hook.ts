import { useInfiniteQuery, useQuery } from 'react-query'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { PAGE_SIZE_TEN } from '@global/constant'
import { useIntersect } from '@global/hook'
import { getLogcat, getNetwork, getShellLogs, getShells } from './func'

/**
 * Logcat 무한스크롤 조회 hook
 */
export const useInfiniteLogcat = ({ enabled, ...params }: Parameters<typeof getLogcat>[0] & { enabled?: boolean }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, hasNextPage, isFetching, fetchNextPage } = useInfiniteQuery(
    ['infinite_logcat', params],
    ({ pageParam = 1 }) => {
      return getLogcat({
        ...params,
        page: pageParam as number,
        page_size: PAGE_SIZE_TEN,
        scenario_id: scenarioId || undefined,
        testrun_id: testRunId || undefined,
      })
    },
    {
      enabled,
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
    logcats: data?.pages.flatMap(({ items }) => items) || [],
    loadingRef: ref,
    hasNextPage,
  }
}

/**
 * Network 무한스크롤 조회 hook
 */
export const useInfiniteNetwork = ({
  enabled,
  ...params
}: Parameters<typeof getNetwork>[0] & { enabled?: boolean }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, hasNextPage, isFetching, fetchNextPage } = useInfiniteQuery(
    ['infinite_network', params],
    ({ pageParam = 1 }) => {
      return getNetwork({
        ...params,
        page: pageParam as number,
        page_size: PAGE_SIZE_TEN,
        scenario_id: scenarioId || undefined,
        testrun_id: testRunId || undefined,
      })
    },
    {
      enabled,
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
    networks: data?.pages.flatMap(({ items }) => items) || [],
    loadingRef: ref,
    hasNextPage,
  }
}

/**
 * 쉘 탭 리스트 조회 hook
 */
export const useShells = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, isLoading, refetch } = useQuery(['shells', { scenarioId, testRunId }], () =>
    getShells({ scenario_id: scenarioId || undefined, testrun_id: testRunId || undefined }),
  )

  return { shells: data, isLoading, refetch }
}

/**
 * 쉘 로그 무한스크롤 조회 hook
 */
export const useInfiniteShellLogs = ({
  enabled,
  ...params
}: Parameters<typeof getShellLogs>[0] & { enabled?: boolean }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { data, hasNextPage, isFetching, fetchNextPage } = useInfiniteQuery(
    ['infinite_shell_logs', params],
    ({ pageParam = 1 }) => {
      return getShellLogs({
        ...params,
        page: pageParam as number,
        page_size: PAGE_SIZE_TEN,
        scenario_id: scenarioId || undefined,
        testrun_id: testRunId || undefined,
      })
    },
    {
      enabled,
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
    shellLogs: data?.pages.flatMap(({ items }) => items) || [],
    loadingRef: ref,
    hasNextPage,
  }
}

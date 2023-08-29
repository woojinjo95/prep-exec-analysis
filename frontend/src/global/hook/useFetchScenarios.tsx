import { PaginationResponse, ScenarioSummary } from '@global/api/entity'
import { getScenarios } from '@global/api/func'
import { QueryFunctionContext, useInfiniteQuery } from 'react-query'

/**
 * 무한스크롤로 scenarios를 가져올 hook
 * @param page_size 한번에 불러올 페이지 사이즈
 * @returns
 */
const useFetchScenarios = (page_size: number) =>
  useInfiniteQuery<PaginationResponse<ScenarioSummary[]>>(
    ['scenarios'],
    ({ pageParam = 1 }: QueryFunctionContext) => {
      return getScenarios({ page: pageParam as number, page_size })
    },
    {
      // getNextPageParam의 return 값이 pageParam 값으로 return 됨
      getNextPageParam: (lastPage) => {
        // lastPage : useInfiniteQuery의 return Type (PaginationResponse<ScenarioSummary[])
        const nextPage = lastPage.next

        if (nextPage <= lastPage.pages) {
          return nextPage
        }

        return undefined
      },
    },
  )

export default useFetchScenarios

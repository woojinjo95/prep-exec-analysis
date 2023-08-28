import { Text, Title } from '@global/ui'
import React, { useMemo, useState } from 'react'
import cx from 'classnames'
import { ReactComponent as MoreIcon } from '@assets/images/button_more.svg'
import { formatDateTo } from '@global/usecase'
import Scrollbars from 'react-custom-scrollbars-2'
import { QueryFunctionContext, useInfiniteQuery, useQuery } from 'react-query'
import { getScenarios } from '@global/api/func'
import useIntersect from '@global/hook/useIntersect'
import { PaginationResponse, ScenarioSummary } from '@global/api/entity'
import { useRecoilState } from 'recoil'
import { scenarioIdState } from '@global/atom'
import { useNavigate } from 'react-router-dom'

const FilesSection: React.FC = () => {
  const [selectedMenu, setSelectedMenu] = useState<'Blocks' | 'Analysis Results'>('Blocks')

  // const [current, setCurrent] = useState<number>(1)

  const { data, hasNextPage, isFetching, fetchNextPage } = useInfiniteQuery<PaginationResponse<ScenarioSummary[]>>(
    ['scenarios'],
    ({ pageParam = 1 }: QueryFunctionContext) => {
      return getScenarios({ page: pageParam as number })
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

    if (hasNextPage && !!isFetching) {
      // setCurrent((prev) => prev + 1)
      console.log('hi')
      fetchNextPage()
    }
  })

  const scenarios = useMemo(() => {
    return data ? data.pages.flatMap(({ items }) => items) : []
  }, [data])

  const [scenarioId, setScenarioId] = useRecoilState(scenarioIdState)

  const navigate = useNavigate()

  return (
    <div className="flex flex-col w-full h-full p-7 min-h-full border-r-[1px] border-b-grey">
      <div className="min-h-[100px]">
        <div className="flex justify-between mt-5">
          <Title as="h1" className="mb-5 text-white">
            Files
          </Title>
          <div className="flex">
            <Text size="md" className="mr-6 cursor-pointer">
              Search
            </Text>
            <Text size="md" className="cursor-pointer">
              Filter
            </Text>
          </div>
        </div>
        <div className="flex">
          <Text
            className={cx('!text-[15px] mr-[23px] cursor-pointer', {
              'text-primary': selectedMenu === 'Blocks',
              'text-white': selectedMenu !== 'Blocks',
            })}
            onClick={() => {
              setSelectedMenu('Blocks')
            }}
          >
            Blocks
          </Text>
          <Text
            className={cx('!text-[15px] cursor-pointer', {
              'text-primary': selectedMenu === 'Analysis Results',
              'text-white': selectedMenu !== 'Analysis Results',
            })}
            onClick={() => {
              setSelectedMenu('Analysis Results')
            }}
          >
            Analysis Results
          </Text>
        </div>
      </div>
      <div className="mt-5 flex w-full min-h-[calc(100%-100px)]">
        <div className="flex flex-col w-full">
          <div className="w-full grid grid-cols-[30%_40%_25%_5%] border-b-grey border-b-[1px] h-8 items-center">
            <Text className="text-sm" colorScheme="grey">
              Name
            </Text>
            <Text className="text-sm" colorScheme="grey">
              Tag
            </Text>
            <Text className="text-sm" colorScheme="grey">
              Last modified
            </Text>
            <div />
          </div>
          <Scrollbars
            renderThumbVertical={({ ...props }) => <div {...props} className="bg-[#4E525A] w-2 rounded-[5px]" />}
          >
            {scenarios?.map((scenario) => (
              <div className="flex flex-col w-full" key={`file_${scenario.name}`}>
                <div className="w-full grid grid-cols-[30%_40%_25%_5%] border-b-grey border-b-[1px] min-h-[48px] items-center">
                  <div>
                    <Text className="text-white mr-3" invertBackground colorScheme="light-orange">
                      B
                    </Text>
                    <Text
                      size="md"
                      colorScheme="light"
                      className="cursor-pointer"
                      onClick={() => {
                        setScenarioId(scenario.id)
                        navigate('/action')
                      }}
                    >
                      {scenario.name}
                    </Text>
                  </div>

                  <div className="flex flex-wrap w-full h-full pt-[10px] items-center">
                    {scenario.tags.map((tag) => (
                      <Text
                        className="text-white mr-2 mb-2"
                        invertBackground
                        colorScheme="dark-grey"
                        key={`${scenario.name}_tag_${tag}`}
                      >
                        {tag}
                      </Text>
                    ))}
                  </div>
                  <Text size="md" colorScheme="light">
                    {formatDateTo('M DD YYYY, HH:MM AA', new Date(scenario.updated_at))}
                  </Text>
                  <div className="flex justify-center cursor-pointer h-full">
                    <MoreIcon className="w-[20px] fill-white " />
                  </div>
                </div>
              </div>
            ))}
            {/* Intersect Target */}
            <div className="h-[5px]" ref={ref} />
          </Scrollbars>
        </div>
      </div>
    </div>
  )
}

export default FilesSection

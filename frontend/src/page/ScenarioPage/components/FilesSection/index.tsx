import { Text, Title } from '@global/ui'
import React, { useMemo, useState } from 'react'
import cx from 'classnames'
import { ReactComponent as MoreIcon } from '@assets/images/button_more.svg'
import { formatDateTo } from '@global/usecase'
import Scrollbars from 'react-custom-scrollbars-2'
import useIntersect from '@global/hook/useIntersect'
import { useRecoilState } from 'recoil'
import { scenarioIdState } from '@global/atom'
import { useNavigate } from 'react-router-dom'
import useFetchScenarios from '@global/hook/useFetchScenarios'
import { PAGE_SIZE_TWENTY } from '@global/constant'

const FilesSection: React.FC = () => {
  const [selectedMenu, setSelectedMenu] = useState<'Blocks' | 'Analysis Results'>('Blocks')

  const { data, hasNextPage, isFetching, fetchNextPage } = useFetchScenarios(PAGE_SIZE_TWENTY)

  const ref = useIntersect((entry, observer) => {
    // 발견시 실행될 callback
    observer.unobserve(entry.target)

    if (hasNextPage && !isFetching) {
      // 다음 페이지가 존재하고 isFetching이 아니라면
      fetchNextPage()
    }
  })

  const scenarios = useMemo(() => {
    // InfiniteData type의 data를 flatMap으로 1 depth 배열로 평탄화 작업
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
            <div
              className="min-h-[48px] border-b-grey border-b-[1px]"
              ref={ref}
              style={{ display: !hasNextPage ? 'none' : '' }}
            >
              {/* Loading spin 같은 로딩 UI가 필요 */}
              Loading...
            </div>
          </Scrollbars>
        </div>
      </div>
    </div>
  )
}

export default FilesSection

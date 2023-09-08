import { Button, Text, Title } from '@global/ui'
import React, { useMemo } from 'react'
import Scrollbars from 'react-custom-scrollbars-2'
import useIntersect from '@global/hook/useIntersect'
import useFetchScenarios from '@global/hook/useFetchScenarios'
import { PAGE_SIZE_TWENTY } from '@global/constant'
import { useMutation } from 'react-query'
import { postScenario } from '@global/api/func'
import { useNavigate } from 'react-router-dom'
import { useRecoilState } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useWebsocket } from '@global/hook'
import ScenarioItem from './ScenarioItem'

const FilesSection: React.FC = () => {
  const navigate = useNavigate()
  const { data, hasNextPage, isFetching, fetchNextPage } = useFetchScenarios(PAGE_SIZE_TWENTY)

  const ref = useIntersect((entry, observer) => {
    // 발견시 실행될 callback
    observer.unobserve(entry.target)

    if (hasNextPage && !isFetching) {
      // 다음 페이지가 존재하고 isFetching이 아니라면
      fetchNextPage()
    }
  })

  const { sendMessage } = useWebsocket()

  const scenarios = useMemo(() => {
    // InfiniteData type의 data를 flatMap으로 1 depth 배열로 평탄화 작업
    return data ? data.pages.flatMap(({ items }) => items) : []
  }, [data])

  const [, setScenarioId] = useRecoilState(scenarioIdState)

  const [, setTestRunId] = useRecoilState(testRunIdState)

  const { mutate: postScenarioMutate } = useMutation(postScenario, {
    onSuccess: (res) => {
      setScenarioId(res.id)
      setTestRunId(res.testrun_id)

      sendMessage({
        level: 'info',
        msg: 'action_mode',
      })
      navigate('/action')
    },
  })
  return (
    <div className="flex flex-col w-full h-full p-7 min-h-full border-r-[1px] border-b-grey">
      <div className="min-h-[100px]">
        <div className="flex justify-between mt-5 items-center">
          <Title as="h1" className="text-white flex">
            Project
          </Title>
          <Button
            className="!w-[190px] !h-[50px]"
            colorScheme="primary"
            onClick={() => {
              postScenarioMutate({ is_active: false })
            }}
          >
            New Workspace
          </Button>
        </div>
        <div className="flex w-full justify-between mt-5">
          <Text className="!text-[15px] mr-[23px] cursor-pointer !text-primary">All</Text>
          <div className="flex">
            <Text size="md" className="mr-6 cursor-pointer">
              Search
            </Text>
            <Text size="md" className="cursor-pointer">
              Filter
            </Text>
          </div>
        </div>
      </div>
      <div className="mt-5 flex w-full min-h-[calc(100%-100px)]">
        <div className="flex flex-col w-full">
          <div className="px-5 py-3 w-full">
            <div className="pl-[28px]">
              <div className="w-[calc(100%-96px)] grid grid-cols-[17.5%_35%_5%_12.5%_17.5%_5%_5%] min-h-8 items-center gap-x-4">
                <Text className="text-sm" colorScheme="grey">
                  Name
                </Text>
                <Text className="text-sm" colorScheme="grey">
                  Tag
                </Text>
                <Text className="text-sm" colorScheme="grey">
                  Block
                </Text>
                <Text className="text-sm" colorScheme="grey">
                  Number of Analysis Result
                </Text>
                <Text className="text-sm" colorScheme="grey">
                  Last Modified
                </Text>
                <div />
                <div />
              </div>
            </div>
          </div>
          <Scrollbars
            renderThumbVertical={({ ...props }) => <div {...props} className="bg-light-charcoal w-2 rounded-[5px]" />}
          >
            {scenarios?.map((scenario) => (
              <div className="flex flex-col w-full" key={`file_${scenario.name}`}>
                <ScenarioItem scenario={scenario} />
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
      {/* scenario 생성 모달
      생성했을 때 post scenario */}
    </div>
  )
}

export default FilesSection

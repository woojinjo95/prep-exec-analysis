import { ScenarioSummary } from '@global/api/entity'
import { getTestrun, postTestrun } from '@global/api/func'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { Accordion, Text } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import { AxiosError } from 'axios'
import React from 'react'
import { useMutation, useQuery } from 'react-query'
import { useNavigate } from 'react-router-dom'
import { useRecoilState } from 'recoil'

interface ScenarioItemProps {
  scenario: ScenarioSummary
}

const ScenarioItem: React.FC<ScenarioItemProps> = ({ scenario }) => {
  const { refetch } = useQuery(['testrun', scenario.id], () => getTestrun({ scenaroId: scenario.id }), {
    onSuccess: () => {
      console.log('tset')
    },
    enabled: false,
  })

  const [, setScenarioId] = useRecoilState(scenarioIdState)

  const navigate = useNavigate()

  const [, setTestRunId] = useRecoilState(testRunIdState)

  const { mutate: postTestrunMutate } = useMutation(postTestrun, {
    onSuccess: (res) => {
      setScenarioId(scenario.id)
      setTestRunId(res.id)
      navigate('/action')
    },
    onError: (err: AxiosError) => {
      console.error(err)
    },
  })

  return (
    <div className="mt-1">
      <Accordion
        onClick={() => {
          refetch()
        }}
        header={
          <div className="w-[calc(100%-24px)] grid grid-cols-[17.5%_35%_5%_12.5%_17.5%_5%_5%] min-h-8 gap-x-1 items-center">
            <Text colorScheme="light" size="md">
              {scenario.name}
            </Text>
            <div className="flex flex-wrap w-full">
              {scenario.tags.map((tag) => (
                <Text
                  className="text-white mr-2 h-full"
                  invertBackground
                  colorScheme="dark-grey"
                  key={`${scenario.name}_tag_${tag}`}
                >
                  {tag}
                </Text>
              ))}
            </div>
            <Text>{scenario.has_block ? 'true' : 'false'}</Text>
            <Text colorScheme="light" size="md">
              {scenario.testrun_count}
            </Text>
            <Text size="md" colorScheme="light">
              {formatDateTo('M DD YYYY, HH:MM AA', new Date(scenario.updated_at))}
            </Text>
            <Text
              className="w-[74px] h-7 cursor-pointer"
              colorScheme="light"
              onClick={(e) => {
                e.stopPropagation()
                postTestrunMutate(scenario.id)
              }}
            >
              Open
            </Text>
            <Text className="w-[74px] h-7 bg-light-charcoal">More</Text>
          </div>
        }
      >
        <div className="w-[calc(100%-8px)] grid grid-cols-[15%_63%_2%] min-h-8 gap-x-1 items-center" />
      </Accordion>
    </div>
  )
}

export default ScenarioItem

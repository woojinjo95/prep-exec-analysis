import { ScenarioSummary } from '@global/api/entity'
import { deleteTestrun, getTestrun } from '@global/api/func'
import { Text } from '@global/ui'
import React from 'react'
import { useMutation, useQuery } from 'react-query'
import { formatDateTo } from '@global/usecase'
import { useRecoilState } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useNavigate } from 'react-router-dom'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'

interface TestRunItemProps {
  scenarioSummary: ScenarioSummary
}

const TestRunItem: React.FC<TestRunItemProps> = ({ scenarioSummary }) => {
  const { data: testruns, refetch } = useQuery(['testrun', scenarioSummary.id], () =>
    getTestrun({ scenario_id: scenarioSummary.id }),
  )

  const [, setScenarioId] = useRecoilState(scenarioIdState)

  const navigate = useNavigate()

  const [, setTestRunId] = useRecoilState(testRunIdState)

  const { mutate: deleteTestrunMutate } = useMutation(deleteTestrun, {
    onSuccess: () => {
      refetch()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  return (
    <div className="flex flex-col w-full">
      <div className="px-5 py-3 w-full">
        <div>
          <div className="w-[calc(100%-32px)] grid grid-cols-[15%_80%_5%] min-h-8 items-center gap-x-4">
            <Text className="text-sm" colorScheme="grey">
              Last Updated
            </Text>
            <Text className="text-sm" colorScheme="grey">
              Analysis Item
            </Text>
            <div />
          </div>
        </div>
      </div>
      {testruns?.map((testrun) => (
        <div
          key={`scenario_${scenarioSummary.id}_testrun_${testrun.id}`}
          className="mt-1 px-5 py-3 w-full min-h-8 bg-charcoal rounded-lg cursor-pointer"
          onClick={() => {
            setScenarioId(scenarioSummary.id)
            setTestRunId(testrun.id)
            navigate('/analysis')
          }}
        >
          <div>
            <div className="w-[calc(100%-32px)] grid grid-cols-[15%_83%_2%] min-h-8 items-center gap-x-4 ">
              <Text className="text-sm" colorScheme="light">
                {formatDateTo('M DD YYYY, HH:MM AA', new Date(testrun.updated_at))}
              </Text>
              <Text className="text-sm" colorScheme="light">
                {testrun.measure_targets.join(', ')}
              </Text>
              <TrashIcon
                className="w-4 fill-white cursor-pointer"
                onClick={(e) => {
                  e.stopPropagation()
                  if (window.confirm('do you really want to delete this testrun?')) {
                    deleteTestrunMutate({ scenario_id: scenarioSummary.id, testrun_id: testrun.id })
                  }
                }}
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default TestRunItem

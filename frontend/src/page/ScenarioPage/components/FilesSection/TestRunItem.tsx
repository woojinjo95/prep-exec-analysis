import { ScenarioSummary } from '@global/api/entity'
import { getTestrun } from '@global/api/func'
import { Text } from '@global/ui'
import React from 'react'
import { useQuery } from 'react-query'
import { formatDateTo } from '@global/usecase'
import { useRecoilState } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useNavigate } from 'react-router-dom'

interface TestRunItemProps {
  scenario: ScenarioSummary
}

const TestRunItem: React.FC<TestRunItemProps> = ({ scenario }) => {
  const { data: testruns } = useQuery(['testrun', scenario.id], () => getTestrun({ scenaroId: scenario.id }))

  const [, setScenarioId] = useRecoilState(scenarioIdState)

  const navigate = useNavigate()

  const [, setTestRunId] = useRecoilState(testRunIdState)

  return (
    <div className="flex flex-col w-full">
      <div className="px-5 py-3 w-full">
        <div>
          <div className="w-[calc(100%-32px)] grid grid-cols-[15%_80%_5%] min-h-8 items-center gap-x-4">
            <Text className="text-sm" colorScheme="grey">
              Last Updated
            </Text>
            <Text className="text-sm" colorScheme="grey">
              Analyis Item
            </Text>
            <div />
          </div>
        </div>
      </div>
      {testruns?.map((testrun) => (
        <div
          key={`scenario_${scenario.id}_testrun_${testrun.id}`}
          className="mt-1 px-5 py-3 w-full min-h-8 bg-charcoal rounded-lg cursor-pointer"
          onClick={() => {
            setScenarioId(scenario.id)
            setTestRunId(testrun.id)
            navigate('/analysis')
          }}
        >
          <div>
            <div className="w-[calc(100%-32px)] grid grid-cols-[15%_80%_5%] min-h-8 items-center gap-x-4 ">
              <Text className="text-sm" colorScheme="grey">
                {formatDateTo('M DD YYYY, HH:MM AA', new Date(testrun.updated_at))}
              </Text>
              <Text className="text-sm" colorScheme="grey">
                {testrun.analysis_targets.join(',')}
              </Text>
              <div />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default TestRunItem

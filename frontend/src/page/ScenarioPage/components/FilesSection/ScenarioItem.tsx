import { ScenarioSummary } from '@global/api/entity'
import { deleteScenario, postTestrun } from '@global/api/func'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { Accordion, DropdownWithMoreButton, OptionItem, Text } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import { AxiosError } from 'axios'
import React, { useState } from 'react'
import { useMutation } from 'react-query'
import { useNavigate } from 'react-router-dom'
import { useRecoilState } from 'recoil'
import { useWebsocket } from '@global/hook'
import { ReactComponent as ValidIcon } from '@assets/images/icon_Is_valid.svg'
import { ReactComponent as InvalidIcon } from '@assets/images/icon_invalid.svg'
import TestRunItem from './TestRunItem'
import ModifyProjectModal from './ModifyProjectModal'

interface ScenarioItemProps {
  scenarioSummary: ScenarioSummary
  scenariosRefetch: () => void
}

const ScenarioItem: React.FC<ScenarioItemProps> = ({ scenarioSummary, scenariosRefetch }) => {
  const [, setScenarioId] = useRecoilState(scenarioIdState)

  const navigate = useNavigate()

  const [, setTestRunId] = useRecoilState(testRunIdState)

  const { sendMessage } = useWebsocket()

  const [isModifyScenarioModalOpen, setIsModifyScenarioModalOpen] = useState<boolean>(false)

  const { mutate: postTestrunMutate } = useMutation(postTestrun, {
    onSuccess: (res) => {
      setScenarioId(scenarioSummary.id)
      setTestRunId(res.id)

      sendMessage({
        level: 'info',
        msg: 'action_mode',
      })
      navigate('/action')
    },
    onError: (err: AxiosError) => {
      console.error(err)
    },
  })

  const { mutate: deleteScenarioMutate } = useMutation(deleteScenario, {
    onSuccess: () => {
      scenariosRefetch()
    },
    onError: () => {
      alert('시나리오 삭제에 실패하였습니다')
      scenariosRefetch()
    },
  })

  return (
    <div className="mt-1">
      <Accordion
        header={
          <div className="w-[calc(100%-96px)] grid grid-cols-[20.5%_37%_5%_12.5%_17.5%_5%_3%] min-h-8 gap-x-4 items-center">
            <Text colorScheme="light" size="md">
              {scenarioSummary.name}
            </Text>
            <div className="flex flex-wrap w-full">
              {scenarioSummary.tags.map((tag) => (
                <Text
                  className="text-white mr-2 h-full"
                  invertBackground
                  colorScheme="dark-grey"
                  key={`${scenarioSummary.name}_tag_${tag}`}
                >
                  {tag}
                </Text>
              ))}
            </div>
            {/* <Text>{scenario.has_block ? 'true' : 'false'}</Text> */}
            {scenarioSummary.has_block ? <ValidIcon className="w-[22px]" /> : <InvalidIcon className="w-[22px]" />}
            <Text colorScheme="light" size="md">
              {scenarioSummary.testrun_count}
            </Text>
            <Text size="md" colorScheme="light">
              {formatDateTo('M DD YYYY, HH:MM AA', new Date(scenarioSummary.updated_at))}
            </Text>
            <Text
              className="w-[74px] h-7 cursor-pointer flex justify-center !rounded-[14px]"
              colorScheme="light-charcoal"
              invertBackground
              onClick={(e) => {
                e.stopPropagation()
                postTestrunMutate(scenarioSummary.id)
              }}
            >
              Open
            </Text>
            <DropdownWithMoreButton colorScheme="charcoal" type="icon">
              <OptionItem
                colorScheme="charcoal"
                onClick={() => {
                  setIsModifyScenarioModalOpen(true)
                }}
              >
                Modify
              </OptionItem>
              <OptionItem
                colorScheme="charcoal"
                onClick={(e) => {
                  e.stopPropagation()
                  if (!scenarioSummary) return

                  if (window.confirm('do you really want to delete this scenario?')) {
                    deleteScenarioMutate({ scenario_id: scenarioSummary.id })
                  }
                }}
              >
                Delete
              </OptionItem>
            </DropdownWithMoreButton>
          </div>
        }
      >
        <TestRunItem scenarioSummary={scenarioSummary} />
      </Accordion>
      {isModifyScenarioModalOpen && (
        <ModifyProjectModal
          isOpen={isModifyScenarioModalOpen}
          close={() => {
            setIsModifyScenarioModalOpen(false)
          }}
          scenarioSummary={scenarioSummary}
          scenariosRefetch={scenariosRefetch}
        />
      )}
    </div>
  )
}

export default ScenarioItem

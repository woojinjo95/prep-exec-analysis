import React, { useState } from 'react'
import { ReactComponent as RecordIcon } from '@assets/images/icon_record.svg'
import { ReactComponent as PlayIcon } from '@assets/images/icon_play.svg'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { ReactComponent as StopIcon } from '@assets/images/icon_stop.svg'

import { IconButton, OptionItem, Text, DropdownWithMoreButton, Input } from '@global/ui'
import { useWebsocket } from '@global/hook'
import { useRecoilState, useRecoilValue } from 'recoil'
import {
  isBlockRecordModeState,
  playStartTimeState,
  scenarioIdState,
  selectedBlockIdsState,
  testRunIdState,
} from '@global/atom'
import { useScenarioById, useServiceState } from '@global/api/hook'
import { useMutation } from 'react-query'
import cx from 'classnames'
import { useNavigate } from 'react-router-dom'
import { blockControlMenu } from '../constants'
import SaveBlocksModal from './SaveBlocksModal'
import OpenBlocksModal from './OpenBlocksModal'
import { deleteBlock, putBlockGroup } from '../api/func'
import AddMonkeyTestBlockModal from './AddMonkeyTestBlockModal'
import AddIntelligentMonkeyTestBlockModal from './AddIntelligentMonkeyTestBlockModal'

const BlockControls: React.FC = () => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testrunId = useRecoilValue(testRunIdState)

  const navigate = useNavigate()

  const [isSaveBlocksModalOpen, setIsSaveBlocksModalOpen] = useState<boolean>(false)
  const [isOpenBlocksModalOpen, setIsOpenBlocksModalOpen] = useState<boolean>(false)
  const [isAddMonkeyTestBlockModalOpen, setIsAddMonkeyTestBlockModalOpen] = useState<boolean>(false)
  const [isAddIntelligentMonkeyTestBlockModalOpen, setIsAddIntelligentMonkeyTestBlockModalOpen] =
    useState<boolean>(false)

  const [isBlockRecordMode, setIsBlockRecordMode] = useRecoilState(isBlockRecordModeState)

  // 최소 1을 가지고 있음
  const [repeatCnt, setRepeatCnt] = useState<number>(1)

  const { scenario, refetch } = useScenarioById({
    scenarioId,
    testrunId,
    onSuccess: (res) => {
      if (res.block_group.length > 0) {
        setRepeatCnt(res.block_group[0].repeat_cnt)
      }
    },
  })

  const { serviceState } = useServiceState()

  const { mutate: deleteBlocksMutate } = useMutation(deleteBlock, {
    onSuccess: () => {
      refetch()
    },
  })

  const { mutate: putBlockGroupMutate } = useMutation(putBlockGroup, {
    onSuccess: () => {
      refetch()
    },
  })

  const selectedBlockIds = useRecoilValue(selectedBlockIdsState)

  // 재생 시작했던 시간
  const [playStartTime, setPlayStartTime] = useRecoilState(playStartTimeState)

  const [isPlay, setIsPlay] = useState<boolean>(false)

  const { sendMessage } = useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'end_playblock') {
        if (!playStartTime) return
        navigate('/analysis')
      }
    },
  })

  if (!scenario) return <div />

  return (
    <>
      <div className="flex flex-wrap items-center px-3 py-2 gap-y-2 border-t border-[#DFE0EE] bg-white">
        <div className="flex items-center">
          <DropdownWithMoreButton positionX="left" disabled={serviceState === 'playblock'}>
            {blockControlMenu?.map((menu) => (
              <OptionItem
                disabled={
                  !isBlockRecordMode &&
                  (menu === 'Add Monkey Test Block' || menu === 'Add Intelligent Monkey Test Block')
                }
                colorScheme="light"
                key={`menu_${menu}`}
                onClick={() => {
                  if (menu === 'Save') {
                    setIsSaveBlocksModalOpen(true)
                  }
                  if (menu === 'Open') {
                    setIsOpenBlocksModalOpen(true)
                  }
                  if (menu === 'Add Monkey Test Block' && isBlockRecordMode) {
                    setIsAddMonkeyTestBlockModalOpen(true)
                  }
                  if (menu === 'Add Intelligent Monkey Test Block' && isBlockRecordMode) {
                    setIsAddIntelligentMonkeyTestBlockModalOpen(true)
                  }
                }}
              >
                {menu}
              </OptionItem>
            ))}
          </DropdownWithMoreButton>

          {scenario.block_group.length > 0 && (
            <>
              <Input
                disabled={serviceState === 'playblock'}
                colorScheme="light"
                className={cx('!w-[74px] !h-10 ml-3 mr-1', { '!bg-light-grey': serviceState === 'playblock' })}
                value={repeatCnt}
                type="number"
                onChange={(e) => {
                  setRepeatCnt(Number(e.target.value))
                }}
                onBlur={() => {
                  if (!scenario) return

                  // 같을 때는 불필요하게 api 호출 X
                  if (repeatCnt === scenario.block_group[0].repeat_cnt) return

                  putBlockGroupMutate({
                    block_group_id: scenario.block_group[0].id,
                    repeat_cnt: repeatCnt,
                    scenario_id: scenario.id,
                  })
                }}
              />
              <Text colorScheme="dark" weight="bold" size="sm">
                Repeat
              </Text>
            </>
          )}
        </div>

        <div className="flex items-center gap-x-1 ml-auto">
          {!isBlockRecordMode ? (
            <IconButton
              colorScheme="none"
              className="disabled:bg-light-grey"
              icon={<RecordIcon className="!fill-red" />}
              onClick={() => {
                setIsBlockRecordMode((prev) => !prev)
              }}
              disabled={serviceState === 'playblock'}
            />
          ) : (
            <IconButton
              colorScheme="none"
              className="disabled:bg-light-grey"
              icon={<StopIcon className="!fill-red" />}
              onClick={() => {
                setIsBlockRecordMode((prev) => !prev)
              }}
              disabled={serviceState === 'playblock'}
            />
          )}

          {serviceState !== 'playblock' ? (
            <IconButton
              className="disabled:bg-light-grey"
              disabled={isBlockRecordMode}
              icon={<PlayIcon />}
              onClick={() => {
                if (!scenarioId) return

                // new workspace로 진입했을 때
                if (scenario.is_active === false) {
                  if (window.confirm('Do you want to save the block?')) {
                    // 블럭 저장 모달 실행
                    setIsPlay(true)
                    setIsSaveBlocksModalOpen(true)
                  } else {
                    // 재생
                    sendMessage({
                      level: 'info',
                      msg: 'start_playblock',
                      data: { scenario_id: scenarioId },
                    })

                    setPlayStartTime(new Date().getTime() / 1000)
                  }

                  return
                }

                sendMessage({
                  level: 'info',
                  msg: 'start_playblock',
                  data: { scenario_id: scenarioId },
                })

                setPlayStartTime(new Date().getTime() / 1000)

                // setIsPlay(true)
              }}
            />
          ) : (
            <IconButton
              className="disabled:bg-light-grey"
              disabled={isBlockRecordMode}
              icon={
                <StopIcon
                  onClick={() => {
                    sendMessage({
                      level: 'info',
                      msg: 'stop_playblock',
                    })
                  }}
                />
              }
            />
          )}

          <IconButton
            className="disabled:bg-light-grey"
            disabled={serviceState === 'playblock'}
            icon={<TrashIcon />}
            onClick={() => {
              if (!scenarioId) return

              deleteBlocksMutate({
                block_ids: selectedBlockIds,
                scenario_id: scenarioId,
              })
            }}
          />
          <div
            className={cx(
              'flex justify-center items-center border border-[#DFE0EE] h-[40px] w-[74px] rounded-[20px] text-[14px] font-medium cursor-pointer',
              { 'cusror-none bg-light-grey': serviceState === 'playblock' },
            )}
            onClick={() => {
              if (!scenarioId) return
              // TODO: blockgroup이 하나라는 가정
              deleteBlocksMutate({
                block_ids: scenario.block_group[0].block.map((block) => block.id),
                scenario_id: scenarioId,
              })
            }}
          >
            <Text size="sm" colorScheme="dark" weight="medium">
              Clear
            </Text>
          </div>
        </div>
      </div>
      {isSaveBlocksModalOpen && (
        <SaveBlocksModal
          isOpen={isSaveBlocksModalOpen}
          close={() => {
            setIsSaveBlocksModalOpen(false)
          }}
          isMoveAnalysisPage={false}
          isPlay={isPlay}
        />
      )}
      {isOpenBlocksModalOpen && (
        <OpenBlocksModal isOpen={isOpenBlocksModalOpen} close={() => setIsOpenBlocksModalOpen(false)} />
      )}
      {isAddMonkeyTestBlockModalOpen && (
        <AddMonkeyTestBlockModal
          isOpen={isAddMonkeyTestBlockModalOpen}
          close={() => setIsAddMonkeyTestBlockModalOpen(false)}
        />
      )}
      {isAddIntelligentMonkeyTestBlockModalOpen && (
        <AddIntelligentMonkeyTestBlockModal
          isOpen={isAddIntelligentMonkeyTestBlockModalOpen}
          close={() => setIsAddIntelligentMonkeyTestBlockModalOpen(false)}
        />
      )}
    </>
  )
}

export default BlockControls

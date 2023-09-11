import React, { useState } from 'react'
import { ReactComponent as RecordIcon } from '@assets/images/icon_record.svg'
import { ReactComponent as PlayIcon } from '@assets/images/icon_play.svg'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { ReactComponent as StopIcon } from '@assets/images/icon_stop.svg'

import { IconButton, OptionItem, Text, DropdownWithMoreButton } from '@global/ui'
import { useWebsocket } from '@global/hook'
import { useRecoilState, useRecoilValue } from 'recoil'
import {
  isBlockRecordModeState,
  isTestOptionModalOpenState,
  playStartTimeState,
  scenarioIdState,
  selectedBlockIdsState,
} from '@global/atom'
import { useScenarioById, useServiceState } from '@global/api/hook'
import { useMutation } from 'react-query'
import cx from 'classnames'
import { useNavigate } from 'react-router-dom'
import { blockControlMenu } from '../constants'
import SaveBlocksModal from './SaveBlocksModal'
import OpenBlocksModal from './OpenBlocksModal'
import { deleteBlock } from '../api/func'
import AddMonkeyTestBlockModal from './AddMonkeyTestBlockModal'
import AddIntelligentMonkeyTestBlockModal from './AddIntelligentMonkeyTestBlockModal'
import TestOptionModal from './TestOptionModal'

const BlockControls: React.FC = () => {
  const scenarioId = useRecoilValue(scenarioIdState)

  const navigate = useNavigate()

  const [isSaveBlocksModalOpen, setIsSaveBlocksModalOpen] = useState<boolean>(false)
  const [isOpenBlocksModalOpen, setIsOpenBlocksModalOpen] = useState<boolean>(false)
  const [isAddMonkeyTestBlockModalOpen, setIsAddMonkeyTestBlockModalOpen] = useState<boolean>(false)
  const [isAddIntelligentMonkeyTestBlockModalOpen, setIsAddIntelligentMonkeyTestBlockModalOpen] =
    useState<boolean>(false)
  const [isTestOptionModalOpen, setIsTesetOptionModalOpen] = useRecoilState(isTestOptionModalOpenState)

  const [isBlockRecordMode, setIsBlockRecordMode] = useRecoilState(isBlockRecordModeState)

  const { scenario, refetch } = useScenarioById({ scenarioId })

  const { serviceState } = useServiceState()

  const { mutate: deleteBlocksMutate } = useMutation(deleteBlock, {
    onSuccess: () => {
      refetch()
    },
  })

  const selectedBlockIds = useRecoilValue(selectedBlockIdsState)

  // 재생 시작했던 시간
  const playStartTime = useRecoilValue(playStartTimeState)

  const [isPlay, setIsPlay] = useState<boolean>(false)

  const { sendMessage } = useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'end_playblock') {
        // analysis_mode message 전송 후 이동
        if (!playStartTime) return
        sendMessage({
          level: 'info',
          msg: 'analysis_mode_init',
          data: {
            start_time: playStartTime,
            end_time: new Date().getTime() / 1000,
          },
        })
        navigate('/analysis')
      }
    },
  })

  if (!scenario) return <div />

  return (
    <>
      <div className="flex flex-wrap items-center px-3 py-2 gap-y-2 border-t border-[#DFE0EE] bg-white">
        <div className="flex items-center">
          <DropdownWithMoreButton positionX="left">
            {blockControlMenu?.map((menu) => (
              <OptionItem
                colorScheme="light"
                key={`menu_${menu}`}
                onClick={() => {
                  if (menu === 'Save') {
                    setIsSaveBlocksModalOpen(true)
                  }
                  if (menu === 'Open') {
                    setIsOpenBlocksModalOpen(true)
                  }
                  if (menu === 'Add Monkey Test Block') {
                    setIsAddMonkeyTestBlockModalOpen(true)
                  }
                  if (menu === 'Add Intelligent Monkey Test Block') {
                    setIsAddIntelligentMonkeyTestBlockModalOpen(true)
                  }
                }}
              >
                {menu}
              </OptionItem>
            ))}
          </DropdownWithMoreButton>
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
                    // test option modal 실행
                    setIsTesetOptionModalOpen(true)
                  }

                  return
                }

                setIsTesetOptionModalOpen(true)

                setIsPlay(true)
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
              { 'cusror-none bg-light-grey': isBlockRecordMode },
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
      {isTestOptionModalOpen && (
        <TestOptionModal
          isOpen={isTestOptionModalOpen}
          close={() => {
            setIsTesetOptionModalOpen(false)
            setIsPlay(false)
          }}
        />
      )}
    </>
  )
}

export default BlockControls

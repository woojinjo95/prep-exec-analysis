import React, { useEffect, useRef, useState } from 'react'
import classNames from 'classnames/bind'

// import { ReactComponent as AddIcon } from '@assets/images/add.svg'

import { KeyEvent } from '@page/ActionPage/types'

import { AppURL } from '@global/constant'
import { Button, OptionItem, DropdownWithMoreButton, Text, IconButton } from '@global/ui'
import { useHardwareConfiguration } from '@global/api/hook'
import { useWebsocket } from '@global/hook'
import { remoconService } from '@global/service/RemoconService/RemoconService'
import { CustomKeyTransmit, RemoconTransmit } from '@global/service/RemoconService/type'
import { ReactComponent as PlusIcon } from '@assets/images/add.svg'
import { useMutation, useQuery } from 'react-query'
import { customKeyDropdownMenu } from '@page/ActionPage/costants'
import { CustomKey, Remocon } from '../../api/entity'
import RemoconButtons from './RemoconButtons'
import styles from './RemoconComponent.module.scss'
import AddCustomKeyModal from '../AddCustomKeyModal'
import ModifyCustomKeyModal from '../ModifyCustomKeyModal'
import { deleteCustomKey, getRemocon } from '../../api/func'

const cx = classNames.bind(styles)

interface RemoconProps {
  remocon: Remocon
  keyEvent: KeyEvent | null
}

type RemoconResponseMessageDataBody = {
  key: string
  type: 'ir' | 'bt'
  press_time: number
  sensor_time: number
}

const RemoconComponent: React.FC<RemoconProps> = ({ remocon, keyEvent }) => {
  const remoconRef = useRef<HTMLImageElement | null>(null)
  const [isLoadedRemoconImage, setIsLoadedRemoconImage] = useState<boolean>(false)
  const [isAddCustomModalOpen, setIsAddCustomModalOpen] = useState<boolean>(false)
  const [isRendered, setIsRendered] = useState<boolean>(false)
  const [selectedCustomKey, setSelectedCustomKey] = useState<CustomKey | null>(null)

  const { hardwareConfiguration } = useHardwareConfiguration()
  const [clickedCustomKeyMessage, setClickedCustomKeyMessage] = useState<CustomKeyTransmit | null>(null)

  const [isModifyCustomKeyModalOpen, setIsModifyCustomKeyModalOpen] = useState<boolean>(false)

  const { sendMessage } = useWebsocket<RemoconResponseMessageDataBody>({
    onMessage: (message) => {
      if (!clickedCustomKeyMessage) return
      if (message.msg === 'remocon_response' && message.level === 'info') {
        // 커스텀 키 조합의 맨 마지막 신호가 왔다면
        if (message.data.key === clickedCustomKeyMessage.data[clickedCustomKeyMessage.data.length - 1].key) {
          remoconService.customKeyClick(clickedCustomKeyMessage)
          setClickedCustomKeyMessage(null)
        }
      }
    },
  })

  useEffect(() => {
    setIsRendered(true)
  }, [])

  useEffect(() => {
    // remocon의 name이 변경되면 (즉 다른 remocon을 선택했을 때)
    if (isRendered) {
      setIsLoadedRemoconImage(false)
    }
  }, [remocon.name, setIsRendered])

  const { refetch } = useQuery<Remocon[]>(['remocon'], () => getRemocon(), {
    onError: (err) => {
      console.error(err)
    },
  })

  const { mutate: deleteCustomKeyMutate } = useMutation(deleteCustomKey, {
    onSuccess: () => {
      refetch()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  if (!hardwareConfiguration) return <div />

  return (
    <>
      <div className="h-[calc(100%-62px)] grid grid-cols-2 grid-rows-1">
        <div className={cx('w-full h-full flex items-start overflow-y-auto relative', 'remocon-container')}>
          <img
            ref={remoconRef}
            onLoad={() => {
              setIsLoadedRemoconImage(true)
            }}
            src={`${AppURL.backendURL}${remocon.image_path}`}
            alt="remocon"
            className="w-full"
          />
          {isLoadedRemoconImage && <RemoconButtons keyEvent={keyEvent} remoconRef={remoconRef} remocon={remocon} />}
        </div>
        <div className="flex flex-col h-full pl-4">
          <div className="grid grid-rows-[1fr_8fr] overflow-y-auto">
            <div className="flex flex-row justify-between mt-[20px] items-center">
              <p className="font-medium text-[18px]">Custom Key</p>
              <IconButton
                className="w-11 h-8"
                onClick={() => {
                  setIsAddCustomModalOpen(true)
                }}
                icon={<PlusIcon />}
              />
            </div>
            <div className={cx('mt-[20px] overflow-y-auto w-full', 'hot-key-container')}>
              {remocon.custom_keys &&
                remocon.custom_keys.map((custom_key) => (
                  <Button
                    colorScheme="dark"
                    className="h-[40px] w-full border-[1px] border-[#707070] mb-[5px] flex justify-center !px-3"
                    key={`custom_keys_${custom_key.id}`}
                    onClick={() => {
                      const message: CustomKeyTransmit = {
                        msg: 'remocon_transmit',
                        data: custom_key.custom_code.map((code) => {
                          return {
                            key: code,
                            type: hardwareConfiguration.remote_control_type,
                            press_time: 0,
                            name: remocon.name,
                          }
                        }),
                      }
                      setClickedCustomKeyMessage(message)

                      custom_key.custom_code.forEach((code) => {
                        const message: RemoconTransmit = {
                          msg: 'remocon_transmit',
                          data: {
                            key: code,
                            type: hardwareConfiguration.remote_control_type,
                            press_time: 0,
                            name: remocon.name,
                          },
                        }

                        sendMessage(message)
                      })
                    }}
                  >
                    <div className="w-full flex justify-between">
                      <Text className="text-left w-[calc(100%-25px)] whitespace-nowrap overflow-hidden text-ellipsis">
                        {custom_key.name}
                      </Text>
                      <DropdownWithMoreButton colorScheme="light" type="icon" iconColorScheme="charcoal">
                        {customKeyDropdownMenu?.map((menu) => (
                          <OptionItem
                            colorScheme="light"
                            key={`${custom_key.id}_dropdown_menu_${menu}`}
                            onClick={() => {
                              if (menu === 'Modify') {
                                setSelectedCustomKey(custom_key)
                                setIsModifyCustomKeyModalOpen(true)
                              }

                              if (menu === 'Delete') {
                                deleteCustomKeyMutate({
                                  remocon_name: remocon.name,
                                  custom_key_ids: [custom_key.id],
                                })
                              }
                            }}
                          >
                            {menu}
                          </OptionItem>
                        ))}
                      </DropdownWithMoreButton>
                    </div>
                  </Button>
                ))}
            </div>
          </div>
        </div>
      </div>
      {isAddCustomModalOpen && (
        <AddCustomKeyModal
          isOpen={isAddCustomModalOpen}
          close={() => {
            setIsAddCustomModalOpen(false)
          }}
          remocon={remocon}
          keyEvent={keyEvent}
        />
      )}
      {isModifyCustomKeyModalOpen && selectedCustomKey && (
        <ModifyCustomKeyModal
          isOpen={isModifyCustomKeyModalOpen}
          close={() => {
            setIsModifyCustomKeyModalOpen(false)
          }}
          customKey={selectedCustomKey}
          remocon={remocon}
        />
      )}
    </>
  )
}

export default RemoconComponent

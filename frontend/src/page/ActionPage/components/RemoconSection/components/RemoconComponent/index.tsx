import React, { useEffect, useRef, useState } from 'react'
import classNames from 'classnames/bind'

// import { ReactComponent as AddIcon } from '@assets/images/add.svg'

import { KeyEvent } from '@page/ActionPage/types'

import AppURL from '@global/constant/appURL'
import DropdownWithMoreButton from '@global/ui/DropdownWithMoreButton'
import { Button, OptionItem } from '@global/ui'
import { useHardwareConfiguration } from '@global/api/hook'
import useWebsocket from '@global/module/websocket'
import { remoconService } from '@global/service/RemoconService/RemoconService'
import { CustomKeyTransmit, RemoconTransmit } from '@global/service/RemoconService/type'
import { Remocon } from '../../api/entity'
import RemoconButtons from './RemoconButtons'
import styles from './RemoconComponent.module.scss'
import AddCustomKeyModal from '../AddCustomKeyModal'

const cx = classNames.bind(styles)

interface RemoconProps {
  remocon: Remocon
  keyEvent: KeyEvent | null
}

const dropdownMenu = ['Add', 'Modify', 'Delete']

const RemoconComponent: React.FC<RemoconProps> = ({ remocon, keyEvent }) => {
  const remoconRef = useRef<HTMLImageElement | null>(null)
  const [isLoadedRemoconImage, setIsLoadedRemoconImage] = useState<boolean>(false)
  const [isAddCustomModalOpen, setIsAddCustomModalOpen] = useState<boolean>(false)
  const [isRendered, setIsRendered] = useState<boolean>(false)

  const { hardwareConfiguration } = useHardwareConfiguration()

  const { sendMessage } = useWebsocket()

  useEffect(() => {
    setIsRendered(true)
  }, [])

  useEffect(() => {
    // remocon의 name이 변경되면 (즉 다른 remocon을 선택했을 때)
    if (isRendered) {
      setIsLoadedRemoconImage(false)
    }
  }, [remocon.name, setIsRendered])

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
              <DropdownWithMoreButton>
                {dropdownMenu?.map((menu) => (
                  <OptionItem
                    colorScheme="light"
                    key={`menu_${menu}`}
                    onClick={() => {
                      if (menu === 'Add') {
                        setIsAddCustomModalOpen(true)
                      }
                    }}
                  >
                    {menu}
                  </OptionItem>
                ))}
              </DropdownWithMoreButton>
            </div>
            <div className={cx('mt-[20px] overflow-y-auto w-full', 'hot-key-container')}>
              {remocon.custom_keys &&
                remocon.custom_keys.map((custom_key) => (
                  <Button
                    colorScheme="dark"
                    className="h-[40px] w-full border-[1px] border-[#707070] mb-[5px] flex justify-center"
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
                      } as const
                      remoconService.customKeyClick(message)

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
                    {custom_key.name}
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
    </>
  )
}

export default RemoconComponent

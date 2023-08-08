import React, { useEffect, useRef, useState } from 'react'
import classNames from 'classnames/bind'

import { ReactComponent as MoreButton } from '@assets/images/button_more.svg'
// import { ReactComponent as AddIcon } from '@assets/images/add.svg'

import { KeyEvent } from '@page/ActionPage/types'

import { remoconService } from '@global/service/RemoconService'
import { Remocon } from '../../api/entity'
import RemoconButtons from './RemoconButtons'
import styles from './RemoconComponent.module.scss'
import AddCustomKeyModal from '../AddCustomKeyModal'

const cx = classNames.bind(styles)

const hotkeys = [
  '*7890#',
  '*7890#1',
  '*7890#2',
  '*7890#3',
  '*7890#4',
  '*7890#5',
  '*7890#6',
  '*7890#7',
  '*7890#8',
  '*7890#9',
  '*7890#10',
  '*7890#11',
  '*7890#12',
  '*7890#313',
  '*7890#14',
  '*7890#15',
  '*7890#16',
  '*7890#22',
  '*7890#23',
  '*7890#24',
  '*7890#35',
  '*7890#31',
  '*7890#32',
  '*7890#33',
  '*7890#34',
  '*7890#36',
]

interface RemoconProps {
  remocon: Remocon
  keyEvent: KeyEvent | null
}

const RemoconComponent: React.FC<RemoconProps> = ({ remocon, keyEvent }) => {
  const remoconRef = useRef<HTMLImageElement | null>(null)
  const [isLoadedRemoconImage, setIsLoadedRemoconImage] = useState<boolean>(false)
  const [isAddCustomModalOpen, setIsAddCustomModalOpen] = useState<boolean>(false)

  useEffect(() => {
    // remocon의 name이 변경되면 (즉 다른 remocon을 선택했을 때)
    setIsLoadedRemoconImage(false)
  }, [remocon.name])

  return (
    <>
      <div className="h-[calc(100%-30px)] grid grid-cols-2 grid-rows-1">
        <div className={cx('w-full h-full flex items-start overflow-y-auto relative', 'remocon-container')}>
          <img
            ref={remoconRef}
            onLoad={() => {
              setIsLoadedRemoconImage(true)
            }}
            src={`${
              import.meta.env.VITE_BACKEND_URL || `${window.location.protocol}//${window.location.hostname}:5000`
            }${remocon.image_path}`}
            alt="remocon"
            className="w-full"
          />
          {isLoadedRemoconImage && <RemoconButtons keyEvent={keyEvent} remoconRef={remoconRef} remocon={remocon} />}
        </div>
        <div className="flex flex-col h-full pl-4">
          <div className="grid grid-rows-[1fr_8fr] overflow-y-auto">
            <div className="flex flex-row justify-between mt-[20px] items-center">
              <p className="font-medium text-[18px]">Custom Key</p>
              <div
                className="flex flex-row justify-center items-center cursor-pointer bg-white w-[50px] border border-[#DFE0EE] h-full rounded-3xl"
                onClick={() => {
                  setIsAddCustomModalOpen(true)
                }}
              >
                <MoreButton className="w-[18px]" />
              </div>
            </div>
            <div className={cx('mt-[20px] overflow-y-auto w-full', 'hot-key-container')}>
              {remocon.custom_keys &&
                remocon.custom_keys.map((custom_key) => (
                  <button
                    type="button"
                    className="h-[32px] w-full bg-white border-[1px] border-[#707070] rounded-[38px] mb-[5px] font-[500] flex pl-[10px] hover:bg-gray-200"
                    key={`custom_keys_${custom_key.id}`}
                    onClick={() => {
                      remoconService.customKeyClick(custom_key.name)
                    }}
                  >
                    {custom_key.custom_code.join('')}
                  </button>
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

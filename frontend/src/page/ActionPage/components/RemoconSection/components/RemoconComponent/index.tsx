import React, { useRef, useState } from 'react'
import classNames from 'classnames/bind'

import { ReactComponent as EditIcon } from '@assets/images/edit.svg'
import { ReactComponent as AddIcon } from '@assets/images/add.svg'

import { KeyEvent } from '@page/ActionPage/types'
import { Remocon } from '../../api/entity'
import RemoconButtons from './RemoconButtons'
import styles from './RemoconComponent.module.scss'

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

  return (
    <div className="h-[calc(100%-30px)] grid grid-cols-2 grid-rows-1">
      <div className="w-full h-full flex items-center justify-center">
        <img
          ref={remoconRef}
          onLoad={() => {
            setIsLoadedRemoconImage(true)
          }}
          src={`${import.meta.env.VITE_BACKEND_URL || `${window.location.protocol}//${window.location.hostname}:5000`}${
            remocon.image_path
          }`}
          alt="remocon"
          className="h-full object-contain"
        />
        {isLoadedRemoconImage && <RemoconButtons keyEvent={keyEvent} remoconRef={remoconRef} remocon={remocon} />}
      </div>
      <div className="flex flex-col h-full">
        <div className="grid grid-rows-[1fr_8fr] overflow-y-auto">
          <div className="flex flex-row justify-between mt-[20px] items-center">
            <p className="font-medium text-[14px]">Custom Key</p>
            <div className="flex flex-row justify-between items-center">
              <AddIcon className="w-[14px] h-[14px]" />
              <EditIcon className="w-[14px] h-[14px] ml-[10px]" />
            </div>
          </div>
          <div className={cx('mt-[20px] overflow-y-auto w-full', 'hot-key-container')}>
            {remocon.custom_keys &&
              remocon.custom_keys.map((custom_keys) => (
                <button
                  type="button"
                  className="h-[32px] w-full bg-white border-[1px] border-[#707070] rounded-[38px] mb-[5px] font-[500] flex pl-[10px] hover:bg-gray-200"
                  key={`custom_keys_${custom_keys.custom_code.join('')}`}
                >
                  {custom_keys.custom_code.join('')}
                </button>
              ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default RemoconComponent

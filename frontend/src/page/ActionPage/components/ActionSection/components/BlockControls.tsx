import React from 'react'
import { ReactComponent as MoreIcon } from '@assets/images/button_more.svg'
import { ReactComponent as PlusIcon } from '@assets/images/icon_add.svg'
import { ReactComponent as RecordIcon } from '@assets/images/icon_record.svg'
import { ReactComponent as PlayIcon } from '@assets/images/icon_play.svg'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { ReactComponent as StopIcon } from '@assets/images/icon_stop.svg'

import classNames from 'classnames/bind'
import styles from '../css/BlockControls.module.scss'

const cx = classNames.bind(styles)

// FIXME: 모듈화!!!
const ws = new WebSocket(`ws://${window.location.hostname}:5000/api/v1/client/ws`)

const BlockControls: React.FC = () => {
  return (
    <div className="flex justify-between items-center pl-[10px] pr-[10px] border-t border-[#DFE0EE]">
      <div className="flex items-center">
        <div className="flex justify-center items-center border border-[#DFE0EE] h-[32px] w-[50px] rounded-3xl cursor-pointer">
          <MoreIcon className="h-[4px] w-[18px]" />
        </div>
        <div className="flex justify-center items-center border border-[#DFE0EE] h-[40px] w-[74px] rounded-[20px] ml-3 text-[14px] font-medium cursor-pointer">
          <p>Clear</p>
        </div>
      </div>
      <div className="flex items-center">
        <div className="flex justify-center items-center border border-[#D1D2DF] h-[40px] w-[52px] rounded-[20px] cursor-pointer">
          <PlusIcon className="h-[18px] w-[18px]" />
        </div>
        <div className="flex justify-center items-center ml-[4px] border border-[#D1D2DF] h-[40px] w-[52px] rounded-[20px] cursor-pointer">
          <StopIcon
            className={cx('record-icon', 'h-[16px] w-[16px]')}
            onClick={() => {
              ws.send('{"streaming": "stop"}')
            }}
          />
        </div>
        <div className="flex justify-center items-center ml-[4px] border border-[#D1D2DF] h-[40px] w-[52px] rounded-[20px] cursor-pointer">
          <RecordIcon className={cx('record-icon', 'h-[16px] w-[16px]')} />
        </div>
        <div className="flex justify-center items-center ml-[4px] border border-[#D1D2DF] h-[40px] w-[52px] rounded-[20px] cursor-pointer">
          <PlayIcon
            className="h-[16px] w-[18px]"
            onClick={() => {
              ws.send('{"streaming": "start"}')
            }}
          />
        </div>
        <div className="flex justify-center items-center ml-[4px] border border-[#D1D2DF] h-[40px] w-[52px] rounded-[20px] cursor-pointer">
          <TrashIcon className="h-[16px] w-[16px]" />
        </div>
      </div>
    </div>
  )
}

export default BlockControls

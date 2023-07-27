import React from 'react'
import { ReactComponent as PlayIcon } from '@assets/images/dropdown.svg'

const BlockControls = (): JSX.Element => {
  return (
    <div className="grid grid-cols-[1fr_2fr_1fr_1fr_1fr_1fr_1fr_1fr] items-center pl-[10px] pr-[10px]">
      <div
        className="flex justify-center items-center border-[1px] border-[#7777775E] h-[40px] w-[40px] rounded-full"
        style={{ boxShadow: '0px 1px 5px #7777775E' }}
      >
        <PlayIcon className="h-[15px]" />
      </div>
      <div
        className="flex justify-center items-center border-[1px] border-[#7777775E] h-[40px] w-[80px] rounded-full"
        style={{ boxShadow: '0px 1px 5px #7777775E' }}
      >
        <p>clear</p>
      </div>
      <div
        className="flex justify-center items-center border-[1px] border-[#7777775E] h-[40px] w-[40px] rounded-full"
        style={{ boxShadow: '0px 1px 5px #7777775E' }}
      >
        <PlayIcon className="h-[15px]" />
      </div>
      <div className="flex justify-center items-center">
        <PlayIcon className="h-[15px]" />
      </div>
      <div className="flex justify-center items-center">
        <PlayIcon className="h-[15px]" />
      </div>
      <div className="flex justify-center items-center">
        <PlayIcon className="h-[15px]" />
      </div>
      <div className="flex justify-center items-center">
        <PlayIcon className="h-[15px]" />
      </div>
      <div className="flex justify-center items-center">
        <PlayIcon className="h-[15px]" />
      </div>
    </div>
  )
}

export default BlockControls

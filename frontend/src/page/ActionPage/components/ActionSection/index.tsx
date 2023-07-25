import React from 'react'
import { ReactComponent as PlayIcon } from '@assets/images/dropdown.svg'
import ActionBlockArea from './components/ActionBlockArea'

/**
 * 액션 영역
 */
const ActionSection: React.FC = () => {
  return (
    <section className="border border-black row-span-2 p-[20px] h-full">
      <div className="grid grid-rows-[30px_auto_30px] gap-y-[10px] h-full">
        <div className="flex justify-end">
          <button
            type="button"
            className="flex flex-row justify-center items-center w-[100px] h-[32px] bg-white border-[1px] border-[#707070] rounded-[38px] mb-[5px] font-[500] hover:bg-gray-200"
          >
            <PlayIcon className="h-[10px] w-[10px] rotate-90" />
            <p className="text-[14px] ml-[10px]">Play</p>
          </button>
        </div>

        <ActionBlockArea />

        <div className="flex justify-between">
          <button
            type="button"
            className="flex flex-row justify-center items-center w-[100px] h-[32px] bg-black border-[1px] border-[#707070] rounded-[38px] mb-[5px] font-[500] hover:bg-gray-200"
          >
            <p className="text-[14px] text-white">Clear</p>
          </button>
          <button
            type="button"
            className="flex flex-row justify-center items-center w-[100px] h-[32px] bg-white border-[1px] border-[#707070] rounded-[38px] mb-[5px] font-[500] hover:bg-gray-200"
          >
            {/* TODO : RFC 빨간색 svg 필요 */}
            <PlayIcon className="h-[10px] w-[10px] rotate-90" />
            <p className="text-[14px] ml-[10px]">RFC</p>
          </button>
        </div>
      </div>
    </section>
  )
}

export default ActionSection

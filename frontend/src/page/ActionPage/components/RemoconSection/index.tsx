import React, { useEffect, useRef, useState } from 'react'
import Remocon from '@assets/images/btv_remote_control.png'

import { Menu, MenuButton, MenuList, MenuItem } from '@chakra-ui/react'

import { ReactComponent as DropdownIcon } from '@assets/images/dropdown.svg'
import { ReactComponent as EditIcon } from '@assets/images/edit.svg'
import { ReactComponent as AddIcon } from '@assets/images/add.svg'
import InformationIcon from '@assets/images/information.png'

import classNames from 'classnames/bind'

import { KeyEvent } from '@page/ActionPage/constants'
import styles from './RemoconSection.module.scss'
import ButtonSquares from './ButtonSquares/ButtonSquares'

const cx = classNames.bind(styles)

interface RemoconSectionProps {
  event: KeyEvent | null
}

/**
 * 리모컨 영역
 */
const RemoconSection: React.FC<RemoconSectionProps> = ({ event }) => {
  const remoconDivRef = useRef<HTMLDivElement>(null)

  const remoconRef = useRef<HTMLImageElement>(null)

  const [selectedRemocon, setSelectedRemocon] = useState<string | null>(null)

  const remocons = ['skb', 'kt', 'lg']

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

  useEffect(() => {
    setSelectedRemocon(remocons[0])
  }, [])

  const keyboardCoors: { leftTop: { left: number; top: number }; rightBottom: { right: number; bottom: number } }[] = [
    {
      leftTop: { left: 10, top: 10 },
      rightBottom: { right: 50, bottom: 50 },
    },
  ]

  return (
    <section className="border border-black h-full p-[20px]">
      <div className="flex flex-row justify-between w-full h-[30px] items-center">
        {selectedRemocon && remocons && (
          <Menu>
            <MenuButton className="w-[60%] flex justify-end">
              <div className="flex justify-between pr-[5px] pl-[5px] border-b-[1px] border-black">
                <p className="pl-[8px] font-medium text-[14px]">{selectedRemocon}</p>
                <DropdownIcon className="w-[10px] rotate-180" />
              </div>
            </MenuButton>
            <MenuList>
              {remocons.map((remocon) => {
                return (
                  <MenuItem
                    key={`remocon_${remocon}`}
                    onClick={() => {
                      setSelectedRemocon(remocon)
                    }}
                  >
                    {remocon}
                  </MenuItem>
                )
              })}
            </MenuList>
          </Menu>
        )}

        <img alt="information_icon" src={InformationIcon} className="w-[20px] h-[20px] cursor-pointer" />
      </div>

      <div className="h-[calc(100%-30px)] grid grid-cols-2 grid-rows-1">
        <div ref={remoconDivRef} className="h-full items-center justify-center">
          <ButtonSquares keyboardCoors={keyboardCoors} event={event} />
          <img ref={remoconRef} src={Remocon} alt="remocon" className="h-full object-contain" />
        </div>
        <div className="flex flex-col h-full">
          <div className="grid grid-rows-[1fr_8fr] overflow-y-auto">
            <div className="flex flex-row justify-between mt-[20px]">
              <p className="font-medium text-[14px]">Custom Key</p>
              <div className="flex flex-row justify-between items-center">
                <AddIcon className="w-[14px] h-[14px]" />
                <EditIcon className="w-[14px] h-[14px] ml-[10px]" />
              </div>
            </div>
            <div className={cx('flex flex-col mt-[20px] flex-grow overflow-y-auto', 'hot-key-container')}>
              {hotkeys.map((hotKey) => (
                <button
                  type="button"
                  className="h-[32px] bg-white border-[1px] border-[#707070] rounded-[38px] mb-[5px] font-[500] flex pl-[10px] hover:bg-gray-200"
                  key={`hotKey_${hotKey}`}
                >
                  {hotKey}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default RemoconSection

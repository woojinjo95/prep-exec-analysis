import React, { useEffect, useMemo, useRef, useState } from 'react'
import { Menu, MenuList, MenuItem } from '@chakra-ui/react'

// import RemoconImage from '@assets/images/btv_remote_control.png'
import { ReactComponent as EditIcon } from '@assets/images/edit.svg'
import { ReactComponent as AddIcon } from '@assets/images/add.svg'
import InformationIcon from '@assets/images/information.png'
import { DropdownButton } from '@global/ui'

import classNames from 'classnames/bind'

import { KeyEvent } from '@page/ActionPage/types'
import { useQuery } from 'react-query'
import styles from './RemoconSection.module.scss'
import ButtonSquares from './ButtonSquares/ButtonSquares'
import { Remocon } from './api/entity'
import { getRemocon } from './api/func'

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

interface RemoconSectionProps {
  keyEvent: KeyEvent | null
}

/**
 * 리모컨 영역
 */
const RemoconSection: React.FC<RemoconSectionProps> = ({ keyEvent }) => {
  const [selectedRemocon, setSelectedRemocon] = useState<Remocon | null>(null)

  const { data: remocons, isFetching } = useQuery<Remocon[]>(['remocon'], () => getRemocon(), {
    onSuccess: (res) => {
      if (res) {
        setSelectedRemocon(res[0])
      }
    },
    onError: (err) => {
      console.error(err)
    },
  })

  const remoconRef = useRef<HTMLImageElement>(null)

  const selectedKeyoardCoors = useMemo(() => {
    if (remocons && selectedRemocon) {
      return selectedRemocon.remocon_codes.map((remocon_code) => {
        return {
          leftTop: { left: remocon_code.coordinate[0], top: remocon_code.coordinate[1] },
          rightBottom: { right: remocon_code.coordinate[2], bottom: remocon_code.coordinate[3] },
        }
      })
    }

    return null
  }, [remocons, selectedRemocon])

  return (
    <section className="border border-black h-full p-[20px]">
      <div className="grid grid-rows-1 grid-cols-[1fr_auto] w-full h-[30px] items-center">
        {selectedRemocon && remocons && (
          <Menu>
            <DropdownButton className="w-[60%]">{selectedRemocon.name}</DropdownButton>
            <MenuList>
              {remocons.map((remocon) => {
                return (
                  <MenuItem
                    key={`remocon_${remocon.name}`}
                    onClick={() => {
                      setSelectedRemocon(remocon)
                    }}
                  >
                    {remocon.name}
                  </MenuItem>
                )
              })}
            </MenuList>
          </Menu>
        )}

        <img alt="information_icon" src={InformationIcon} className="w-[20px] h-[20px] cursor-pointer" />
      </div>

      {selectedRemocon && remocons && selectedKeyoardCoors && (
        <div className="h-[calc(100%-30px)] grid grid-cols-2 grid-rows-1">
          <div className="h-full items-center justify-center w-full flex">
            <img
              ref={remoconRef}
              src={`${
                import.meta.env.VITE_BACKEND_URL || `${window.location.protocol}//${window.location.hostname}:5000`
              }${selectedRemocon.image_path}`}
              alt="remocon"
              className="h-full object-contain"
            />
            <ButtonSquares
              keyboardCoors={selectedKeyoardCoors}
              keyEvent={keyEvent}
              imageRef={remoconRef}
              remoconResolution={selectedRemocon.image_resolution}
            />
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
                {hotkeys.map((hotKey) => (
                  <button
                    type="button"
                    className="h-[32px] w-full bg-white border-[1px] border-[#707070] rounded-[38px] mb-[5px] font-[500] flex pl-[10px] hover:bg-gray-200"
                    key={`hotKey_${hotKey}`}
                  >
                    {hotKey}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  )
}

export default RemoconSection

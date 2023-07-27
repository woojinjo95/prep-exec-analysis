import React, { useEffect, useRef, useState } from 'react'
import { ReactComponent as MenuIcon } from '@assets/images/menu.svg'
import cx from 'classnames'
import { ActionStatus, Block } from '../types'

interface ActionBlockItemProps {
  block: Block
  selectedBlockIds: number[]
  handleBlockClick: (event: React.MouseEvent<HTMLDivElement>, blockId: number) => void
  actionStatus: ActionStatus
  setModifyingBlockId: React.Dispatch<React.SetStateAction<number | null>>
  modifyingBlockId: number | null
}

const ActionBlockItem = ({
  block,
  selectedBlockIds,
  handleBlockClick,
  actionStatus,
  setModifyingBlockId,
  modifyingBlockId,
}: ActionBlockItemProps): JSX.Element => {
  const handleDragStart = (e: React.MouseEvent<HTMLDivElement>) => {
    // 부모 컴포넌트의 onMouseDown 이벤트 발생을 막기 위해서
    e.stopPropagation()
  }

  const [changedMin, setChangedMin] = useState<number>(0)

  const [changedSec, setChangedSec] = useState<number>(0)

  const itemRef = useRef<HTMLDivElement>(null)

  const handleOutsideClick = (e: MouseEvent): void => {
    if (!(modifyingBlockId && modifyingBlockId === block.id)) return

    if (!itemRef.current) {
      return
    }

    if (e.target instanceof Node && !itemRef.current.contains(e.target)) {
      setModifyingBlockId(null)
    }
  }

  useEffect(() => {
    if (modifyingBlockId && modifyingBlockId === block.id) {
      document.addEventListener('mousedown', handleOutsideClick)
    }

    return () => {
      document.removeEventListener('mousedown', handleOutsideClick)
    }
  }, [handleOutsideClick, modifyingBlockId])

  return (
    <div
      ref={itemRef}
      className={cx('relative w-full mb-[3px]', { 'z-20': modifyingBlockId && modifyingBlockId === block.id })}
      onClick={(e) => {
        if (!modifyingBlockId) {
          handleBlockClick(e, block.id)
        }
      }}
      id={`block-${block.id}`}
      onMouseDown={(e) => handleDragStart(e)}
    >
      <div
        className={cx(
          'border-box h-full w-full min-h-[35px] pl-[10px] pr-[10px] grid grid-cols-[1fr_minmax(100px,auto)] border-[1px] border-[#DFE0EE] bg-white rounded-[5px] whitespace-break-space outline-[#4C4E68]',
          {
            '!outline !outline-[1px]': selectedBlockIds.includes(block.id),
            '!border-[#FF433D] !outline-[#FF433D]': actionStatus === 'RFC',
            '!border-[#00B1FF] !outline-[#FF433D]': actionStatus === 'playing',
          },
        )}
      >
        <div
          className={cx('flex items-center border-[#DFE0EE] border-r-[1px] box-border', {
            '!border-r-[2px]': selectedBlockIds.includes(block.id),
            '!border-[#FF433D] border-r-[2px]': actionStatus === 'RFC',
            '!border-[#00B1FF] border-r-[2px]': actionStatus === 'playing',
          })}
        >
          <MenuIcon
            className="mr-[10px] cursor-pointer"
            onClick={(e) => {
              e.stopPropagation()

              setModifyingBlockId(block.id)
            }}
          />
          <div
            style={{
              msUserSelect: 'none',
              MozUserSelect: 'none',
              WebkitUserSelect: 'none',
              userSelect: 'none',
            }}
          >
            {block.title}
          </div>
        </div>
        <div className={cx('flex items-center justify-end')}>
          {modifyingBlockId && modifyingBlockId === block.id ? (
            <div className="flex pl-[10px] items-center">
              <p>Delay Time</p>
              <input
                type="number"
                className=" ml-[10px] bg-[#EBEBF2] text-right pr-[5px] w-[30px]"
                min={0}
                max={59}
                onChange={(e) => setChangedMin(Math.min(Number(e.target.value), 59))}
                value={changedMin}
              />
              <p> m</p>
              <input
                type="number"
                className=" ml-[10px] bg-[#EBEBF2] text-right pr-[5px] w-[30px]"
                min={0}
                max={59}
                onChange={(e) => setChangedSec(Math.min(Number(e.target.value), 59))}
                value={changedSec}
              />
              <p> m</p>
            </div>
          ) : (
            <div
              style={{
                msUserSelect: 'none',
                MozUserSelect: 'none',
                WebkitUserSelect: 'none',
                userSelect: 'none',
              }}
            >
              {block.time}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ActionBlockItem

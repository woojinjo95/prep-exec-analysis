import React, { useEffect, useRef, useState } from 'react'
import { ReactComponent as EditIcon } from '@assets/images/icon_edit.svg'
import cx from 'classnames'
import { Block } from '@page/ActionPage/components/ActionSection/api/entity'
import { changeMinSecMsToMs, changeMsToMinSecMs, formMsToHundred } from '@global/usecase'
import { useMutation } from 'react-query'
import { ActionStatus } from '../types'
import { putBlock } from '../api/func'

interface ActionBlockItemProps {
  block: Block
  selectedBlockIds: string[]
  handleBlockClick: (event: React.MouseEvent<HTMLDivElement>, blockId: string) => void
  actionStatus: ActionStatus
  setModifyingBlockId: React.Dispatch<React.SetStateAction<string | null>>
  modifyingBlockId: string | null
  blockRefetch: () => void
}

const ActionBlockItem = ({
  block,
  selectedBlockIds,
  handleBlockClick,
  actionStatus,
  setModifyingBlockId,
  modifyingBlockId,
  blockRefetch,
}: ActionBlockItemProps): JSX.Element => {
  const handleDragStart = (e: React.MouseEvent<HTMLDivElement>) => {
    // 부모 컴포넌트의 onMouseDown 이벤트 발생을 막기 위해서
    e.stopPropagation()
  }

  const [changedMin, setChangedMin] = useState<string>('')

  const [changedSec, setChangedSec] = useState<string>('')

  const [changedMSec, setChangedMSec] = useState<string>('')

  useEffect(() => {
    const minSecMillisec = changeMsToMinSecMs(block.delay_time)
    setChangedMin(String(minSecMillisec.m))
    setChangedSec(String(minSecMillisec.s))
    setChangedMSec(String(minSecMillisec.ms))
  }, [block])

  const { mutate: putScenarioMutate } = useMutation(putBlock, {
    onSuccess: () => {
      blockRefetch()
    },
    onError: () => {
      alert('블록 수정에 실패하였습니다')
    },
  })

  const itemRef = useRef<HTMLDivElement>(null)

  const handleOutsideClick = (e: MouseEvent): void => {
    if (!(modifyingBlockId && modifyingBlockId === block.id)) return

    if (!itemRef.current) {
      return
    }

    if (e.target instanceof Node && !itemRef.current.contains(e.target)) {
      putScenarioMutate({
        block_id: block.id,
        newBlock: {
          ...block,
          delay_time: changeMinSecMsToMs(Number(changedMin), Number(changedSec), Number(changedMSec)),
        },
      })
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
          `border-box h-full w-full min-h-[48px] pl-[10px] pr-[10px] grid grid-cols-[1fr_minmax(100px,auto)] border-[1px] border-[#DFE0EE] bg-white rounded-xl whitespace-break-space`,
          {
            'hover:outline-1 hover:outline-[#4C4E68] hover:outline': !selectedBlockIds.includes(block.id),
            '!outline !outline-[1px] !outline-[#4C4E68]': selectedBlockIds.includes(block.id),
            '!bg-[#F1F2F4]': selectedBlockIds.includes(block.id) && modifyingBlockId !== block.id,
            '!border-[#FF2300] !outline-[#FF2300]': actionStatus === 'RFC',
            '!border-[#00B1FF] !outline-[#00B1FF]': actionStatus === 'playing',
          },
        )}
      >
        <div
          className={cx('flex items-center border-[#DFE0EE] border-r-[1px] box-border', {
            'hover:border-r-2 hover:border-[4C4E68]': !selectedBlockIds.includes(block.id),
            '!border-r-[1px] !border-[#4C4E68]': selectedBlockIds.includes(block.id),
            '!border-[#FF2300] border-r-[2px]': actionStatus === 'RFC',
            '!border-[#00B1FF] border-r-[2px]': actionStatus === 'playing',
          })}
        >
          <div
            style={{
              msUserSelect: 'none',
              MozUserSelect: 'none',
              WebkitUserSelect: 'none',
              userSelect: 'none',
            }}
          >
            {block.type} : {block.value}
          </div>
        </div>
        <div className={cx('flex items-center justify-end overflow-x-hidden')}>
          {modifyingBlockId && modifyingBlockId === block.id ? (
            <div className="flex pl-[10px] items-center">
              <p>Delay Time</p>
              <input
                type="number"
                className=" ml-[10px] bg-[#F1F2F4] border-[1px] border-[#C2C3D5] text-right pr-[5px] w-[50px] h-[40px] rounded-xl"
                min={0}
                max={59}
                onChange={(e) => setChangedMin(String(Math.min(Number(e.target.value), 59)))}
                value={changedMin}
              />
              <p> m</p>
              <input
                type="number"
                className=" ml-[10px] bg-[#F1F2F4] border-[1px] border-[#C2C3D5] text-right pr-[5px] w-[50px] h-[40px] rounded-xl"
                min={0}
                max={59}
                onChange={(e) => setChangedSec(String(Math.min(Number(e.target.value), 59)))}
                value={changedSec}
              />
              <p> s</p>
              <input
                type="number"
                className=" ml-[10px] bg-[#F1F2F4] border-[1px] border-[#C2C3D5] text-right pr-[5px] w-[50px] h-[40px] rounded-xl"
                min={0}
                max={900}
                onChange={(e) => {
                  setChangedMSec(String(formMsToHundred(Number(e.target.value))))
                }}
                value={changedMSec}
              />
              <p> ms</p>
            </div>
          ) : (
            <>
              <div
                style={{
                  msUserSelect: 'none',
                  MozUserSelect: 'none',
                  WebkitUserSelect: 'none',
                  userSelect: 'none',
                }}
              >
                {block.delay_time}
              </div>
              <EditIcon
                className="cursor-pointer ml-[10px] h-4 w-4"
                onClick={(e) => {
                  e.stopPropagation()

                  setModifyingBlockId(block.id)
                }}
              />
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default ActionBlockItem

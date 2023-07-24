import React from 'react'
import { ReactComponent as TrashIcon } from '@assets/images/trash.svg'
import cx from 'classnames'
import { ActionStatus, Block } from '../types'

interface ActionBlockItemProps {
  block: Block
  selectedBlockIds: number[]
  handleBlockClick: (event: React.MouseEvent<HTMLDivElement>, blockId: number) => void
  actionStatus: ActionStatus
}

const ActionBlockItem = ({
  block,
  selectedBlockIds,
  handleBlockClick,
  actionStatus,
}: ActionBlockItemProps): JSX.Element => {
  const handleDragStart = (event: React.MouseEvent<HTMLDivElement>) => {
    // 부모 컴포넌트의 onMouseDown 이벤트 발생을 막기 위해서
    event.stopPropagation()
  }
  return (
    <div
      className="w-full h-[35px] mb-[2px] justify-center items-center"
      onClick={(event) => handleBlockClick(event, block.id)}
      id={`block-${block.id}`}
      onMouseDown={handleDragStart}
    >
      <div
        className={cx('h-full w-full p-[5px] flex items-center border-[1px] bg-white justify-between  rounded-[5px]', {
          'bg-blue-200': selectedBlockIds.includes(block.id),
          'border-red-400': actionStatus === 'RFC',
          'border-blue-400': actionStatus === 'playing',
          'border-gray-400': actionStatus === 'normal',
        })}
      >
        <p
          style={{
            msUserSelect: 'none',
            MozUserSelect: 'none',
            WebkitUserSelect: 'none',
            userSelect: 'none',
          }}
        >
          {block.time} {block.title}
        </p>
        {actionStatus === 'normal' && <TrashIcon className="stroke-current text-black" />}
      </div>
    </div>
  )
}

export default ActionBlockItem

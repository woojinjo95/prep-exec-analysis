import React, { useEffect, useRef, useState } from 'react'
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd'
import cx from 'classnames'
import { formatDateTo } from '@global/usecase'
import ActionBlockItem from './ActionBlockItem'
import { Block } from '../types'

const blockData: Block[] = Array.from({ length: 15 }, (_, i) => ({
  id: i,
  title: `block ${i}`,
  time: formatDateTo('HH:MM:SS', new Date()),
  refIdx: i,
}))

const ActionBlockArea = (): JSX.Element => {
  // 전체 블럭
  const [blocks, setBlocks] = useState<Block[]>(blockData)

  // 선택된 블럭 id list
  const [selectedBlockIds, setSelectedBlockIds] = useState<number[]>([])

  const blocksRef = useRef<HTMLDivElement[] | null[]>(new Array(blocks.length))

  /**
   * 실제로 렌더링 때 사용될 blockDummys
   * 하나의 블럭 = 하나의 블럭 Dummy
   * 연속된 블럭 모음 = 하나의 블럭 Dummy
   */
  const [blockDummys, setBlockDummys] = useState<Block[][]>([])

  /**
   * onDragEnd handler (block용)
   */
  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return

    const { source, destination } = result
    // drag를 시작한 블록의 index
    const sourceIndex = source.index
    // drag를 놓은 위치의 index
    const destinationIndex = destination.index

    if (sourceIndex === destinationIndex) return

    const updatedBlockDummys: Block[][] = Array.from(blockDummys)

    // sourceIndex 위치의 블록을 제거하고 removed에 저장해두기
    const [removed] = updatedBlockDummys.splice(sourceIndex, 1)

    // 목적 index에 removed를 삽입
    updatedBlockDummys.splice(destinationIndex, 0, removed)
    setBlockDummys(updatedBlockDummys)

    // 전체 blocks 최신화
    setBlocks(updatedBlockDummys.flat())
  }

  /**
   * block onClick handler
   * @param blockId 클릭한 block id
   */
  const handleBlockClick = (event: React.MouseEvent<HTMLDivElement>, blockId: number) => {
    const { ctrlKey, shiftKey } = event

    if (ctrlKey) {
      // ctrlKey가 눌렸을 때 개별 선택
      setSelectedBlockIds((prev) => (prev.includes(blockId) ? prev.filter((id) => id !== blockId) : [...prev, blockId]))
    } else if (shiftKey && selectedBlockIds.length > 0) {
      // shiftKey가 눌렸을 때 (시작점이 필요하기 때문에 선택된 블럭이 하나 이상 있어야 함)

      // 맨 마지막에 선택된 block이 기준이 됨
      const lastSelectedBlockId = selectedBlockIds[selectedBlockIds.length - 1]
      const start = blocks.findIndex((block) => block.id === lastSelectedBlockId)
      // 클릭한 block까지
      const end = blocks.findIndex((block) => block.id === blockId)

      // min 부터 max 까지
      const selectedBlocks = blocks.slice(Math.min(start, end), Math.max(start, end) + 1).map((block) => block.id)
      setSelectedBlockIds(selectedBlocks)
    } else {
      // 단일 건 클릭 선택
      setSelectedBlockIds([blockId])
    }
  }

  // 연속된 block을 하나의 blockDummy로 묶기 위한 useEffect
  useEffect(() => {
    const blockIndexs: number[] = selectedBlockIds
      .map((id) => blocks.findIndex((block_id) => block_id.id === id))
      .filter((idx) => idx !== -1)

    // 선택된 블록들의 sorted index list
    const sortedBlockIdxs = blockIndexs.sort((a, b) => a - b)

    if (sortedBlockIdxs.length > 1) {
      // 연속성 체크
      let checkContinuous = true

      for (let i = 0; i < sortedBlockIdxs.length - 1; i += 1) {
        if (Math.abs(sortedBlockIdxs[i + 1] - sortedBlockIdxs[i]) !== 1) {
          checkContinuous = false
          break
        }
      }

      // 연속인 블럭의 경우
      if (checkContinuous) {
        const tempDummyBlocks = []

        for (let i = 0; i < blocks.length; i += 1) {
          if (i >= sortedBlockIdxs[0] && i <= sortedBlockIdxs[sortedBlockIdxs.length - 1]) {
            if (i === sortedBlockIdxs[0]) {
              tempDummyBlocks.push(sortedBlockIdxs.map((idx) => blocks[idx]))
            }
          } else {
            tempDummyBlocks.push([blocks[i]])
          }
        }

        setBlockDummys(tempDummyBlocks)
      } else {
        setBlockDummys(blocks.map((block) => [block]))
      }
    } else {
      setBlockDummys(blocks.map((block) => [block]))
    }
  }, [selectedBlockIds, blocks])

  // 드래그 영역을 표시하기 위한 상태와 시작 지점
  const [dragSelection, setDragSelection] = useState<{
    startX: number
    startY: number
    endX: number
    endY: number
  } | null>(null)

  // 드래그 영역 계산 및 업데이트 함수
  const handleMouseDown = (event: React.MouseEvent<HTMLDivElement>) => {
    const x = event.clientX
    const y = event.clientY
    setDragSelection({ startX: x, startY: y, endX: x, endY: y })
    // setStartPosition({ x, y })
    setSelectedBlockIds([])
  }

  // 드래그 후 마우스를 땠을 때
  const handleMouseUp = () => {
    if (dragSelection) {
      const { startX, startY, endX, endY } = dragSelection
      const minX = Math.min(startX, endX)
      const minY = Math.min(startY, endY)
      const maxX = Math.max(startX, endX)
      const maxY = Math.max(startY, endY)

      // 드래그 영역 안에 있는 블록들을 선택
      const selectedIds: number[] = blocks
        .filter((block) => {
          if (!blocksRef.current[block.refIdx]) return false

          const blockRect = blocksRef.current[block.refIdx]!.getBoundingClientRect()
          const blockX = blockRect.left + blockRect.width / 2
          const blockY = blockRect.top + blockRect.height / 2

          return blockX >= minX && blockX <= maxX && blockY >= minY && blockY <= maxY
        })
        .map((block) => block.id)

      setSelectedBlockIds(selectedIds)
      setDragSelection(null)
    }
  }

  // 드래그 중일 때
  const handleMouseMove = (event: React.MouseEvent<HTMLDivElement>) => {
    if (dragSelection) {
      const x = event.clientX
      const y = event.clientY

      if (dragSelection) {
        setDragSelection((prevState) => ({
          ...prevState!,
          endX: x,
          endY: y,
        }))

        const { startX, startY, endX, endY } = dragSelection
        const minX = Math.min(startX, endX)
        const minY = Math.min(startY, endY)
        const maxX = Math.max(startX, endX)
        const maxY = Math.max(startY, endY)

        // 드래그 영역에 속하는 블럭들의 id
        const selectedIds: number[] = blocks
          .filter((block) => {
            if (!blocksRef.current[block.refIdx]) return false

            const blockRect = blocksRef.current[block.refIdx]!.getBoundingClientRect()
            const blockX = blockRect.left + blockRect.width / 2
            const blockY = blockRect.top + blockRect.height / 2

            return blockX >= minX && blockX <= maxX && blockY >= minY && blockY <= maxY
          })
          .map((block) => block.id)

        setSelectedBlockIds(selectedIds)
      }
    }
  }

  return (
    <div
      className="h-full w-full"
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onMouseMove={handleMouseMove}
    >
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="droppable">
          {(provided) => (
            <div ref={provided.innerRef} {...provided.droppableProps} className="flex flex-col">
              {blockDummys.map((dummy, dummyIdx) => {
                return (
                  <Draggable key={dummyIdx} draggableId={`dummy-${dummyIdx}`} index={dummyIdx}>
                    {(provided) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        className={cx('w-full cursor-grab ', {})}
                      >
                        {dummy.map((block) => {
                          return (
                            <div
                              key={block.id}
                              ref={(ele) => {
                                blocksRef.current[block.refIdx] = ele
                              }}
                            >
                              <ActionBlockItem
                                actionStatus="normal"
                                block={block}
                                selectedBlockIds={selectedBlockIds}
                                handleBlockClick={handleBlockClick}
                              />
                            </div>
                          )
                        })}
                      </div>
                    )}
                  </Draggable>
                )
              })}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>

      {dragSelection && (
        <div
          className="absolute border border-blue-500 bg-blue-200 opacity-50"
          style={{
            top: Math.min(dragSelection.startY, dragSelection.endY),
            left: Math.min(dragSelection.startX, dragSelection.endX),
            width: Math.abs(dragSelection.endX - dragSelection.startX),
            height: Math.abs(dragSelection.endY - dragSelection.startY),
          }}
        />
      )}
    </div>
  )
}

export default ActionBlockArea

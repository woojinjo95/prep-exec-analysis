import React, { useEffect, useRef, useState } from 'react'
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd'
import cx from 'classnames'

import { Block, BlockGroup, Scenario } from '@page/ActionPage/components/ActionSection/api/entity'
import { useMutation, useQuery } from 'react-query'
import BackgroundImage from '@assets/images/background_pattern.svg'
import ActionBlockItem from './ActionBlockItem'
import BlockControls from './BlockControls'
import { getScenario, putScenario } from '../api/func'

type BlocksRef = {
  [id: string]: HTMLDivElement | null
}

const ActionBlockArea = (): JSX.Element => {
  // 전체 블럭
  const [blocks, setBlocks] = useState<Block[] | null>(null)

  /**
   * 실제로 렌더링 때 사용될 blockDummys
   * 하나의 블럭 = 하나의 블럭 Dummy
   * 연속된 블럭 모음 = 하나의 블럭 Dummy
   */
  const [blockDummys, setBlockDummys] = useState<Block[][]>([])

  const { data: scenario, refetch: blockRefetch } = useQuery<Scenario>(['scenario'], () => getScenario(), {
    onSuccess: (res) => {
      if (res && res.items.block_group.length > 0) {
        const newBlocks: Block[] = res.items.block_group[0].block
        setBlocks(newBlocks)
        setBlockDummys(newBlocks.map((block) => [block]))
      }
    },
  })

  const { mutate: putScenarioMutate } = useMutation(putScenario, {
    onSuccess: () => {
      blockRefetch()
    },
    onError: () => {
      alert('시나리오 수정에 실패하였습니다')
    },
  })

  // 선택된 블럭 id list
  const [selectedBlockIds, setSelectedBlockIds] = useState<string[]>([])

  const blocksRef = useRef<BlocksRef>({})

  const [modifyingBlockId, setModifyingBlockId] = useState<string | null>(null)

  /**
   * onDragEnd handler (block용)
   */
  const handleDragEnd = (result: DropResult) => {
    if (!scenario) return

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

    const newBlockGroup: BlockGroup = { ...scenario.items.block_group[0], block: updatedBlockDummys.flat() }

    putScenarioMutate({
      block_group: [newBlockGroup],
    })
  }

  /**
   * block onClick handler
   * @param blockId 클릭한 block id
   */
  const handleBlockClick = (event: React.MouseEvent<HTMLDivElement>, blockId: string) => {
    if (!blocks) return

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
    if (blocks) {
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
    if (dragSelection && blocks) {
      const { startX, startY, endX, endY } = dragSelection
      const minX = Math.min(startX, endX)
      const minY = Math.min(startY, endY)
      const maxX = Math.max(startX, endX)
      const maxY = Math.max(startY, endY)

      // 드래그 영역에 속하는 블럭들의 id
      const selectedIds: string[] = blocks
        .filter((block) => {
          if (!blocksRef.current[block.id]) return false

          const blockRect = blocksRef.current[block.id]!.getBoundingClientRect()
          const blockY = blockRect.top + blockRect.height / 2

          return (
            blockY >= minY &&
            blockY <= maxY &&
            ((minX <= blockRect.left && maxX >= blockRect.left) ||
              (maxX >= blockRect.right && minX <= blockRect.right) ||
              (minX >= blockRect.left && maxX <= blockRect.right))
          )
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

      if (dragSelection && blocks) {
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
        const selectedIds: string[] = blocks
          .filter((block) => {
            if (!blocksRef.current[block.id]) return false

            const blockRect = blocksRef.current[block.id]!.getBoundingClientRect()
            const blockY = blockRect.top + blockRect.height / 2

            return (
              blockY >= minY &&
              blockY <= maxY &&
              ((minX <= blockRect.left && maxX >= blockRect.left) ||
                (maxX >= blockRect.right && minX <= blockRect.right) ||
                (minX >= blockRect.left && maxX <= blockRect.right))
            )
          })
          .map((block) => block.id)

        setSelectedBlockIds(selectedIds)
      }
    }
  }

  return (
    <div className="h-full w-full">
      <div className="grid grid-rows-[auto_56px] h-full">
        <div
          className="h-full w-full pt-[30px] overflow-y-auto bg-repeat-y"
          onMouseDown={handleMouseDown}
          onMouseUp={handleMouseUp}
          onMouseMove={handleMouseMove}
          style={{
            backgroundImage: `url(${BackgroundImage})`,
            backgroundSize: '100%',
          }}
        >
          {blocks && blockDummys && blocks.length > 0 && (
            <div className="w-full h-full pl-[30px] pr-[30px] overflow-y-auto pt-[2px] pb-[2px]">
              <DragDropContext onDragEnd={handleDragEnd}>
                <Droppable droppableId="droppable">
                  {(provided) => (
                    <div ref={provided.innerRef} {...provided.droppableProps} className="flex flex-col">
                      {blockDummys.map((dummy, dummyIdx) => {
                        return (
                          <Draggable
                            key={dummyIdx}
                            draggableId={`dummy-${dummyIdx}`}
                            index={dummyIdx}
                            isDragDisabled={
                              !!(modifyingBlockId && dummy.find((block) => block.id === modifyingBlockId))
                            }
                          >
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
                                        blocksRef.current[block.id] = ele
                                      }}
                                    >
                                      <ActionBlockItem
                                        actionStatus="normal"
                                        block={block}
                                        selectedBlockIds={selectedBlockIds}
                                        handleBlockClick={handleBlockClick}
                                        setModifyingBlockId={setModifyingBlockId}
                                        modifyingBlockId={modifyingBlockId}
                                        blockRefetch={() => {
                                          blockRefetch()
                                        }}
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
            </div>
          )}

          {blocks && blockDummys && blocks.length === 0 && (
            <div className="h-full w-full justify-center items-center">
              <p className="text-xl">No Blocks</p>
              <p className="text-base">Start action about device control and adb/ssh access</p>
            </div>
          )}

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
        <BlockControls />
      </div>
      {modifyingBlockId && <div className="absolute top-0 left-0 h-full z-10 w-full bg-gray-100 opacity-50" />}
    </div>
  )
}

export default ActionBlockArea

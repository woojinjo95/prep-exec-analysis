import React, { useMemo, useRef, useState } from 'react'
import cx from 'classnames'
import { createPortal } from 'react-dom'
import { DragDropContext, Draggable, Droppable, OnDragEndResponder } from 'react-beautiful-dnd'
import { SimpleButton, Text } from '@global/ui'
import { ReactComponent as SettingIcon } from '@assets/images/setting.svg'
import { ReactComponent as DragIcon } from '@assets/images/drag.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { useOutsideClick } from '@global/hook'
import { createPortalStyle } from '@global/usecase'
import { ChartLabel } from '../../constant'

const SHOWN_DROPPABLE_ID = 'chart-filter-shown-column'
const HIDDEN_DROPPABLE_ID = 'chart-filter-hidden-column'
const ITEM_HEIGHT = 34

interface FilterButtonProps {
  activeChartList: (keyof typeof ChartLabel)[]
  setActiveChartList: React.Dispatch<React.SetStateAction<(keyof typeof ChartLabel)[]>>
  allChartList: (keyof typeof ChartLabel)[]
  setAllChartList: React.Dispatch<React.SetStateAction<(keyof typeof ChartLabel)[]>>
}

/**
 * 차트의 순서변경 및 숨기기/보기 기능을 사용할 수 있는 필터 버튼
 */
const FilterButton: React.FC<FilterButtonProps> = ({
  activeChartList,
  setActiveChartList,
  allChartList,
  setAllChartList,
}) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const [isOpenFilter, setIsOpenFilter] = useState<boolean>(false)
  const { ref } = useOutsideClick<HTMLDivElement>({
    mode: 'position',
    onClickOutside: () => {
      setIsOpenFilter(false)
    },
  })
  const shownChartList = useMemo(
    () => allChartList.filter((key) => activeChartList.includes(key)),
    [allChartList, activeChartList],
  )
  const hiddenChartList = useMemo(
    () => allChartList.filter((key) => !activeChartList.includes(key)),
    [allChartList, activeChartList],
  )

  const onDragEnd: OnDragEndResponder = (result) => {
    if (!result.destination) return
    if (result.source.index === result.destination.index) return

    // 보기 리스트에서 숨기기 리스트로 이동했을 경우
    if (result.source.droppableId === SHOWN_DROPPABLE_ID && result.destination.droppableId === HIDDEN_DROPPABLE_ID) {
      setActiveChartList((prev) => prev.filter((key) => key !== allChartList[result.source.index]))
    }

    // 숨기기 리스트에서 보기 리스트로 이동했을 경우
    if (result.source.droppableId === HIDDEN_DROPPABLE_ID && result.destination.droppableId === SHOWN_DROPPABLE_ID) {
      const newActiveChartList = [...activeChartList]
      newActiveChartList.splice(result.destination.index, 0, allChartList[result.source.index])
      setActiveChartList(newActiveChartList)
    }

    const newAllChartList = [...allChartList]
    const [removed] = newAllChartList.splice(result.source.index, 1)
    newAllChartList.splice(result.destination.index, 0, removed)

    setAllChartList(newAllChartList)
  }

  return (
    <div ref={wrapperRef} className="relative">
      <button
        type="button"
        className="h-full w-48 bg-charcoal border-b-[1px] border-light-charcoal px-5 flex items-center justify-between transition-all hover:brightness-125 active:brightness-95"
        onClick={() => setIsOpenFilter((prev) => !prev)}
      >
        <Text colorScheme="light" weight="medium">
          Filter
        </Text>
        <SettingIcon className="w-4 h-4 fill-white" />
      </button>

      {isOpenFilter &&
        createPortal(
          <div
            ref={ref}
            style={createPortalStyle({ wrapperRef, spaceX: 8, spaceY: 4 })}
            className="fixed z-20 bg-light-black border border-light-charcoal rounded-lg pb-4 pt-3 h-fit"
            onClick={(e) => e.stopPropagation()}
          >
            <DragDropContext onDragEnd={onDragEnd}>
              {!!shownChartList.length && (
                <div className="px-4 flex items-center justify-between">
                  <Text size="xs" weight="medium" colorScheme="grey">
                    Shown in board
                  </Text>
                  <SimpleButton colorScheme="primary" onClick={() => setActiveChartList([])}>
                    <Text colorScheme="primary" weight="medium" size="xs">
                      Hide all
                    </Text>
                  </SimpleButton>
                </div>
              )}

              <Droppable droppableId={SHOWN_DROPPABLE_ID}>
                {(_provided) => (
                  <div
                    ref={_provided.innerRef}
                    {..._provided.droppableProps}
                    style={{
                      height: (shownChartList.length ? shownChartList.length + 1 : 0) * ITEM_HEIGHT,
                    }}
                  >
                    {shownChartList.map((key, index) => (
                      <Draggable key={`chart-filter-${key}`} index={index} draggableId={`chart-filter-${key}`}>
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={cx(
                              'select-none px-4 py-1 hover:bg-light-charcoal flex justify-between items-center',
                              {
                                'bg-light-charcoal': snapshot.isDragging,
                              },
                            )}
                          >
                            <div className="flex items-center gap-x-3 mr-4">
                              <DragIcon className="w-4 h-4 fill-white" />
                              <Text colorScheme="light" weight="medium">
                                {ChartLabel[key]}
                              </Text>
                            </div>

                            <SimpleButton
                              isIcon
                              colorScheme="grey"
                              onClick={() => {
                                setActiveChartList((prev) => prev.filter((_key) => _key !== key))
                                setAllChartList((prev) => [...prev.filter((_key) => _key !== key), key])
                              }}
                            >
                              <ShowEyeIcon className="h-2.5 w-3.5" />
                            </SimpleButton>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {_provided.placeholder}
                  </div>
                )}
              </Droppable>

              {!!hiddenChartList.length && (
                <div className="px-4 flex items-center justify-between">
                  <Text size="xs" weight="medium" colorScheme="grey">
                    Hidden in board
                  </Text>
                  <SimpleButton colorScheme="primary" onClick={() => setActiveChartList([...allChartList])}>
                    <Text colorScheme="primary" weight="medium" size="xs">
                      Show all
                    </Text>
                  </SimpleButton>
                </div>
              )}

              <Droppable droppableId={HIDDEN_DROPPABLE_ID}>
                {(_provided) => (
                  <div
                    ref={_provided.innerRef}
                    {..._provided.droppableProps}
                    style={{
                      height: (hiddenChartList.length ? hiddenChartList.length + 1 : 0) * ITEM_HEIGHT,
                    }}
                  >
                    {hiddenChartList.map((key, index) => (
                      <Draggable
                        key={`chart-filter-${key}`}
                        index={index + shownChartList.length}
                        draggableId={`chart-filter-${key}`}
                      >
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={cx(
                              'select-none px-4 py-1 hover:bg-light-charcoal flex justify-between items-center',
                              {
                                'bg-light-charcoal': snapshot.isDragging,
                              },
                            )}
                          >
                            <div className="flex items-center gap-x-3 mr-4">
                              <DragIcon className="w-4 h-4 fill-grey" />
                              <Text colorScheme="grey" weight="medium">
                                {ChartLabel[key]}
                              </Text>
                            </div>

                            <SimpleButton
                              isIcon
                              colorScheme="grey"
                              onClick={() => {
                                setActiveChartList((prev) => [...prev, key])
                                setAllChartList((prev) => [
                                  ...prev.filter((_key) => activeChartList.includes(_key)),
                                  key,
                                  ...prev.filter((_key) => !activeChartList.includes(_key) && _key !== key),
                                ])
                              }}
                            >
                              <HiddenEyeIcon className="h-2.5 w-3.5" />
                            </SimpleButton>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {_provided.placeholder}
                  </div>
                )}
              </Droppable>
            </DragDropContext>
          </div>,
          document.body,
        )}
    </div>
  )
}

export default React.memo(FilterButton)

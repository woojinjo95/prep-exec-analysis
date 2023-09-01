import { PAGE_SIZE_TWENTY } from '@global/constant'
import useFetchScenarios from '@global/hook/useFetchScenarios'
import useIntersect from '@global/hook/useIntersect'
import { Button, Modal, Text } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import React, { useEffect, useMemo, useRef, useState } from 'react'
import { Scrollbars } from 'react-custom-scrollbars-2'
import cx from 'classnames'
import { useRecoilState } from 'recoil'
import { scenarioIdState } from '@global/atom'
import { useNavigate } from 'react-router-dom'

interface OpenBlocksModalProps {
  isOpen: boolean
  close: () => void
}

const OpenBlocksModal: React.FC<OpenBlocksModalProps> = ({ isOpen, close }) => {
  const { data, hasNextPage, isFetching, fetchNextPage } = useFetchScenarios(PAGE_SIZE_TWENTY)

  const scenarios = useMemo(() => {
    return data ? data.pages.flatMap(({ items }) => items) : []
  }, [data])

  const ref = useIntersect((entry, observer) => {
    // 발견시 실행될 callback
    observer.unobserve(entry.target)

    if (hasNextPage && !isFetching) {
      // 다음 페이지가 존재하고 isFetching이 아니라면
      fetchNextPage()
    }
  })

  const firstFocusableElementRef = useRef<HTMLButtonElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Tab') {
        // shift : 역으로 이동
        if (event.shiftKey) {
          if (document.activeElement === firstFocusableElementRef.current) {
            event.preventDefault()
            lastFocusableElementRef.current?.focus()
          }
        } else if (document.activeElement === lastFocusableElementRef.current) {
          event.preventDefault()
          firstFocusableElementRef.current?.focus()
        }
      }
    }

    firstFocusableElementRef.current?.focus()

    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null)

  const [, setScenarioId] = useRecoilState(scenarioIdState)

  const navigate = useNavigate()

  return (
    <Modal
      isOpen={isOpen}
      close={() => {
        close()
      }}
      title="Open Blocks"
    >
      <div className="h-[745px] w-[1140px] flex flex-col justify-between">
        <div className="flex flex-col w-full min-h-[620px]">
          <div className="w-[calc(100%-16px)] grid grid-cols-[35%_45%_20%] gap-x-2 min-h-[48px] items-end border-b-grey border-b-[1px] pb-2">
            <Text className="text-sm" colorScheme="grey">
              Name
            </Text>
            <Text className="text-sm" colorScheme="grey">
              Tag
            </Text>
            <Text className="text-sm" colorScheme="grey">
              Last modified
            </Text>
          </div>
          <Scrollbars
            renderThumbVertical={({ ...props }) => (
              <div {...props} className="w-2 rounded-[5px] pr-2 bg-light-charcoal" />
            )}
          >
            {scenarios.map((scenario) => (
              <div
                className={cx('flex flex-col w-full cursor-pointer', {
                  'bg-grey': selectedScenarioId && selectedScenarioId === scenario.id,
                })}
                key={`file_${scenario.name}`}
                onClick={() => {
                  setSelectedScenarioId(scenario.id)
                }}
              >
                <div className="w-[calc(100%-16px)] grid grid-cols-[35%_45%_20%]  gap-x-2 border-b-grey border-b-[1px] min-h-[48px] items-center">
                  <div>
                    <Text className="text-white mr-3" invertBackground colorScheme="light-orange">
                      B
                    </Text>
                    <Text size="md" colorScheme="light">
                      {scenario.name}
                    </Text>
                  </div>

                  <div className="flex flex-wrap w-full h-full pt-[10px] items-center">
                    {scenario.tags.map((tag) => (
                      <Text
                        className="text-white mr-2 mb-2"
                        invertBackground
                        colorScheme="dark-grey"
                        key={`${scenario.name}_tag_${tag}`}
                      >
                        {tag}
                      </Text>
                    ))}
                  </div>
                  <Text size="md" colorScheme="light">
                    {formatDateTo('M DD YYYY, HH:MM AA', new Date(scenario.updated_at))}
                  </Text>
                </div>
              </div>
            ))}
            {/* Intersect Target */}
            <div
              className="min-h-[48px] border-b-grey border-b-[1px]"
              ref={ref}
              style={{ display: !hasNextPage ? 'none' : '' }}
            >
              {/* Loading spin 같은 로딩 UI가 필요 */}
              Loading...
            </div>
          </Scrollbars>
        </div>
        <div className="flex justify-end mt-7">
          <Button
            ref={firstFocusableElementRef}
            colorScheme="primary"
            className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
            onClick={() => {
              setScenarioId(selectedScenarioId)
              // 새로고침하지 않고 강제로 이동하게 해야 함
              navigate('/action', { state: { force: true } })
              close()
            }}
          >
            Open
          </Button>
          <Button
            colorScheme="grey"
            className="w-[132px] h-[48px] text-white rounded-3xl"
            ref={lastFocusableElementRef}
            onClick={() => {
              close()
            }}
          >
            Cancel
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default OpenBlocksModal

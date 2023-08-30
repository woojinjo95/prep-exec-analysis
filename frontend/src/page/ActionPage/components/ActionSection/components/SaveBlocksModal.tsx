import React, { useEffect, useMemo, useRef, useState } from 'react'
import { Button, Input, Text, Modal } from '@global/ui'
import useFetchScenarios from '@global/hook/useFetchScenarios'
import { PAGE_SIZE_TWENTY } from '@global/constant'
import useIntersect from '@global/hook/useIntersect'
import { formatDateTo } from '@global/usecase'
import Scrollbars from 'react-custom-scrollbars-2'
import { useScenarioById } from '@global/api/hook'
import { useRecoilValue } from 'recoil'
import { scenarioIdState } from '@global/atom'

interface SaveBlocksModalProps {
  isOpen: boolean
  close: () => void
}

const SaveBlocksModal: React.FC<SaveBlocksModalProps> = ({ isOpen, close }) => {
  const firstFocusableElementRef = useRef<HTMLInputElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  const [blocksName, setBlocksName] = useState<string>('')

  const { data, hasNextPage, isFetching, fetchNextPage } = useFetchScenarios(PAGE_SIZE_TWENTY)

  const scenarioId = useRecoilValue(scenarioIdState)

  const { scenario: currentScenario } = useScenarioById({
    scenarioId,
    onSuccess: (res) => {
      setBlocksName(res.name)
    },
  })

  const ref = useIntersect((entry, observer) => {
    // 발견시 실행될 callback
    observer.unobserve(entry.target)

    if (hasNextPage && !isFetching) {
      // 다음 페이지가 존재하고 isFetching이 아니라면
      fetchNextPage()
    }
  })

  const scenarios = useMemo(() => {
    // InfiniteData type의 data를 flatMap으로 1 depth 배열로 평탄화 작업
    return data ? data.pages.flatMap(({ items }) => items) : []
  }, [data])

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
  return (
    <Modal
      mode="center"
      isOpen={isOpen}
      close={() => {
        close()
      }}
      title="Save Blocks"
    >
      <div className="h-[745px] w-[1140px] flex flex-col rounded-[10px]">
        <div className="w-full grid grid-cols-[1fr_6fr] items-center h-12 mb-4">
          <Text colorScheme="light" className="!text-lg " weight="bold">
            Name
          </Text>
          <Input value={blocksName} onChange={(e) => setBlocksName(e.target.value)} ref={firstFocusableElementRef} />
        </div>
        <div className="w-full grid grid-cols-[1fr_6fr] items-center h-12">
          <Text colorScheme="light" className="!text-lg " weight="bold">
            Tag
          </Text>
          <Input value={blocksName} onChange={(e) => setBlocksName(e.target.value)} />
        </div>
        <div className="mt-5 flex flex-col w-full min-h-[520px]">
          <div className="mt-9 w-full grid grid-cols-[35%_45%_20%] gap-x-2 min-h-[48px] items-end border-b-grey border-b-[1px] pb-2">
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
            renderThumbVertical={({ ...props }) => <div {...props} className="bg-[#4E525A] w-2 rounded-[5px] pr-2" />}
          >
            {scenarios?.map((scenario) => (
              <div className="flex flex-col w-full" key={`file_${scenario.name}`}>
                <div className="w-full grid grid-cols-[35%_45%_20%] border-b-grey border-b-[1px] min-h-[48px] items-center">
                  <div>
                    <Text className="text-white mr-3" invertBackground colorScheme="light-orange">
                      B
                    </Text>
                    <Text
                      size="md"
                      colorScheme="light"
                      className="cursor-pointer"
                      onClick={() => {
                        // setScenarioId(scenario.id)
                      }}
                    >
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
            colorScheme="primary"
            className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
            onClick={() => {
              console.log('test')
            }}
          >
            Save
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

export default SaveBlocksModal

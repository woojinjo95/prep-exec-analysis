import React, { useEffect, useMemo, useRef, useState } from 'react'
import { Button, Input, Text, Modal, Select, TagItem } from '@global/ui'
import useFetchScenarios from '@global/hook/useFetchScenarios'
import { PAGE_SIZE_TWENTY } from '@global/constant'
import useIntersect from '@global/hook/useIntersect'
import { formatDateTo } from '@global/usecase'
import { useScenarioById } from '@global/api/hook'
import { useRecoilState, useRecoilValue } from 'recoil'
import { playStartTimeState, scenarioIdState, testRunIdState } from '@global/atom'
import Tag from '@global/ui/Tag'
import { useMutation, useQuery } from 'react-query'
import { getTag, postCopyScenario, postTag, putScenario } from '@global/api/func'
import { useToast } from '@chakra-ui/react'
import { AxiosError } from 'axios'
import { useWebsocket } from '@global/hook'
import { useNavigate } from 'react-router-dom'
import ScrollComponent from '@global/ui/ScrollComponent'

interface SaveBlocksModalProps {
  isOpen: boolean
  close: () => void
  // 저장 후 분석 페이지 이동 여부
  isMoveAnalysisPage: boolean
  // 재생으로 연결되는지 여부
  isPlay: boolean
}

const SaveBlocksModal: React.FC<SaveBlocksModalProps> = ({ isOpen, close, isMoveAnalysisPage, isPlay }) => {
  const toast = useToast({ duration: 3000, isClosable: true })

  const firstFocusableElementRef = useRef<HTMLInputElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  const [blocksName, setBlocksName] = useState<string>('')
  const [blocksTags, setBlocksTags] = useState<string[]>([])
  const [tagInput, setTagInput] = useState<string>('')

  const {
    data,
    hasNextPage,
    isFetching,
    fetchNextPage,
    refetch: scenariosRefetch,
  } = useFetchScenarios(PAGE_SIZE_TWENTY)

  const [scenarioId, setScenarioId] = useRecoilState(scenarioIdState)

  const { sendMessage } = useWebsocket()

  const testrunId = useRecoilValue(testRunIdState)

  const { scenario: currentScenario, refetch: currentScenarioRefetch } = useScenarioById({
    scenarioId,
    testrunId,
    onSuccess: (res) => {
      if (res.is_active) {
        setBlocksName(res.name)
      } else {
        setBlocksName('undefined blocks')
      }

      setBlocksTags(res.tags)
    },
  })

  const { data: tags, refetch: tagRefetch } = useQuery<string[]>(['tags'], () => getTag())

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

  const [, setTestRunIdState] = useRecoilState(testRunIdState)

  const navigate = useNavigate()

  const searchedTags = useMemo(() => {
    if (!tags || !currentScenario) return null
    // if (tagInput === '') return null

    return tags.filter((tag) => tag.includes(tagInput) && blocksTags.find((_tag) => _tag === tag) === undefined)
  }, [tagInput, tags, blocksTags])

  const [, setPlayStartTime] = useRecoilState(playStartTimeState)

  const { mutate: postTagMutate } = useMutation(postTag, {
    onSuccess: () => {
      tagRefetch()
      scenariosRefetch()
    },
    onError: (err: AxiosError) => {
      if (err.status === 406) {
        toast({ status: 'error', title: 'Tag name duplicated' })
      }
      console.error(err)
    },
  })

  const { mutate: putScenarioMutate } = useMutation(putScenario, {
    onSuccess: () => {
      tagRefetch()
      scenariosRefetch()
      currentScenarioRefetch()

      close()

      if (isPlay && scenarioId) {
        sendMessage({
          level: 'info',
          msg: 'start_playblock',
          data: { scenario_id: scenarioId },
        })

        setPlayStartTime(new Date().getTime() / 1000)
      }

      // 분석페이지로 이동한다면
      if (isMoveAnalysisPage) {
        const date = new Date()
        const startDate = new Date(date)
        startDate.setMinutes(date.getMinutes() - 30)

        sendMessage({
          level: 'info',
          msg: 'analysis_mode_init',
          data: {
            start_time: startDate.getTime() / 1000,
            end_time: date.getTime() / 1000,
          },
        })
        navigate('/analysis')
      }
    },
    onError: (err: AxiosError) => {
      console.error(err)
    },
  })

  const { mutate: postCopyScenarioMutate } = useMutation(postCopyScenario, {
    onSuccess: (res) => {
      setScenarioId(res.id)
      setTestRunIdState(res.testrun_id)
      tagRefetch()
      scenariosRefetch()
      currentScenarioRefetch()
      close()

      if (isPlay && scenarioId) {
        sendMessage({
          level: 'info',
          msg: 'start_playblock',
          data: { scenario_id: scenarioId },
        })

        setPlayStartTime(new Date().getTime() / 1000)
      }

      if (isMoveAnalysisPage) {
        const date = new Date()
        const startDate = new Date(date)
        startDate.setMinutes(date.getMinutes() - 30)

        sendMessage({
          level: 'info',
          msg: 'analysis_mode_init',
          data: {
            start_time: startDate.getTime() / 1000,
            end_time: date.getTime() / 1000,
          },
        })
        navigate('/analysis')
      }
    },
    onError: (err: AxiosError) => {
      console.error(err)
    },
  })

  if (!(tags && currentScenario && scenarios)) return <div />

  return (
    <Modal
      isOpen={isOpen}
      close={() => {
        close()
      }}
      title="Save Blocks"
    >
      <div className="h-[745px] w-[1140px] flex flex-col">
        <div className="w-full grid grid-cols-[1fr_6fr] items-center h-12 mb-4">
          <Text colorScheme="light" className="!text-lg " weight="bold">
            Name
          </Text>
          <Input
            value={blocksName}
            onChange={(e) => {
              setBlocksName(e.target.value)
            }}
            ref={firstFocusableElementRef}
          />
        </div>
        <div className="w-full grid grid-cols-[1fr_6fr] items-center h-12">
          <Text colorScheme="light" className="!text-lg " weight="bold">
            Tag
          </Text>
          <Select
            colorScheme="charcoal"
            header={
              <div className="flex w-full">
                {blocksTags.map((tag) => (
                  <React.Fragment key={`blocks_${currentScenario.id}_${tag}`}>
                    <Tag
                      colorScheme="charcoal"
                      tag={tag}
                      onDelete={() => setBlocksTags((prev) => prev.filter((_tag) => _tag !== tag))}
                    />
                  </React.Fragment>
                ))}
                <input
                  className="ml-3 border-none bg-transparent w-full outline-none text-white"
                  value={tagInput}
                  onChange={(e) => {
                    e.stopPropagation()
                    setTagInput(e.target.value)
                  }}
                />
              </div>
            }
          >
            {searchedTags &&
              searchedTags.map((tag) => {
                return (
                  <TagItem
                    colorScheme="charcoal"
                    tag={tag}
                    tagRefetch={() => {
                      tagRefetch()
                    }}
                    scenariosRefetch={() => {
                      scenariosRefetch()
                    }}
                    key={`scenario_${currentScenario.id}_tag_item_${tag}`}
                    setBlocksTags={setBlocksTags}
                  />
                )
              })}
            {tagInput !== '' && (
              <div
                className="rounded-[4px] flex items-center px-3 py-1 hover:bg-light-charcoal cursor-pointer"
                onClick={(e) => {
                  e.stopPropagation()

                  if (tags && !tags.find((tag) => tag === tagInput)) {
                    postTagMutate(tagInput)
                    setBlocksTags((prev) => [...prev, tagInput])
                    setTagInput('')
                  } else {
                    toast({ status: 'error', title: 'Tag name duplicated' })
                  }
                }}
                onMouseDown={(e) => {
                  e.stopPropagation()
                }}
              >
                <Text colorScheme="light" className="mr-2">
                  Create :{' '}
                </Text>
                <Tag colorScheme="charcoal" tag={tagInput} />
              </div>
            )}
          </Select>
        </div>
        <div className="mt-5 flex flex-col w-full min-h-[520px]">
          <div className="mt-9 w-[calc(100%-16px)] grid grid-cols-[35%_45%_20%] gap-x-2 min-h-[48px] items-end border-b-grey border-b-[1px] pb-2">
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
          <ScrollComponent>
            {scenarios.map((scenario) => (
              <div className="flex flex-col w-full" key={`file_${scenario.name}`}>
                <div className="w-[calc(100%-16px)] grid grid-cols-[35%_45%_20%]  gap-x-2 border-b-grey border-b-[1px] min-h-[48px] items-center">
                  <div>
                    <Text className="text-white mr-3" invertBackground colorScheme="light-orange">
                      B
                    </Text>
                    <Text size="md" colorScheme="light" className="cursor-pointer">
                      {scenario.name}
                    </Text>
                  </div>

                  <div className="flex flex-wrap w-full h-full items-center">
                    {scenario.tags.map((tag) => (
                      <Tag key={`${scenario.name}_tag_${tag}`} tag={tag} colorScheme="dark" />
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
          </ScrollComponent>
        </div>
        <div className="flex justify-end mt-7">
          <Button
            colorScheme="primary"
            className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
            onClick={(e) => {
              e.stopPropagation()

              // 이미 있는 시나리오일 때
              if (currentScenario.is_active) {
                // 이름 변경하였을 때
                if (currentScenario.name !== blocksName) {
                  postCopyScenarioMutate({
                    copy_scenario: {
                      src_scenario_id: currentScenario.id,
                      name: blocksName,
                      tags: blocksTags,
                      block_group: currentScenario.block_group,
                    },
                  })
                } else {
                  putScenarioMutate({
                    new_scenario: {
                      ...currentScenario,
                      tags: blocksTags,
                    },
                  })
                }
              } else {
                // 처음 만든 시나리오 일 때
                putScenarioMutate({
                  new_scenario: {
                    ...currentScenario,
                    is_active: true,
                    tags: blocksTags,
                    name: blocksName,
                  },
                })
              }
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

              if (isPlay && scenarioId) {
                sendMessage({
                  level: 'info',
                  msg: 'start_playblock',
                  data: { scenario_id: scenarioId },
                })

                setPlayStartTime(new Date().getTime() / 1000)
              }

              if (isMoveAnalysisPage) {
                const date = new Date()
                const startDate = new Date(date)
                startDate.setMinutes(date.getMinutes() - 30)

                sendMessage({
                  level: 'info',
                  msg: 'analysis_mode_init',
                  data: {
                    start_time: startDate.getTime() / 1000,
                    end_time: date.getTime() / 1000,
                  },
                })
                navigate('/analysis')
              }
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

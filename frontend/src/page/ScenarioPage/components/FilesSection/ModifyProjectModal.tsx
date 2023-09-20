import { useToast } from '@chakra-ui/react'
import { ScenarioSummary } from '@global/api/entity'
import { getTag, postTag, putScenario } from '@global/api/func'
import { useScenarioById } from '@global/api/hook'
import { testRunIdState } from '@global/atom'
import { Modal, Text, Input, Button, Select, Tag, TagItem } from '@global/ui'
import { AxiosError } from 'axios'
import React, { useMemo, useRef, useState } from 'react'
import { useMutation, useQuery } from 'react-query'
import { useRecoilValue } from 'recoil'

interface ModifyProjectModalProps {
  scenarioSummary: ScenarioSummary
  isOpen: boolean
  close: () => void
  scenariosRefetch: () => void
}

const ModifyProjectModal: React.FC<ModifyProjectModalProps> = ({
  isOpen,
  close,
  scenarioSummary,
  scenariosRefetch,
}) => {
  const toast = useToast({ duration: 3000, isClosable: true })

  const [scenarioName, setScenarioName] = useState<string>(scenarioSummary.name)
  const [scenarioTags, setScenarioTags] = useState<string[]>(scenarioSummary.tags)
  const [tagInput, setTagInput] = useState<string>('')

  const firstFocusableElementRef = useRef<HTMLInputElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  const { data: tags, refetch: tagRefetch } = useQuery<string[]>(['tags'], () => getTag())

  const searchedTags = useMemo(() => {
    if (!tags) return null
    // if (tagInput === '') return null

    return tags.filter((tag) => tag.includes(tagInput) && scenarioTags.find((_tag) => _tag === tag) === undefined)
  }, [tagInput, tags, scenarioTags])

  const testrunId = useRecoilValue(testRunIdState)

  const { scenario } = useScenarioById({ scenarioId: scenarioSummary.id, testrunId })

  const { mutate: postTagMutate } = useMutation(postTag, {
    onSuccess: () => {
      tagRefetch()
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
      scenariosRefetch()
      close()
    },
    onError: () => {
      alert('시나리오 수정에 실패하였습니다')
      scenariosRefetch()
      close()
    },
  })

  return (
    <Modal
      isOpen={isOpen}
      close={() => {
        close()
      }}
      title="Modify Project"
    >
      <div className="h-[200px] w-[1140px] flex flex-col">
        <div className="w-full grid grid-cols-[1fr_6fr] items-center h-12 mb-4">
          <Text colorScheme="light" className="!text-lg " weight="bold">
            Name
          </Text>
          <Input
            value={scenarioName}
            onChange={(e) => {
              setScenarioName(e.target.value)
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
                {scenarioTags.map((tag) => (
                  <React.Fragment key={`blocks_${scenarioSummary.id}_${tag}`}>
                    <Tag
                      colorScheme="charcoal"
                      tag={tag}
                      onDelete={() => setScenarioTags((prev) => prev.filter((_tag) => _tag !== tag))}
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
                    key={`scenario_${scenarioSummary.id}_tag_item_${tag}`}
                    setBlocksTags={setScenarioTags}
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
                    setScenarioTags((prev) => [...prev, tagInput])
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
        <div className="flex justify-end mt-7">
          <Button
            colorScheme="primary"
            className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
            onClick={() => {
              if (!scenario) return
              putScenarioMutate({
                new_scenario: {
                  ...scenario,
                  name: scenarioName,
                  tags: scenarioTags,
                },
              })
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

export default ModifyProjectModal

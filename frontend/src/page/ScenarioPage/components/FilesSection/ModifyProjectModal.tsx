import { useToast } from '@chakra-ui/react'
import { ScenarioSummary } from '@global/api/entity'
import { getTag, postTag } from '@global/api/func'
import { Modal, Text, Input, Button, Select, Tag, TagItem } from '@global/ui'
import { AxiosError } from 'axios'
import React, { useMemo, useRef, useState } from 'react'
import { useMutation, useQuery } from 'react-query'

interface ModifyProjectModalProps {
  scenario: ScenarioSummary
  isOpen: boolean
  close: () => void
}

const ModifyProjectModal: React.FC<ModifyProjectModalProps> = ({ isOpen, close, scenario }) => {
  const toast = useToast({ duration: 3000, isClosable: true })

  const [scenarioName, setScenarioName] = useState<string>(scenario.name)
  const [scenarioTags, setScenarioTags] = useState<string[]>(scenario.tags)
  const [tagInput, setTagInput] = useState<string>('')

  const firstFocusableElementRef = useRef<HTMLInputElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  const { data: tags, refetch: tagRefetch } = useQuery<string[]>(['tags'], () => getTag())

  const searchedTags = useMemo(() => {
    if (!tags) return null
    // if (tagInput === '') return null

    return tags.filter((tag) => tag.includes(tagInput) && scenarioTags.find((_tag) => _tag === tag) === undefined)
  }, [tagInput, tags, scenarioTags])

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
                  <React.Fragment key={`blocks_${scenario.id}_${tag}`}>
                    <Tag
                      tag={tag}
                      mode="delete"
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
                    key={`scenario_${scenario.id}_tag_item_${tag}`}
                    setBlocksTags={setScenarioTags}
                  />
                )
              })}
            {tagInput !== '' && (
              <div
                className="h-11 flex px-3 py-2 hover:bg-light-charcoal cursor-pointer"
                onClick={() => {
                  if (!scenarioTags.find((tag) => tag === tagInput)) {
                    postTagMutate(tagInput)
                    setScenarioTags((prev) => [...prev, tagInput])
                    setTagInput('')
                  } else {
                    toast({ status: 'error', title: 'Tag name duplicated' })
                  }
                }}
              >
                <Text colorScheme="light" className="mr-2">
                  Create :{' '}
                </Text>
                <Tag tag={tagInput} />
              </div>
            )}
          </Select>
        </div>
        <div className="flex justify-end mt-7">
          <Button colorScheme="primary" className="w-[132px] h-[48px] mr-3 text-white rounded-3xl">
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

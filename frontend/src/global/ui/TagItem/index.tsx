import React, { useState } from 'react'
import cx from 'classnames'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { useMutation } from 'react-query'
import { deleteTag, putTag } from '@global/api/func'
import { AxiosError } from 'axios'
import { useToast } from '@chakra-ui/react'
import { DropdownWithMoreButton, Input, OptionItem, Text } from '..'
import Tag from '../Tag'

interface TagItemProps extends React.LiHTMLAttributes<HTMLLIElement> {
  mode?: 'create' | 'item'
  tag: string

  colorScheme?: 'dark' | 'charcoal' | 'light'
  isActive?: boolean
  setBlocksTags: React.Dispatch<React.SetStateAction<string[]>>
  tagRefetch: () => void
  scenariosRefetch?: () => void
}

/**
 * OptionList 아이템 컴포넌트로 사용 가능
 *
 * OptionList 컴포넌트와 같이 사용
 */
const TagItem: React.FC<TagItemProps> = ({
  mode = 'item',
  tag,
  colorScheme = 'charcoal',
  isActive,
  setBlocksTags,
  tagRefetch,
  scenariosRefetch,
  ...props
}) => {
  const toast = useToast({ duration: 3000, isClosable: true })
  const { mutate: deleteTagMutate } = useMutation(deleteTag, {
    onSuccess: () => {
      tagRefetch()
      scenariosRefetch?.()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  const [tagInput, setTagInput] = useState<string>(tag)

  const { mutate: putTagMutate } = useMutation(putTag, {
    onSuccess: () => {
      tagRefetch()
      scenariosRefetch?.()
    },
    onError: (err: AxiosError) => {
      if (err.status === 406) {
        toast({ status: 'error', title: 'Tag name duplicated' })
        return
      }
      console.error(err)
    },
  })

  return (
    <li
      className={cx(
        'rounded-[4px] px-3 py-2 cursor-pointer truncate hover:backdrop-brightness-110',
        {
          'bg-charcoal': colorScheme === 'dark' && isActive,
          'bg-light-charcoal': colorScheme === 'charcoal' && isActive,
          'bg-[#F1F2F4]': colorScheme === 'light' && isActive,

          'hover:bg-charcoal': colorScheme === 'dark',
          'hover:bg-light-charcoal': colorScheme === 'charcoal',
          'hover:bg-[#F1F2F4]': colorScheme === 'light',
        },
        props.className,
      )}
      onClick={(e) => {
        e.stopPropagation()
        setBlocksTags((prev) => [...prev, tag])
      }}
      onMouseDown={(e) => {
        e.stopPropagation()
      }}
      {...props}
    >
      {mode === 'item' && (
        <div className="flex justify-between items-center">
          <Tag colorScheme={colorScheme} tag={tag} />
          <DropdownWithMoreButton type="icon" colorScheme="charcoal">
            <OptionItem colorScheme="charcoal">
              <Input
                colorScheme="charcoal"
                onChange={(e) => {
                  setTagInput(e.target.value)
                }}
                onClick={(e) => {
                  e.stopPropagation()
                }}
                onMouseDown={(e) => {
                  e.stopPropagation()
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    putTagMutate({ targetTag: tag, newTag: tagInput })
                  }
                }}
                value={tagInput}
              />
            </OptionItem>
            <OptionItem colorScheme="charcoal">
              <div
                className="flex"
                onClick={(e) => {
                  e.stopPropagation()
                  deleteTagMutate(tag)
                }}
                onMouseDown={(e) => {
                  e.stopPropagation()
                }}
              >
                <TrashIcon className="w-4 h-[19px] fill-white mr-2" />
                <Text>Delete</Text>
              </div>
            </OptionItem>
          </DropdownWithMoreButton>
        </div>
      )}
    </li>
  )
}

export default TagItem

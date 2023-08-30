import React from 'react'
import cx from 'classnames'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { DropdownWithMoreButton, OptionItem, Text } from '..'
import Tag from '../Tag'

interface TagItemProps extends React.LiHTMLAttributes<HTMLLIElement> {
  mode?: 'create' | 'item'
  tag: string

  colorScheme?: 'dark' | 'charcoal' | 'light'
  isActive?: boolean
}

/**
 * OptionList 아이템 컴포넌트로 사용 가능
 *
 * OptionList 컴포넌트와 같이 사용
 */
const TagItem: React.FC<TagItemProps> = ({ mode = 'item', tag, colorScheme = 'charcoal', isActive, ...props }) => {
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
      {...props}
    >
      {mode === 'item' && (
        <div
          className="flex justify-between"
          // onClick={(e) => {
          //   e.stopPropagation()
          //   e.preventDefault()
          // }}
        >
          <Tag tag={tag} />
          <DropdownWithMoreButton type="icon" colorScheme="charcoal">
            <OptionItem colorScheme="charcoal">Testing</OptionItem>
            <OptionItem colorScheme="charcoal">
              <div className="flex">
                <TrashIcon className="w-4 h-[19px] fill-white" />
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

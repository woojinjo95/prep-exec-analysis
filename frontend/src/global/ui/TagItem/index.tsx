import React from 'react'
import cx from 'classnames'
import { Text } from '..'

interface TagItemProps extends React.LiHTMLAttributes<HTMLLIElement> {
  mode?: 'create' | 'item'
  tag?: string

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
        <div className="flex justify-between">
          <Text className="text-white mr-2 mb-2" invertBackground colorScheme="dark-grey">
            {tag}
          </Text>
        </div>
      )}
    </li>
  )
}

export default TagItem

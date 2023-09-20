import React from 'react'
import cx from 'classnames'
import { Text } from '@global/ui'
import { ReactComponent as XIcon } from '@assets/images/x.svg'

interface TagProps {
  tag: string
  onDelete?: () => void
  colorScheme: 'light' | 'charcoal' | 'dark'
}

const Tag: React.FC<TagProps> = ({ tag, onDelete, colorScheme }) => {
  return (
    <div
      className={cx('flex justify-between items-center border rounded-[4px] px-2 py-1 mr-1', {
        'bg-white': colorScheme === 'light',
        'border-light-grey': colorScheme === 'light',
        'bg-light-charcoal': colorScheme === 'charcoal',
        'border-grey': colorScheme === 'charcoal',
        'bg-charcoal': colorScheme === 'dark',
        'border-light-charcoal': colorScheme === 'dark',
      })}
    >
      <Text weight="medium" size="sm" className="truncate">
        {tag}
      </Text>
      {onDelete && (
        <XIcon
          className="w-[9px] h-[9px] ml-3 fill-white"
          onClick={(e) => {
            e.stopPropagation()
            onDelete()
          }}
        />
      )}
    </div>
  )
}

export default Tag

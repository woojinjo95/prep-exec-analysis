import React from 'react'
import { Text } from '@global/ui'
import { ReactComponent as XIcon } from '@assets/images/x.svg'

interface TagProps {
  mode?: 'delete' | 'normal'
  tag: string
  onDelete?: () => void
}

const Tag: React.FC<TagProps> = ({ mode = 'normal', tag, onDelete }) => {
  return (
    <Text colorScheme="light-charcoal" invertBackground className="border border-grey p-1">
      {mode === 'delete' ? (
        <div className="flex justify-between items-center ">
          <Text>{tag}</Text>
          <XIcon
            className="w-[9px] h-[9px] ml-3 fill-white hover:bg-grey"
            onClick={(e) => {
              e.stopPropagation()
              onDelete?.()
            }}
          />
        </div>
      ) : (
        <span>{tag}</span>
      )}
    </Text>
  )
}

export default Tag

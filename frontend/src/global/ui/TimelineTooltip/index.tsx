import React, { useRef } from 'react'
import { createPortal } from 'react-dom'
import { createPortalStyle, formatDateTo } from '@global/usecase'
import { Text } from '@global/ui'

type DefaultDataType = { datetime: number }

interface TimelineTooltipProps<T extends DefaultDataType> {
  posX: number
  data: T | null
  children?: React.ReactNode | React.ReactNode[]
}

/**
 * 타임라인 차트의 툴팁 컴포넌트
 */
const TimelineTooltip = <T extends DefaultDataType>({
  posX,
  data,
  children,
}: TimelineTooltipProps<T>): React.ReactElement => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)

  return (
    <div
      ref={wrapperRef}
      className="absolute top-0 h-full w-1 bg-white opacity-30"
      style={{
        transform: `translateX(${posX - 2}px)`,
      }}
    >
      {!!data &&
        createPortal(
          <div
            className="fixed bg-light-black border border-charcoal rounded-lg p-4 grid grid-cols-1 gap-y-2 shadow-lg shadow-black z-10"
            style={createPortalStyle({ wrapperRef, spaceY: 8 })}
          >
            <Text colorScheme="light" weight="medium">
              {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(data.datetime))}
            </Text>

            {children}
          </div>,
          document.body,
        )}
    </div>
  )
}

export default TimelineTooltip

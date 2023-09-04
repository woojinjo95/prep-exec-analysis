import React from 'react'
import { createPortal } from 'react-dom'
import { createPortalStyle, formatDateTo } from '@global/usecase'
import { Text } from '@global/ui'

type DefaultDataType = { datetime: number }

interface TimelineTooltipProps<T extends DefaultDataType> {
  posX: number
  data: T
  wrapperRef: React.MutableRefObject<HTMLDivElement | null>
  children?: React.ReactNode | React.ReactNode[]
}

/**
 * 타임라인 차트의 툴팁 컴포넌트
 */
const TimelineTooltip = <T extends DefaultDataType>({
  data,
  children,
  wrapperRef,
}: TimelineTooltipProps<T>): React.ReactElement => {
  return createPortal(
    <div
      // FIXME: 툴팁 내에서 스크롤 가능하도록
      className="fixed bg-light-black border border-charcoal rounded-lg p-4 grid grid-cols-1 gap-y-2 shadow-lg shadow-black z-10"
      style={createPortalStyle({ wrapperRef, spaceY: 8 })}
    >
      <Text colorScheme="light" weight="medium">
        {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(data.datetime))}
      </Text>

      <table className="border-t border-l border-charcoal">
        <tbody>{children}</tbody>
      </table>
    </div>,
    document.body,
  )
}

export default TimelineTooltip

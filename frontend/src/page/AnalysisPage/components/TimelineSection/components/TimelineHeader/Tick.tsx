import React from 'react'
import { Text } from '@global/ui'
import { formatDateTo } from '@global/usecase'

interface TickProps {
  width: number
  translateX: number
  time: Date
}

/**
 * 타임라인 차트 상단 Tick 컴포넌트
 */
const Tick: React.FC<TickProps> = ({ width, translateX, time }) => {
  return (
    <div
      className="h-full absolute top-0"
      style={{
        width,
        transform: `translateX(${translateX}px)`,
      }}
    >
      <div className="h-[calc(100%-13px)]">
        <Text colorScheme="grey" size="xs" className="absolute -translate-x-1/2 top-0.5">
          {formatDateTo('HH:MM:SS:MS', time)}
        </Text>
      </div>

      <div className="grid grid-rows-1 grid-cols-[auto_1fr]">
        {/* 큰 tick */}
        <div className="w-px h-[10px] bg-grey" />

        {/* 작은 tick */}
        <div className="flex justify-evenly items-end">
          {Array(15)
            .fill(0)
            .map((_, index) => (
              <div key={`timeline-header-small-tick-${index}`} className="w-px h-[6px] bg-grey" />
            ))}
        </div>
      </div>
    </div>
  )
}

export default Tick

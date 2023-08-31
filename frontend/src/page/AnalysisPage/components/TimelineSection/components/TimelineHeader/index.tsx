import React, { useMemo } from 'react'
import { Text } from '@global/ui'
import Tick from './Tick'

interface TimelineHeaderProps {
  scaleX: d3.ScaleTime<number, number, never> | null
  chartWidth: number | null
}

/**
 * 타임라인 차트 상단에 위치한 헤더 컴포넌트
 *
 * 필터 버튼, 시간 tick 표시
 */
const TimelineHeader: React.FC<TimelineHeaderProps> = ({ scaleX, chartWidth }) => {
  const ticks = useMemo(() => {
    if (!scaleX) return null
    return scaleX.ticks(10)
  }, [scaleX])

  // tick 컴포넌트 넓이
  const tickWidth = useMemo(() => {
    if (!scaleX || !ticks || !ticks.length) return null
    return scaleX(ticks[1]) - scaleX(ticks[0])
  }, [ticks])

  return (
    <div className="h-8 grid grid-cols-[192px_1fr] grid-rows-1">
      <div className="h-full w-48 bg-charcoal border-b-[1px] border-light-charcoal px-5 flex items-center">
        <Text colorScheme="light" weight="medium">
          Filter
        </Text>
      </div>

      {chartWidth && (
        <div
          className="h-full w-full relative overflow-hidden border-l-[0.5px] border-[#37383E]"
          style={{
            width: chartWidth,
          }}
        >
          {scaleX && ticks && tickWidth && (
            <>
              {/* 맨 앞쪽 tick은 안보이기 때문에 채우기용 tick 추가 */}
              <Tick time={new Date()} width={tickWidth} translateX={scaleX(ticks[0]) - tickWidth} />

              {/* tick 리스트 */}
              {ticks.map((time) => (
                <Tick
                  key={`timeline-header-tick-${time.toISOString()}`}
                  time={time}
                  width={tickWidth}
                  translateX={scaleX(time)}
                />
              ))}
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default TimelineHeader

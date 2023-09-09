import React, { useMemo, useRef } from 'react'
import { Text } from '@global/ui'
import { createPortalStyle, formatDateTo } from '@global/usecase'
import { ReactComponent as CursorIcon } from '@assets/images/pentagon.svg'
import Tick from './Tick'

interface TimelineHeaderProps {
  scaleX: d3.ScaleTime<number, number, never> | null
  chartWidth?: number
  cursorTranslateX?: number
  isCursorDragging: boolean
}

/**
 * 타임라인 차트 상단에 위치한 헤더 컴포넌트
 *
 * 필터 버튼, 시간 tick 표시
 */
const TimelineHeader: React.FC<TimelineHeaderProps> = ({ scaleX, chartWidth, cursorTranslateX, isCursorDragging }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)

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
          ref={wrapperRef}
          className="h-full w-full relative overflow-hidden border-l-[0.5px] border-[#37383E]"
          style={{
            width: chartWidth,
          }}
        >
          {cursorTranslateX !== undefined && (
            <div>
              {/* 인디케이터의 오각형 아이콘 */}
              <CursorIcon
                className="absolute w-3 h-3 fill-primary bottom-0 -left-1.5 z-[5]"
                style={{
                  transform: `translateX(${cursorTranslateX}px)`,
                }}
              />
              {/* 인디케이터가 위치하는 시간 */}
              {isCursorDragging && !!scaleX && (
                <div
                  className="fixed bg-primary z-[5] px-2 rounded-sm"
                  style={{
                    ...createPortalStyle({ wrapperRef, spaceY: -60 }),
                    transform: `translateX(${cursorTranslateX}px)`,
                  }}
                >
                  <Text size="xs">{formatDateTo('YYYY-MM-DD HH:MM:SS:MS', scaleX.invert(cursorTranslateX))}</Text>
                </div>
              )}
            </div>
          )}

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

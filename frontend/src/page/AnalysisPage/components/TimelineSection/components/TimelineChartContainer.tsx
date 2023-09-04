import React from 'react'
import { CHART_HEIGHT } from '@global/constant'

interface TimelineChartContainerProps {
  cursorTranslateX: number
  onPointerDown: React.PointerEventHandler<HTMLDivElement>
  onPointerMove: React.PointerEventHandler<HTMLDivElement>
  onPointerUp: React.PointerEventHandler<HTMLDivElement>
  children: React.ReactNode | React.ReactNode[]
}

/**
 * 차트를 감싸는 컨테이너 컴포넌트
 *
 * 분석 페이지에서 포커스하고있는 측정결과 시간 커서 막대기 컴포넌트 또한 표시
 */
const TimelineChartContainer = React.forwardRef<HTMLDivElement, TimelineChartContainerProps>(
  ({ cursorTranslateX, onPointerDown, onPointerMove, onPointerUp, children }, ref) => {
    return (
      <div
        ref={ref}
        className="border-l-[0.5px] border-r-[0.5px] border-[#37383E] relative cursor-pointer"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
      >
        {/* cursor 막대기 */}
        <div
          className="absolute top-0 -left-px h-full w-0.5 bg-primary z-[5]"
          style={{
            // TODO: 표시되는 차트 개수에 따라 유동적으로 변경
            height: CHART_HEIGHT * 10,
            transform: `translateX(${cursorTranslateX}px)`,
          }}
        />

        {children}
      </div>
    )
  },
)

TimelineChartContainer.displayName = 'TimelineChartContainer'

export default TimelineChartContainer

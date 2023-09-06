import React from 'react'
import { CHART_HEIGHT } from '@global/constant'
import { PointChartData } from '@global/types'

interface PointChartProps {
  data: PointChartData
  scaleX: d3.ScaleTime<number, number, never> | null
}

/**
 * 포인트 차트
 *
 * TODO: resizing event
 * TODO: data 개별 color
 */
const PointChart: React.FC<PointChartProps> = ({ data, scaleX }) => {
  if (!scaleX) return <div />
  return (
    <div className="w-full relative">
      <div
        className="flex justify-center items-center border-b border-t border-[#37383E]"
        style={{ height: CHART_HEIGHT }}
      >
        <div className="h-[0.5px] w-full bg-[#37383E]" />
      </div>

      <div>
        {data.map(({ datetime, color }, index) => (
          <div
            key={`point-chart-${datetime}-${index}`}
            className="w-0.5 h-full absolute top-0"
            style={{
              transform: `translateX(${scaleX(new Date(datetime)) - 1}px)`,
              backgroundColor: color,
            }}
          />
        ))}
      </div>
    </div>
  )
}

export default React.memo(PointChart)

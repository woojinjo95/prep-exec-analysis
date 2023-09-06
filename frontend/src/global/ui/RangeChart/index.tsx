import { CHART_HEIGHT } from '@global/constant'
import { RangeChartData } from '@global/types'
import React from 'react'

interface RangeChartProps {
  data: RangeChartData
  scaleX: d3.ScaleTime<number, number, never> | null
}

/**
 * 범위 차트
 *
 * TODO: resizing event
 * TODO: data 개별 color
 */
const RangeChart: React.FC<RangeChartProps> = ({ data, scaleX }) => {
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
        {data.map(({ datetime, duration, color }, index) => {
          return (
            <div
              key={`point-chart-${datetime}-${index}`}
              className="h-full absolute top-0"
              style={{
                transform: `translateX(${scaleX(new Date(datetime)) - 1}px)`,
                width: Math.max(scaleX(new Date(datetime + duration)) - scaleX(new Date(datetime)), 2),
                backgroundColor: color,
              }}
            />
          )
        })}
      </div>
    </div>
  )
}

export default React.memo(RangeChart)

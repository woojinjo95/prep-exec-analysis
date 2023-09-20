import { RangeChartData } from '@global/types'
import React from 'react'

interface RangeChartProps {
  data: RangeChartData
  scaleX: d3.ScaleTime<number, number, never> | null
}

/**
 * 범위 차트
 */
const RangeChart: React.FC<RangeChartProps> = ({ data, scaleX }) => {
  if (!scaleX) return <div />
  return (
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
  )
}

export default React.memo(RangeChart)

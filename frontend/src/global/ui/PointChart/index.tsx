import React from 'react'
import { PointChartData } from '@global/types'

interface PointChartProps {
  data: PointChartData
  scaleX: d3.ScaleTime<number, number, never> | null
}

/**
 * 포인트 차트
 *
 * TODO: resizing event
 */
const PointChart: React.FC<PointChartProps> = ({ data, scaleX }) => {
  if (!scaleX) return <div />
  return (
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
  )
}

export default React.memo(PointChart)

import React from 'react'
import { PointChartData } from '../types'
import { CHART_HEIGHT } from '../constant'

interface PointChartProps {
  data: PointChartData
  scaleX: d3.ScaleTime<number, number, never> | null
  color: string
}

/**
 * 포인트 차트
 *
 * TODO: resizing event
 */
const PointChart: React.FC<PointChartProps> = ({ data, scaleX, color }) => {
  if (!scaleX) return <div />
  return (
    <div className="w-full relative">
      <div className="flex justify-center items-center" style={{ height: CHART_HEIGHT }}>
        <div className="h-[0.5px] w-full bg-[#37383E]" />
      </div>

      <div>
        {data.map((date, index) => (
          <div
            key={`point-chart-${date.toISOString()}-${index}`}
            className="w-0.5 h-full absolute top-0"
            style={{
              transform: `translateX(${scaleX(date) - 1}px)`,
              backgroundColor: color,
            }}
          />
        ))}
      </div>
    </div>
  )
}

export default PointChart

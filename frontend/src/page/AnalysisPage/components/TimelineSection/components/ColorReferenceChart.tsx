import React, { useMemo, useRef } from 'react'
import * as d3 from 'd3'
import { AreaChart } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import { useColorReferences } from '@page/AnalysisPage/api/hook'
import { useTooltipEvent } from '../hook'

interface ColorReferenceChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * Color Reference 차트
 */
const ColorReferenceChart: React.FC<ColorReferenceChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { colorReferences } = useColorReferences({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const colorReferenceData = useMemo(() => {
    if (!colorReferences) return null
    return colorReferences.map(({ timestamp, color_reference }) => ({
      datetime: new Date(timestamp).getTime(),
      value: color_reference,
    }))
  }, [colorReferences])

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(
    () => d3.scaleLinear().domain([0, 8]).range([CHART_HEIGHT, 0]),
    [],
  )

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<
    NonNullable<typeof colorReferenceData>[number]
  >({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!colorReferenceData) return <div style={{ height: CHART_HEIGHT }} />
  return (
    <div onMouseMove={onMouseMove(colorReferenceData)} onMouseLeave={onMouseLeave} className="relative overflow-hidden">
      {!!posX && (
        <div
          ref={wrapperRef}
          className="absolute top-0 h-full w-1 bg-white opacity-30 z-[5]"
          style={{
            transform: `translateX(${posX - 2}px)`,
          }}
        />
      )}

      {/* 툴팁 데이터 위치를 표시하는 포인트 */}
      {!!tooltipData && !!scaleX && (
        <div
          className="absolute -top-[3px] -left-[3px] w-[6px] h-[6px] rounded-full z-10 opacity-70 border border-white"
          style={{
            transform: `translate(${scaleX(new Date(tooltipData.datetime))}px, ${scaleY(tooltipData.value)}px)`,
          }}
        />
      )}

      <div style={{ height: CHART_HEIGHT }}>
        <AreaChart
          chartWidth={dimension?.width}
          scaleX={scaleX}
          scaleY={scaleY}
          data={colorReferenceData}
          minValue={0}
        />
      </div>
    </div>
  )
}

export default ColorReferenceChart

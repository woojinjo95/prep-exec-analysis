import React, { useMemo, useRef } from 'react'
import * as d3 from 'd3'
import { AreaChart, TimelineTooltip, TimelineTooltipItem, Text, Skeleton } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import { bytesToSize } from '@global/usecase'
import { useMemory } from '@page/AnalysisPage/api/hook'
import { useTooltipEvent } from '../hook'

interface MemoryChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  isVisible?: boolean
}

/**
 * Memory 사용률 차트
 */
const MemoryChart: React.FC<MemoryChartProps> = ({ scaleX, startTime, endTime, dimension, isVisible }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { memory } = useMemory({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const memoryData = useMemo(() => {
    if (!memory) return null
    return memory.map(({ timestamp, memory_usage, ...data }) => ({
      datetime: new Date(timestamp).getTime(),
      value: Number(memory_usage),
      ...data,
    }))
  }, [memory])

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(
    () => d3.scaleLinear().domain([0, 100]).range([CHART_HEIGHT, 0]),
    [],
  )

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof memoryData>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!isVisible) return null
  if (!memoryData) {
    return <Skeleton className="w-full border-b border-[#37383E]" style={{ height: CHART_HEIGHT }} colorScheme="dark" />
  }
  return (
    <div onMouseMove={onMouseMove(memoryData)} onMouseLeave={onMouseLeave} className="relative overflow-hidden">
      {!!posX && (
        <div
          ref={wrapperRef}
          className="absolute top-0 h-full w-1 bg-white/30 z-[5]"
          style={{
            transform: `translateX(${posX - 2}px)`,
          }}
        >
          {!!tooltipData && (
            <TimelineTooltip posX={posX} data={tooltipData} wrapperRef={wrapperRef}>
              <TimelineTooltipItem label="Total RAM">
                <Text colorScheme="light">{bytesToSize(Number(tooltipData.total_ram))}</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Used RAM">
                <Text colorScheme="light">{bytesToSize(Number(tooltipData.used_ram))}</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Free RAM">
                <Text colorScheme="light">{bytesToSize(Number(tooltipData.free_ram))}</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Lost RAM">
                <Text colorScheme="light">{bytesToSize(Number(tooltipData.lost_ram))}</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
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
          data={memoryData}
          minValue={0}
          strokeColor="#fa70d8"
          fillColor="#fa70d8"
        />
      </div>
    </div>
  )
}

export default MemoryChart

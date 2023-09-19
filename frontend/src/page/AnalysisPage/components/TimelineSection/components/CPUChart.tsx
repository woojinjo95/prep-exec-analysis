import React, { useMemo, useRef } from 'react'
import * as d3 from 'd3'
import { AreaChart, TimelineTooltip, TimelineTooltipItem, Text } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import { useCPU } from '@page/AnalysisPage/api/hook'
import { useTooltipEvent } from '../hook'

interface CPUChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  isVisible?: boolean
}

/**
 * CPU 사용률 차트
 */
const CPUChart: React.FC<CPUChartProps> = ({ scaleX, startTime, endTime, dimension, isVisible }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { cpu } = useCPU({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const cpuData = useMemo(() => {
    if (!cpu) return null
    return cpu.map(({ timestamp, cpu_usage, ...data }) => ({
      datetime: new Date(timestamp).getTime(),
      value: Number(cpu_usage),
      ...data,
    }))
  }, [cpu])

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(
    () => d3.scaleLinear().domain([0, 100]).range([CHART_HEIGHT, 0]),
    [],
  )

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof cpuData>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!isVisible) return null
  if (!cpuData) return <div style={{ height: CHART_HEIGHT }} />
  return (
    <div onMouseMove={onMouseMove(cpuData)} onMouseLeave={onMouseLeave} className="relative overflow-hidden">
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
              <TimelineTooltipItem label="Total">
                <Text colorScheme="light">{tooltipData.total}%</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="User">
                <Text colorScheme="light">{tooltipData.user}%</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Kernel">
                <Text colorScheme="light">{tooltipData.user}%</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Softirq">
                <Text colorScheme="light">{tooltipData.softirq}%</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Iowait">
                <Text colorScheme="light">{tooltipData.iowait}%</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Irq">
                <Text colorScheme="light">{tooltipData.irq}%</Text>
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
          data={cpuData}
          minValue={0}
          strokeColor="#f29213"
          fillColor="#f29213"
        />
      </div>
    </div>
  )
}

export default CPUChart

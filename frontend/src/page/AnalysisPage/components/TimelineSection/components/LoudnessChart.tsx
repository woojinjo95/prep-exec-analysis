import React, { useMemo, useRef } from 'react'
import * as d3 from 'd3'
import { AreaChart, TimelineTooltip, TimelineTooltipItem, Text } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { useLoudness } from '@page/AnalysisPage/api/hook'
import { useTooltipEvent } from '../hook'

interface LoudnessChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
}

/**
 * Loudness(소리) 변화 차트
 */
const LoudnessChart: React.FC<LoudnessChartProps> = ({ scaleX, startTime, endTime, dimension, summary }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { loudness } = useLoudness({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const loudnessData = useMemo(() => {
    if (!loudness) return null
    return loudness.map(({ timestamp, m }) => ({
      datetime: new Date(timestamp).getTime(),
      value: m,
    }))
  }, [loudness])

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(
    () => d3.scaleLinear().domain([-70, 0]).range([CHART_HEIGHT, 0]),
    [],
  )

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof loudnessData>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!loudnessData) return <div style={{ height: CHART_HEIGHT }} />
  return (
    <div onMouseMove={onMouseMove(loudnessData)} onMouseLeave={onMouseLeave} className="relative overflow-hidden">
      {!!posX && (
        <div
          ref={wrapperRef}
          className="absolute top-0 h-full w-1 bg-white opacity-30 z-[5]"
          style={{
            transform: `translateX(${posX - 2}px)`,
          }}
        >
          {!!tooltipData && (
            <TimelineTooltip posX={posX} data={tooltipData} wrapperRef={wrapperRef}>
              <TimelineTooltipItem label="M-LKFS">
                <Text colorScheme="light">{tooltipData.value} LKFS</Text>
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
          data={loudnessData}
          minValue={-70}
          strokeColor={summary.loudness?.color || 'white'}
          fillColor={summary.loudness?.color || 'white'}
        />
      </div>
    </div>
  )
}

export default LoudnessChart

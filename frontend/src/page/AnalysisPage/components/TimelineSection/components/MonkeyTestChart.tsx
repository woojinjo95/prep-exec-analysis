import React, { useMemo, useRef } from 'react'
import { useMonkeySection, useMonkeySmartSense } from '@page/AnalysisPage/api/hook'
import { PointChart, RangeChart, Text, TimelineTooltip, TimelineTooltipItem } from '@global/ui'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { CHART_HEIGHT } from '@global/constant'
import { useTooltipEvent } from '../hook'

interface MonkeyTestChartProps {
  scaleX: Parameters<typeof RangeChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
}

/**
 * Monkey Test 차트
 */
const MonkeyTestChart: React.FC<MonkeyTestChartProps> = ({ scaleX, startTime, endTime, dimension, summary }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { monkeySection } = useMonkeySection({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })
  const { monkeySmartSense } = useMonkeySmartSense({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const monkeyTestData = useMemo(() => {
    if (!monkeySection) return null
    return monkeySection.map(({ start_timestamp, end_timestamp }) => ({
      datetime: new Date(start_timestamp).getTime(),
      duration: new Date(end_timestamp).getTime() - new Date(start_timestamp).getTime(),
      color: summary.monkey_test?.color || 'white',
    }))
  }, [monkeySection, summary])

  const monkeySmartSenseData = useMemo(() => {
    if (!monkeySmartSense) return null
    return monkeySmartSense.map(({ timestamp, smart_sense_key }) => ({
      datetime: new Date(timestamp).getTime(),
      smart_sense_key,
      color: 'white',
    }))
  }, [monkeySmartSense, summary])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<
    NonNullable<typeof monkeySmartSenseData>[number]
  >({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!monkeyTestData || !monkeySmartSenseData) return <div />
  return (
    <div onMouseMove={onMouseMove(monkeySmartSenseData)} onMouseLeave={onMouseLeave} className="relative">
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
              <TimelineTooltipItem label="Smart Sense Key">
                <Text colorScheme="light">{tooltipData.smart_sense_key.join(', ')}</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      <div className="w-full relative border-b border-[#37383E]">
        <div className="flex justify-center items-center" style={{ height: CHART_HEIGHT - 1 }}>
          <div className="h-[0.5px] w-full bg-[#37383E]" />
        </div>
        <RangeChart scaleX={scaleX} data={monkeyTestData} />
        <PointChart scaleX={scaleX} data={monkeySmartSenseData} />
      </div>
    </div>
  )
}

export default MonkeyTestChart

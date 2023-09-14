import React, { useMemo, useRef } from 'react'
import { useRecoilValue } from 'recoil'
import { CHART_HEIGHT } from '@global/constant'
import { numberWithCommas } from '@global/usecase'
import { intelligentMonkeyTestSectionIdFilterListState } from '@global/atom'
import { PointChart, RangeChart, Text, TimelineTooltip, TimelineTooltipItem } from '@global/ui'
import { useIntelligentMonkeySection, useIntelligentMonkeySmartSense } from '@page/AnalysisPage/api/hook'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { useTooltipEvent } from '../hook'

const IntelligentMonkeyTestSectionColors = [
  '#97B9A8',
  '#7B899F',
  '#C1A3B3',
  '#8C7A95',
  '#E1DAAF',
  '#E5C1B3',
  '#5F666E',
  '#978673',
  '#645F41',
  '#648763',
  '#C59F74',
] as const

interface IntelligentMonkeyTestChartProps {
  scaleX: Parameters<typeof RangeChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
}

/**
 * Intelligent Monkey Test 차트
 */
const IntelligentMonkeyTestChart: React.FC<IntelligentMonkeyTestChartProps> = ({
  scaleX,
  startTime,
  endTime,
  dimension,
  summary,
}) => {
  const intelligentMonkeyTestSectionIdFilterList = useRecoilValue(intelligentMonkeyTestSectionIdFilterListState)
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { intelligentMonkeySection } = useIntelligentMonkeySection({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })
  const { intelligentMonkeySmartSense } = useIntelligentMonkeySmartSense({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const intelligentMonkeyTestData = useMemo(() => {
    if (!intelligentMonkeySection) return null
    return intelligentMonkeySection
      .filter(({ section_id }) => !intelligentMonkeyTestSectionIdFilterList.includes(section_id))
      .map(({ start_timestamp, end_timestamp, section_id }) => ({
        datetime: new Date(start_timestamp).getTime(),
        duration: new Date(end_timestamp).getTime() - new Date(start_timestamp).getTime(),
        color: IntelligentMonkeyTestSectionColors[section_id % IntelligentMonkeyTestSectionColors.length],
      }))
  }, [intelligentMonkeySection, summary, intelligentMonkeyTestSectionIdFilterList])

  const intelligentMonkeySmartSenseData = useMemo(() => {
    if (!intelligentMonkeySmartSense) return null
    return intelligentMonkeySmartSense
      .filter(({ section_id }) => !intelligentMonkeyTestSectionIdFilterList.includes(section_id))
      .map(({ timestamp, smart_sense_key, section_id }) => ({
        datetime: new Date(timestamp).getTime(),
        section_id,
        smart_sense_key,
        color: 'white',
      }))
  }, [intelligentMonkeySmartSense, summary, intelligentMonkeyTestSectionIdFilterList])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<
    NonNullable<typeof intelligentMonkeySmartSenseData>[number]
  >({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!intelligentMonkeyTestData || !intelligentMonkeySmartSenseData) return <div style={{ height: CHART_HEIGHT }} />
  return (
    <div onMouseMove={onMouseMove(intelligentMonkeySmartSenseData)} onMouseLeave={onMouseLeave} className="relative">
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
              <TimelineTooltipItem label="Menu">
                <Text colorScheme="light"># {numberWithCommas(tooltipData.section_id + 1)}</Text>
              </TimelineTooltipItem>

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
        <RangeChart scaleX={scaleX} data={intelligentMonkeyTestData} />
        <PointChart scaleX={scaleX} data={intelligentMonkeySmartSenseData} />
      </div>
    </div>
  )
}

export default IntelligentMonkeyTestChart

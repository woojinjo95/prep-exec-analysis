import React, { useMemo, useRef } from 'react'
import { useRecoilValue } from 'recoil'
import { RangeChart, TimelineTooltip, TimelineTooltipItem, Text, Skeleton } from '@global/ui'
import { freezeTypeFilterListState } from '@global/atom'
import { convertDuration } from '@global/usecase'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { useFreeze } from '@page/AnalysisPage/api/hook'
import { CHART_HEIGHT } from '@global/constant'
import { useTooltipEvent } from '../hook'

interface FreezeChartProps {
  scaleX: Parameters<typeof RangeChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
  isVisible?: boolean
}

/**
 * Video Analysis Result(freeze) 차트
 */
const FreezeChart: React.FC<FreezeChartProps> = ({ scaleX, startTime, endTime, dimension, summary, isVisible }) => {
  const freezeTypeFilterList = useRecoilValue(freezeTypeFilterListState)
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { freeze } = useFreeze({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    freeze_type: summary.freeze?.results.map(({ error_type }) => error_type),
  })

  const freezeData = useMemo(() => {
    if (!freeze) return null
    return freeze
      .filter(({ freeze_type }) => !freezeTypeFilterList.includes(freeze_type))
      .map(({ timestamp, duration }) => ({
        datetime: new Date(timestamp).getTime(),
        duration: duration * 1000,
        color: summary.freeze?.color || 'white',
      }))
  }, [freeze, summary, freezeTypeFilterList])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof freezeData>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!isVisible) return null
  if (!freezeData) {
    return <Skeleton className="w-full border-b border-[#37383E]" style={{ height: CHART_HEIGHT }} colorScheme="dark" />
  }
  return (
    <div onMouseMove={onMouseMove(freezeData)} onMouseLeave={onMouseLeave} className="relative">
      {!!posX && (
        <div
          ref={wrapperRef}
          className="absolute top-0 h-[calc(100%-1px)] w-1 bg-white/30 z-[5]"
          style={{
            transform: `translateX(${posX - 2}px)`,
          }}
        >
          {!!tooltipData && (
            <TimelineTooltip posX={posX} data={tooltipData} wrapperRef={wrapperRef}>
              <TimelineTooltipItem label="Error Type">
                <Text colorScheme="light">Freeze</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Duration">
                <Text colorScheme="light">{convertDuration(tooltipData.duration)}</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      {/* 툴팁 데이터 위치를 표시하는 엘리먼트 */}
      {!!tooltipData && !!scaleX && (
        <div
          className="absolute top-0 h-[calc(100%-1px)] bg-white/50 z-[5]"
          style={{
            transform: `translateX(${scaleX(new Date(tooltipData.datetime)) - 1}px)`,
            width: Math.max(
              scaleX(new Date(tooltipData.datetime + tooltipData.duration)) - scaleX(new Date(tooltipData.datetime)),
              2,
            ),
          }}
        />
      )}

      <div className="w-full relative border-b border-[#37383E]">
        <div className="flex justify-center items-center" style={{ height: CHART_HEIGHT - 1 }}>
          <div className="h-[0.5px] w-full bg-[#37383E]" />
        </div>
        <RangeChart scaleX={scaleX} data={freezeData} />
      </div>
    </div>
  )
}

export default FreezeChart

import React, { useMemo, useRef } from 'react'
import { useRecoilValue } from 'recoil'
import { PointChart, RangeChart, TimelineTooltip, TimelineTooltipItem, Text } from '@global/ui'
import { convertDuration } from '@global/usecase'
import { bootTypeFilterListState, resumeTypeFilterListState } from '@global/atom'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { useBoot, useResume } from '@page/AnalysisPage/api/hook'
import { CHART_HEIGHT } from '@global/constant'
import { useTooltipEvent } from '../hook'

interface ResumeBootChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
  isVisible?: boolean
}

/**
 * Resume(warm booting), Boot(cold booting) 시간 차트
 */
const ResumeBootChart: React.FC<ResumeBootChartProps> = ({
  scaleX,
  startTime,
  endTime,
  dimension,
  summary,
  isVisible,
}) => {
  const resumeTypeFilterList = useRecoilValue(resumeTypeFilterListState)
  const bootTypeFilterList = useRecoilValue(bootTypeFilterListState)
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { resume } = useResume({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })
  const { boot } = useBoot({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const data: { datetime: number; duration: number; color: string; type: 'Resume' | 'Boot' }[] | null = useMemo(() => {
    if (!resume || !boot) return null

    return [
      resume
        .filter(({ target }) => !resumeTypeFilterList.includes(target))
        .map(({ timestamp, measure_time }) => ({
          datetime: new Date(timestamp).getTime(),
          duration: measure_time,
          color: summary.resume?.color || 'white',
          type: 'Resume' as const,
        })),
      boot
        .filter(({ target }) => !bootTypeFilterList.includes(target))
        .map(({ timestamp, measure_time }) => ({
          datetime: new Date(timestamp).getTime(),
          duration: measure_time,
          color: summary.boot?.color || 'white',
          type: 'Boot' as const,
        })),
    ]
      .flat()
      .sort(({ datetime: aDatetime }, { datetime: bDatetime }) => (aDatetime > bDatetime ? 1 : 0))
  }, [resume, boot, summary, resumeTypeFilterList, bootTypeFilterList])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof data>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!isVisible) return null
  if (!data) return <div style={{ height: CHART_HEIGHT }} />
  return (
    <div onMouseMove={onMouseMove(data)} onMouseLeave={onMouseLeave} className="relative">
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
              <TimelineTooltipItem label="Type">
                <Text colorScheme="light">{tooltipData.type}</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Result">
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
        <RangeChart scaleX={scaleX} data={data} />
      </div>
    </div>
  )
}

export default ResumeBootChart

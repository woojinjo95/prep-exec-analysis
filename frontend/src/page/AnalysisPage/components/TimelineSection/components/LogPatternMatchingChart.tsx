import React, { useMemo, useRef } from 'react'
import { useRecoilValue } from 'recoil'
import { PointChart, TimelineTooltip, Text, TimelineTooltipItem } from '@global/ui'
import { logPatternMatchingNameFilterListState } from '@global/atom'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { useLogPatternMatching } from '@page/AnalysisPage/api/hook'
import { CHART_HEIGHT } from '@global/constant'
import { useTooltipEvent } from '../hook'

interface LogPatternMatchingChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
}

/**
 * 패턴에 매칭된 로그(log pattern matching) 차트
 */
const LogPatternMatchingChart: React.FC<LogPatternMatchingChartProps> = ({
  scaleX,
  startTime,
  endTime,
  dimension,
  summary,
}) => {
  const logPatternMatchingNameFilterList = useRecoilValue(logPatternMatchingNameFilterListState)
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { logPatternMatching } = useLogPatternMatching({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const logPatternMatchingData = useMemo(() => {
    if (!logPatternMatching) return null
    return logPatternMatching
      .filter(({ log_pattern_name }) => !logPatternMatchingNameFilterList.includes(log_pattern_name))
      .map(({ timestamp, log_pattern_name, log_level, message, regex }) => ({
        datetime: new Date(timestamp).getTime(),
        log_pattern_name,
        log_level,
        message,
        regex,
        color:
          summary.log_pattern_matching?.results.find(({ log_pattern_name: name }) => name === log_pattern_name)
            ?.color || 'white',
      }))
  }, [logPatternMatching, summary, logPatternMatchingNameFilterList])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<
    NonNullable<typeof logPatternMatchingData>[number]
  >({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!logPatternMatchingData) return <div />
  return (
    <div onMouseMove={onMouseMove(logPatternMatchingData)} onMouseLeave={onMouseLeave} className="relative">
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
              <TimelineTooltipItem label="Log Pattern Name">
                <Text colorScheme="light">{tooltipData.log_pattern_name}</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Log Level">
                <Text colorScheme="light">{tooltipData.log_level}</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Message">
                {/* FIXME: 정규표현식 통과하는 문자열은 다른 색상으로 표시 */}
                <Text colorScheme="light">{tooltipData.message}</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      <div className="w-full relative">
        <div
          className="flex justify-center items-center border-b border-t border-[#37383E]"
          style={{ height: CHART_HEIGHT }}
        >
          <div className="h-[0.5px] w-full bg-[#37383E]" />
        </div>
        <PointChart scaleX={scaleX} data={logPatternMatchingData} />
      </div>
    </div>
  )
}

export default LogPatternMatchingChart

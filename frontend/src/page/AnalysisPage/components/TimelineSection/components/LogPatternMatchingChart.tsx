import React, { useMemo, useRef } from 'react'
import { PointChart, TimelineTooltip, Text, TimelineTooltipItem } from '@global/ui'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { useLogPatternMatching } from '@page/AnalysisPage/api/hook'
import { useTooltipEvent } from '../hook'

interface LogPatternMatchingChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']

  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
}

/**
 * 패턴에 매칭된 로그(log pattern matching) 차트
 */
const LogPatternMatchingChart: React.FC<LogPatternMatchingChartProps> = ({ scaleX, dimension, summary }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  // TODO: 패턴별 보기 / 숨기기 기능
  const { logPatternMatching } = useLogPatternMatching()

  const logPatternMatchingData = useMemo(() => {
    if (!logPatternMatching) return null
    return logPatternMatching.map(({ timestamp, log_pattern_name, log_level, message, regex }) => ({
      datetime: new Date(timestamp).getTime(),
      log_pattern_name,
      log_level,
      message,
      regex,
      color:
        summary.log_pattern_matching?.results.find(({ log_pattern_name: name }) => name === log_pattern_name)?.color ||
        'white',
    }))
  }, [logPatternMatching, summary])

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

      <PointChart scaleX={scaleX} data={logPatternMatchingData} />
    </div>
  )
}

export default LogPatternMatchingChart

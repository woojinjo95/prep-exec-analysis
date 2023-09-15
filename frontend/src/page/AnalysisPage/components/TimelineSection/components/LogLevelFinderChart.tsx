import React, { useMemo, useRef } from 'react'
import { useRecoilValue } from 'recoil'
import { PointChart, TimelineTooltip, Text, TimelineTooltipItem } from '@global/ui'
import { logLevelFinderLogLevelFilterListState } from '@global/atom'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { useLogLevelFinders } from '@page/AnalysisPage/api/hook'
import { CHART_HEIGHT } from '@global/constant'
import { useTooltipEvent } from '../hook'

interface LogLevelFinderChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
  isVisible?: boolean
}

/**
 * Log Level Finder 차트
 */
const LogLevelFinderChart: React.FC<LogLevelFinderChartProps> = ({
  scaleX,
  startTime,
  endTime,
  dimension,
  summary,
  isVisible,
}) => {
  const logLevelFinderLogLevelFilterList = useRecoilValue(logLevelFinderLogLevelFilterListState)
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { logLevelFinders } = useLogLevelFinders({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    log_level: summary.log_level_finder?.results.map(({ target }) => target),
  })

  const logLevelFinderData = useMemo(() => {
    if (!logLevelFinders) return null
    return logLevelFinders
      .filter(({ log_level }) => !logLevelFinderLogLevelFilterList.includes(log_level))
      .map(({ timestamp, log_level }) => ({
        datetime: new Date(timestamp).getTime(),
        log_level,
        color: summary.log_level_finder?.color || 'white',
      }))
  }, [logLevelFinders, summary, logLevelFinderLogLevelFilterList])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<
    NonNullable<typeof logLevelFinderData>[number]
  >({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!isVisible) return null
  if (!logLevelFinderData) return <div style={{ height: CHART_HEIGHT }} />
  return (
    <div onMouseMove={onMouseMove(logLevelFinderData)} onMouseLeave={onMouseLeave} className="relative">
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
              <TimelineTooltipItem label="Log Level">
                <Text colorScheme="light">Logcat {tooltipData.log_level}</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      <div className="w-full relative border-b border-[#37383E]">
        <div className="flex justify-center items-center" style={{ height: CHART_HEIGHT - 1 }}>
          <div className="h-[0.5px] w-full bg-[#37383E]" />
        </div>
        <PointChart scaleX={scaleX} data={logLevelFinderData} />
      </div>
    </div>
  )
}

export default LogLevelFinderChart

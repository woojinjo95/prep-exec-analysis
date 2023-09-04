import React, { useMemo, useRef } from 'react'
import { PointChart, TimelineTooltip, Text, TimelineTooltipItem } from '@global/ui'
import { useLogLevelFinders } from '../api/hook'
import { useTooltipEvent } from '../hook'

interface LogLevelFinderChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * Log Level Finder 차트
 */
const LogLevelFinderChart: React.FC<LogLevelFinderChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { logLevelFinders } = useLogLevelFinders({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const logLevelFinderData = useMemo(() => {
    if (!logLevelFinders) return null
    return logLevelFinders.map(({ timestamp, log_level }) => ({ datetime: new Date(timestamp).getTime(), log_level }))
  }, [logLevelFinders])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<
    NonNullable<typeof logLevelFinderData>[number]
  >({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!logLevelFinderData) return <div />
  return (
    <div onMouseMove={onMouseMove(logLevelFinderData)} onMouseLeave={onMouseLeave} className="relative">
      {!!posX && (
        <div
          ref={wrapperRef}
          className="absolute top-0 h-full w-1 bg-white opacity-30"
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

      <PointChart scaleX={scaleX} data={logLevelFinderData} color="red" />
    </div>
  )
}

export default LogLevelFinderChart

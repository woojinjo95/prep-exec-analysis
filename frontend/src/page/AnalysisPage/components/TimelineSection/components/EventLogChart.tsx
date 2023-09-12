import React, { useMemo, useRef } from 'react'
import { PointChart, Text, TimelineTooltip, TimelineTooltipItem } from '@global/ui'
import { useEventLogs } from '@page/AnalysisPage/api/hook'
import { EventLogTooltip } from '@page/AnalysisPage/api/entity'
import { capitalize } from '@global/usecase'
import { CHART_HEIGHT } from '@global/constant'
import { useTooltipEvent } from '../hook'

// TODO: 이벤트로그 남은 항목 정리
const parseEventLog = (eventLog: EventLogTooltip) => {
  if (eventLog.msg === 'remocon_response') {
    return `RCU (${eventLog.data.type.toUpperCase()}) : ${capitalize(eventLog.data.key)}`
  }

  if (eventLog.msg === 'on_off_control_response' && eventLog.data.enable_dut_power_transition) {
    return `Control : DUT Power ${capitalize(eventLog.data.vac)}`
  }

  if (eventLog.msg === 'on_off_control_response' && eventLog.data.enable_hdmi_transition) {
    return `Control : HDMI ${capitalize(eventLog.data.vac)}`
  }

  if (eventLog.msg === 'on_off_control_response' && eventLog.data.enable_dut_wan_transition) {
    return `Control : DUT Wan ${capitalize(eventLog.data.vac)}`
  }

  if (eventLog.msg === 'shell_response') {
    return `${eventLog.data.mode} : ${eventLog.data.command}`
  }

  return ''
}

interface EventLogChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * 이벤트 로그 차트
 */
const EventLogChart: React.FC<EventLogChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { eventLogs } = useEventLogs({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const eventLogsData = useMemo(() => {
    if (!eventLogs) return null
    return eventLogs.map(({ timestamp, msg, data }) => ({
      datetime: new Date(timestamp).getTime(),
      msg,
      data,
      color: '#269',
    }))
  }, [eventLogs])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof eventLogsData>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!eventLogsData) return <div />
  return (
    <div onMouseMove={onMouseMove(eventLogsData)} onMouseLeave={onMouseLeave} className="relative">
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
              <TimelineTooltipItem label="Event Log">
                <Text colorScheme="light" className="break-all">
                  {parseEventLog(tooltipData as EventLogTooltip)}
                </Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      <div className="w-full relative border-b border-[#37383E]">
        <div className="flex justify-center items-center" style={{ height: CHART_HEIGHT - 1 }}>
          <div className="h-[0.5px] w-full bg-[#37383E]" />
        </div>
        <PointChart scaleX={scaleX} data={eventLogsData} />
      </div>
    </div>
  )
}

export default EventLogChart

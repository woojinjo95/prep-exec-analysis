import React, { useMemo, useRef } from 'react'
import { PointChart, Text, TimelineTooltip, TimelineTooltipItem } from '@global/ui'
import { useEventLogs } from '@page/AnalysisPage/api/hook'
import { EventLogTooltip } from '@page/AnalysisPage/api/entity'
import { capitalize } from '@global/usecase'
import { CHART_HEIGHT } from '@global/constant'
import { useTooltipEvent } from '../hook'

// TODO: 이벤트로그 남은 항목 정리
const parseEventLog = (eventLog: EventLogTooltip) => {
  // 리모컨
  if (eventLog.msg === 'remocon_response') {
    return `RCU (${eventLog.data.type.toUpperCase()}) : ${capitalize(eventLog.data.key)}`
  }

  if (eventLog.msg === 'capture_board_response') {
    return `Screen : Reset`
  }

  // 쉘 명령
  if (eventLog.msg === 'shell_response') {
    return `${eventLog.data.mode} : ${eventLog.data.command}`
  }

  // 쉘 연결(device info)
  if (eventLog.msg === 'config_response') {
    return eventLog.data.mode === 'adb'
      ? `Device Info : adb / ${eventLog.data.host}:${eventLog.data.port}`
      : `Device Info : ssh / ${eventLog.data.host}:${eventLog.data.port}, ID: ${eventLog.data.username || ''}, PW: ${
          eventLog.data.password || ''
        }`
  }

  // On/Off 제어
  if (eventLog.msg === 'on_off_control_response') {
    if (eventLog.data.enable_dut_power_transition) {
      return `Control : DUT Power ${capitalize(eventLog.data.vac)}`
    }

    if (eventLog.data.enable_hdmi_transition) {
      return `Control : HDMI ${capitalize(eventLog.data.vac)}`
    }

    if (eventLog.data.enable_dut_wan_transition) {
      return `Control : DUT Wan ${capitalize(eventLog.data.vac)}`
    }
  }

  // 네트워크 제어
  if (eventLog.msg === 'network_emulation_response') {
    // FIXME: bandwidth, delay, loss - 하나가 변경되어도 전체 bandwidth, delay, loss 데이터를 표기해야함
    if (eventLog.data.updated.packet_bandwidth && eventLog.data.action === 'update') {
      return `Packet Control : Bandwidth ${eventLog.data.updated.packet_bandwidth}Mbps`
    }

    if (eventLog.data.updated.packet_delay && eventLog.data.action === 'update') {
      return `Packet Control : Delay ${eventLog.data.updated.packet_delay}ms`
    }

    if (eventLog.data.updated.packet_loss && eventLog.data.action === 'update') {
      return `Packet Control : Loss ${eventLog.data.updated.packet_loss}%`
    }

    if (eventLog.data.updated.create && eventLog.data.action === 'create') {
      return `IP Limit(Registed) : ${eventLog.data.updated.create.ip}:${eventLog.data.updated.create.port} (${eventLog.data.updated.create.protocol})`
    }

    if (eventLog.data.updated.update && eventLog.data.action === 'update') {
      return `IP Limit(Modified) : ${eventLog.data.updated.update.ip}:${eventLog.data.updated.update.port} (${eventLog.data.updated.update.protocol})`
    }

    if (eventLog.data.updated.delete && eventLog.data.action === 'delete') {
      // FIXME: 무엇을 delete 했는지
      return `IP Limit(Deleted)`
    }

    if (eventLog.data.action === 'reset') {
      // FIXME: 무슨 데이터를 어떻게 표기해야 하는지
      return `Network Emulation Reset`
    }
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

  if (!eventLogsData) return <div style={{ height: CHART_HEIGHT }} />
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

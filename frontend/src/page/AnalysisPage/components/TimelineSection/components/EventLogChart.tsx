import React, { useMemo, useRef } from 'react'
import { createPortal } from 'react-dom'
import { PointChart, Text } from '@global/ui'
import { createPortalStyle, formatDateTo } from '@global/usecase'
import { useEventLogs } from '../api/hook'
import { useTooltipEvent } from '../hook'

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
  const tooltipWrapperRef = useRef<HTMLDivElement | null>(null)
  const { eventLogs } = useEventLogs({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const eventLogsData = useMemo(() => {
    if (!eventLogs) return null
    return eventLogs.map(({ timestamp, msg }) => ({ datetime: new Date(timestamp).getTime(), message: msg }))
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
          ref={tooltipWrapperRef}
          className="absolute top-0 h-full w-1 bg-white opacity-30"
          style={{
            transform: `translateX(${posX - 2}px)`,
          }}
        >
          {!!tooltipData &&
            createPortal(
              <div
                className="fixed bg-light-black border border-charcoal rounded-lg p-4 grid grid-cols-1 gap-y-2 shadow-lg shadow-black z-10"
                style={createPortalStyle({ wrapperRef: tooltipWrapperRef, spaceY: 8 })}
              >
                <Text colorScheme="light" weight="medium">
                  {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(tooltipData.datetime))}
                </Text>

                <table className="border-t border-l border-charcoal">
                  <tr>
                    <th className="border-r border-b border-charcoal bg-charcoal py-2 px-4 text-left">
                      <Text colorScheme="light" weight="medium">
                        Event Log
                      </Text>
                    </th>
                    <td className="border-r border-b border-charcoal py-2 px-4">
                      {/* TODO: 메시지 형식 확정 필요(기획) */}
                      <Text colorScheme="light">{tooltipData.message}</Text>
                    </td>
                  </tr>
                </table>
              </div>,
              document.body,
            )}
        </div>
      )}

      <PointChart scaleX={scaleX} data={eventLogsData} />
    </div>
  )
}

export default EventLogChart

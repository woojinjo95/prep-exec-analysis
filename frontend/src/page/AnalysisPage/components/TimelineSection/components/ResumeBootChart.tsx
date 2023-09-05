import React, { useMemo, useRef } from 'react'
import { PointChart, RangeChart, TimelineTooltip, TimelineTooltipItem, Text } from '@global/ui'
import { useBoot, useResume } from '../api/hook'
import { useTooltipEvent } from '../hook'

interface ResumeBootChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * Resume(warm booting), Boot(cold booting) 시간 차트
 */
const ResumeBootChart: React.FC<ResumeBootChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { resume } = useResume({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })
  const { boot } = useBoot({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const data: { datetime: number; duration: number; type: 'Resume' | 'Boot' }[] | null = useMemo(() => {
    if (!resume || !boot) return null

    return [
      resume.map(({ timestamp, measure_time }) => ({
        datetime: new Date(timestamp).getTime(),
        duration: measure_time,
        type: 'Resume' as const,
      })),
      boot.map(({ timestamp, measure_time }) => ({
        datetime: new Date(timestamp).getTime(),
        duration: measure_time,
        type: 'Boot' as const,
      })),
    ]
      .flat()
      .sort(({ datetime: aDatetime }, { datetime: bDatetime }) => (aDatetime > bDatetime ? 1 : 0))
  }, [resume, boot])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof data>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!data) return <div />
  return (
    <div onMouseMove={onMouseMove(data)} onMouseLeave={onMouseLeave} className="relative">
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
              <TimelineTooltipItem label="Type">
                <Text colorScheme="light">{tooltipData.type}</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Result">
                {/* FIXME: 1000ms 이하일 경우 -> ms로 표시, 나머지 -> h/m/s 표시 */}
                <Text colorScheme="light">{(tooltipData.duration / 1000).toFixed(1)}s</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      <RangeChart scaleX={scaleX} data={data} color="green" />
    </div>
  )
}

export default ResumeBootChart

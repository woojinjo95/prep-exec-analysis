import React, { useMemo, useRef } from 'react'
import { RangeChart, TimelineTooltip, TimelineTooltipItem, Text } from '@global/ui'
import { useFreeze } from '../api/hook'
import { useTooltipEvent } from '../hook'

interface FreezeChartProps {
  scaleX: Parameters<typeof RangeChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * Video Analysis Result(freeze) 차트
 */
const FreezeChart: React.FC<FreezeChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { freeze } = useFreeze({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const freezeData = useMemo(() => {
    if (!freeze) return null
    return freeze.map(({ timestamp, duration }) => ({
      datetime: new Date(timestamp).getTime(),
      duration: duration * 1000,
    }))
  }, [freeze])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof freezeData>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!freezeData) return <div />
  return (
    <div onMouseMove={onMouseMove(freezeData)} onMouseLeave={onMouseLeave} className="relative">
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
              <TimelineTooltipItem label="Error Type">
                <Text colorScheme="light">Freeze</Text>
              </TimelineTooltipItem>

              <TimelineTooltipItem label="Duration">
                <Text colorScheme="light">{(tooltipData.duration / 1000).toFixed(1)}s</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      <RangeChart scaleX={scaleX} data={freezeData} color="blue" />
    </div>
  )
}

export default FreezeChart

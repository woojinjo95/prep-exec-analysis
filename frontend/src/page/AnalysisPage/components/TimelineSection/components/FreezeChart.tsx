import React, { useMemo, useRef } from 'react'
import { RangeChart, TimelineTooltip, TimelineTooltipItem, Text } from '@global/ui'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { convertDuration } from '@global/usecase'
import { useFreeze } from '@page/AnalysisPage/api/hook'
import { useTooltipEvent } from '../hook'

interface FreezeChartProps {
  scaleX: Parameters<typeof RangeChart>[0]['scaleX']
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
}

/**
 * Video Analysis Result(freeze) 차트
 */
const FreezeChart: React.FC<FreezeChartProps> = ({ scaleX, dimension, summary }) => {
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { freeze } = useFreeze({
    // TODO: 타입별 보기 / 숨기기 기능
    freeze_type: summary.freeze?.results.map(({ error_type }) => error_type),
  })

  const freezeData = useMemo(() => {
    if (!freeze) return null
    return freeze.map(({ timestamp, duration }) => ({
      datetime: new Date(timestamp).getTime(),
      duration: duration * 1000,
      color: summary.freeze?.color || 'white',
    }))
  }, [freeze, summary])

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
                <Text colorScheme="light">{convertDuration(tooltipData.duration)}</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      <RangeChart scaleX={scaleX} data={freezeData} />
    </div>
  )
}

export default FreezeChart

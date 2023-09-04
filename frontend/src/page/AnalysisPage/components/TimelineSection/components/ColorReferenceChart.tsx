import React, { useMemo } from 'react'
import { AreaChart } from '@global/ui'
import { useColorReferences } from '../api/hook'

interface ColorReferenceChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * Color Reference 차트
 */
const ColorReferenceChart: React.FC<ColorReferenceChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const { colorReferences } = useColorReferences({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const colorReferenceData = useMemo(() => {
    if (!colorReferences) return null
    return colorReferences.map(({ timestamp, color_reference }) => ({
      date: new Date(timestamp),
      value: color_reference,
    }))
  }, [colorReferences])

  if (!colorReferenceData) return <div />
  return <AreaChart chartWidth={dimension?.width} scaleX={scaleX} data={colorReferenceData} minValue={0} maxValue={8} />
}

export default React.memo(ColorReferenceChart)

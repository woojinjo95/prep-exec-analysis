import React, { useMemo } from 'react'
import * as d3 from 'd3'
import { AreaChart } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
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
      datetime: new Date(timestamp).getTime(),
      value: color_reference,
    }))
  }, [colorReferences])

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(
    () => d3.scaleLinear().domain([0, 8]).range([CHART_HEIGHT, 0]),
    [],
  )

  if (!colorReferenceData) return <div />
  return (
    <AreaChart chartWidth={dimension?.width} scaleX={scaleX} scaleY={scaleY} data={colorReferenceData} minValue={0} />
  )
}

export default ColorReferenceChart

import * as d3 from 'd3'
import { useMemo } from 'react'

/**
 * 가로 시간축, 세로 숫자값축 scale
 */
export const useScale = ({
  width,
  height,
  xAxisMin,
  xAxisMax,
  yAxisMin,
  yAxisMax,
}: {
  width: number | null
  height: number | null
  xAxisMin: Date
  xAxisMax: Date
  yAxisMin: number
  yAxisMax: number
}) => {
  const scaleX: d3.ScaleTime<number, number, never> | null = useMemo(() => {
    if (!width) return null
    return d3.scaleTime().domain([xAxisMin, xAxisMax]).range([0, width])
  }, [width, xAxisMin, xAxisMax])

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(() => {
    if (!height) return null
    return d3.scaleLinear().domain([yAxisMin, yAxisMax]).range([height, 0])
  }, [height, yAxisMin, yAxisMax])

  return { scaleX, scaleY }
}

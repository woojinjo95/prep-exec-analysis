import * as d3 from 'd3'
import { useMemo } from 'react'

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

export class AreaChart {
  private svg: d3.Selection<SVGSVGElement, unknown, null, undefined>

  constructor(
    ref: HTMLDivElement,
    private width: number,
    private height: number,
    private scaleX: NonNullable<ReturnType<typeof useScale>['scaleX']>,
    private scaleY: NonNullable<ReturnType<typeof useScale>['scaleY']>,
  ) {
    const svg = d3
      .select(ref)
      .call((g) => g.select('svg').remove())
      .append('svg')
      .attr('viewBox', `0,0,${width},${height}`)
    this.svg = svg
  }

  public createXAxis() {
    const xAxis: (selection: d3.Selection<SVGGElement, unknown, null, undefined>) => void = (g) =>
      g
        .attr('transform', `translate(0,${this.height})`)
        .call(
          d3
            .axisBottom(this.scaleX)
            .ticks(this.width / 20)
            .tickSizeOuter(0),
        )
        .call((_g) => _g.select('.domain').remove())
        .call((_g) => _g.selectAll('text').remove())
        .call((_g) => _g.selectAll('line').attr('y1', -this.height).style('stroke', '#ddd').style('stroke-width', 0.5))
    this.svg.append('g').call(xAxis)
  }

  public createYAxis() {
    const yAxis: (selection: d3.Selection<SVGGElement, unknown, null, undefined>) => void = (g) =>
      g
        .attr('transform', `translate(0,0)`)
        .call(d3.axisLeft(this.scaleY).ticks(5))
        .call((_g) => _g.select('.domain').remove())
        .call((_g) => _g.selectAll('text').remove())
        .call((_g) => _g.selectAll('line').attr('x2', this.width).style('stroke', '#ddd').style('stroke-width', 0.5))
    this.svg.append('g').call(yAxis)
  }
}

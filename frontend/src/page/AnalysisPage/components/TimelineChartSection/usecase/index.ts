import * as d3 from 'd3'
import { sampleData } from '@page/AnalysisPage/components/TimelineChartSection/constant'
import { useScale } from '../hook'
import { AreaChartData } from '../types'

/**
 * svg를 이용한 영역 차트 생성기
 */
export class AreaChartGenerator {
  private svg!: d3.Selection<SVGSVGElement, unknown, null, undefined>

  constructor(
    private ref: HTMLDivElement,
    private width: number,
    private height: number,
    private scaleX: NonNullable<ReturnType<typeof useScale>['scaleX']>,
    private scaleY: NonNullable<ReturnType<typeof useScale>['scaleY']>,
  ) {}

  public createChart() {
    this.createSvg()
    this.createXAxis()
    this.createYAxis()
    this.createLine()
    this.createArea()
  }

  private createSvg() {
    const svg = d3
      .select(this.ref)
      .call((g) => g.select('svg').remove())
      .append('svg')
      .attr('viewBox', `0,0,${this.width},${this.height}`)
    this.svg = svg
  }

  /**
   * X축 및 세로 가이드라인(격자선) 생성
   */
  private createXAxis() {
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

  /**
   * Y축 및 가로 가이드라인(격자선) 생성
   */
  private createYAxis() {
    const yAxis: (selection: d3.Selection<SVGGElement, unknown, null, undefined>) => void = (g) =>
      g
        .attr('transform', `translate(0,0)`)
        .call(d3.axisLeft(this.scaleY).ticks(5))
        .call((_g) => _g.select('.domain').remove())
        .call((_g) => _g.selectAll('text').remove())
        .call((_g) => _g.selectAll('line').attr('x2', this.width).style('stroke', '#ddd').style('stroke-width', 0.5))
    this.svg.append('g').call(yAxis)
  }

  /**
   * 차트 라인 생성
   */
  private createLine() {
    const line = d3
      .line<AreaChartData[number]>()
      .defined((d) => !Number.isNaN(d.value))
      .x((d) => this.scaleX(d.date))
      .y((d) => this.scaleY(d.value))
    this.svg
      .append('path')
      .datum(sampleData)
      .attr('fill', 'none')
      .attr('stroke', '#269')
      .attr('stroke-width', 1)
      .attr('stroke-linejoin', 'round')
      .attr('stroke-linecap', 'round')
      .attr('opacity', '50%')
      .attr('d', line)
  }

  /**
   * 차트 라인 하단의 배경영역 생성
   */
  private createArea() {
    const area = d3
      .area<AreaChartData[number]>()
      .x((d) => this.scaleX(d.date))
      .y0(this.scaleY(0))
      .y1((d) => this.scaleY(d.value))
    this.svg.append('path').datum(sampleData).attr('fill', 'steelblue').attr('opacity', '50%').attr('d', area)
  }
}

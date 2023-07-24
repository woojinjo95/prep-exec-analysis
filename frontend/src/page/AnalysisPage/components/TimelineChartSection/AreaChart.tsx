import React, { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { sampleData } from '@page/AnalysisPage/constant'
import { useScale } from '@page/AnalysisPage/hook'
import { Text } from '@chakra-ui/react'

const AreaChart: React.FC = () => {
  const divRef = useRef<HTMLDivElement | null>(null)
  const [chartWidth, setChartWidth] = useState<number | null>(null)
  const [chartHeight, setChartHeight] = useState<number | null>(null)

  const { scaleX, scaleY } = useScale({
    width: chartWidth,
    height: chartHeight,
    xAxisMin: sampleData[0].date,
    xAxisMax: sampleData[sampleData.length - 1].date,
    yAxisMin: 0,
    yAxisMax: 100,
  })

  useEffect(() => {
    if (!divRef.current || !chartWidth || !chartHeight || !scaleX || !scaleY) return

    const svg = d3
      .select(divRef.current)
      .call((g) => g.select('svg').remove())
      .append('svg')
      .attr('viewBox', `0,0,${chartWidth},${chartHeight}`)

    const xAxis: (selection: d3.Selection<SVGGElement, unknown, null, undefined>) => void = (g) =>
      g
        .attr('transform', `translate(0,${chartHeight})`)
        .call(
          d3
            .axisBottom(scaleX)
            .ticks(chartWidth / 20)
            .tickSizeOuter(0),
        )
        .call((_g) => _g.select('.domain').remove())
        .call((_g) => _g.selectAll('text').remove())
        .call((_g) => _g.selectAll('line').attr('y1', -chartHeight).style('stroke', '#ddd').style('stroke-width', 0.5))
    svg.append('g').call(xAxis)

    const yAxis: (selection: d3.Selection<SVGGElement, unknown, null, undefined>) => void = (g) =>
      g
        .attr('transform', `translate(0,0)`)
        .call(d3.axisLeft(scaleY).ticks(5))
        .call((_g) => _g.select('.domain').remove())
        .call((_g) => _g.selectAll('text').remove())
        .call((_g) => _g.selectAll('line').attr('x2', chartWidth).style('stroke', '#ddd').style('stroke-width', 0.5))
    svg.append('g').call(yAxis)

    const line = d3
      .line<(typeof sampleData)[number]>()
      .defined((d) => !Number.isNaN(d.value))
      .x((d) => scaleX(d.date))
      .y((d) => scaleY(d.value))
    svg
      .append('path')
      .datum(sampleData)
      .attr('fill', 'none')
      .attr('stroke', '#269')
      .attr('stroke-width', 1)
      .attr('stroke-linejoin', 'round')
      .attr('stroke-linecap', 'round')
      .attr('opacity', '50%')
      .attr('d', line)

    const area = d3
      .area<(typeof sampleData)[number]>()
      .x((d) => scaleX(d.date))
      .y0(scaleY(0))
      .y1((d) => scaleY(d.value))
    svg.append('path').datum(sampleData).attr('fill', 'steelblue').attr('opacity', '50%').attr('d', area)
  }, [chartWidth, chartHeight, scaleX, scaleY])

  return (
    <div className="grid grid-cols-1 grid-rows-[auto_1fr]">
      <Text className="text-xs">CPU</Text>
      <div
        className="border-l-[0.5px] border-r-[0.5px] border-[#ddd]"
        ref={(ref) => {
          if (!ref) return

          setChartWidth(ref.clientWidth)
          setChartHeight(ref.clientHeight)
        }}
      >
        <div ref={divRef} />
      </div>
    </div>
  )
}

export default AreaChart

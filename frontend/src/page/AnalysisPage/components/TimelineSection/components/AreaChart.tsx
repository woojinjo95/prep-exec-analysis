import React, { useEffect, useRef, useState } from 'react'

import { Text } from '@chakra-ui/react'
import { sampleData } from '@page/AnalysisPage/components/TimelineSection/constant'
import { useScale } from '../hook'
import { AreaChartGenerator } from '../usecase'

/**
 * 영역 차트
 */
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

    const chart = new AreaChartGenerator(divRef.current, chartWidth, chartHeight, scaleX, scaleY)
    chart.createChart()
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

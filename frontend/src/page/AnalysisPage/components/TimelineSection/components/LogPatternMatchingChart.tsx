import { PointChart } from '@global/ui'
import React, { useMemo } from 'react'
import { useLogPatternMatching } from '../api/hook'

interface LogPatternMatchingChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * 패턴에 매칭된 로그(log pattern matching) 차트
 */
const LogPatternMatchingChart: React.FC<LogPatternMatchingChartProps> = ({ scaleX, startTime, endTime }) => {
  const { logPatternMatching } = useLogPatternMatching({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const logPatternMatchingData = useMemo(() => {
    if (!logPatternMatching) return null
    return logPatternMatching.map(({ timestamp }) => new Date(timestamp))
  }, [logPatternMatching])

  if (!logPatternMatchingData) return <div />
  return <PointChart scaleX={scaleX} data={logPatternMatchingData} />
}

export default React.memo(LogPatternMatchingChart)

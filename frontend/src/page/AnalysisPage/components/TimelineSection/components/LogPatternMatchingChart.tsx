import { scenarioIdState } from '@global/atom'
import { PointChart } from '@global/ui'
import React, { useMemo } from 'react'
import { useRecoilValue } from 'recoil'
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
  const scenarioId = useRecoilValue(scenarioIdState)
  const { logPatternMatching } = useLogPatternMatching({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    // FIXME: 동적으로 주입되도록 변경 필요
    testrun_id: '2023-08-14T054428F718593',
  })

  const logPatternMatchingData = useMemo(() => {
    if (!logPatternMatching) return null
    return logPatternMatching.map(({ timestamp }) => new Date(timestamp))
  }, [logPatternMatching])

  if (!logPatternMatchingData) return <div />
  return <PointChart scaleX={scaleX} data={logPatternMatchingData} />
}

export default LogPatternMatchingChart

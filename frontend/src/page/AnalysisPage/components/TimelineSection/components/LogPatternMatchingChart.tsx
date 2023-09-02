import { scenarioIdState, testRunIdState } from '@global/atom'
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
  const testRunId = useRecoilValue(testRunIdState)
  const { logPatternMatching } = useLogPatternMatching({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    testrun_id: testRunId || undefined,
  })

  const logPatternMatchingData = useMemo(() => {
    if (!logPatternMatching) return null
    return logPatternMatching.map(({ timestamp }) => new Date(timestamp))
  }, [logPatternMatching])

  if (!logPatternMatchingData) return <div />
  return <PointChart scaleX={scaleX} data={logPatternMatchingData} />
}

export default React.memo(LogPatternMatchingChart)

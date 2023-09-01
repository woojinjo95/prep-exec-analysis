import React, { useMemo } from 'react'
import { useRecoilValue } from 'recoil'
import { PointChart, RangeChart } from '@global/ui'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useFreeze } from '../api/hook'

interface FreezeChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * Video Analysis Result(freeze) 차트
 */
const FreezeChart: React.FC<FreezeChartProps> = ({ scaleX, startTime, endTime }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { freeze } = useFreeze({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    testrun_id: testRunId || undefined,
  })

  const freezeData = useMemo(() => {
    if (!freeze) return null
    return freeze.map(({ timestamp, duration }) => ({ date: new Date(timestamp), duration: duration * 1000 }))
  }, [freeze])

  if (!freezeData) return <div />
  return <RangeChart scaleX={scaleX} data={freezeData} color="blue" />
}

export default React.memo(FreezeChart)

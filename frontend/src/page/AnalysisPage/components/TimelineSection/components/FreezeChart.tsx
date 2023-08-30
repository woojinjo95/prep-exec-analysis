import { PointChart, RangeChart } from '@global/ui'
import React, { useMemo } from 'react'
import { scenarioIdState } from '@global/atom'
import { useRecoilValue } from 'recoil'
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
  const { freeze } = useFreeze({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    // FIXME: 동적으로 주입되도록 변경 필요
    testrun_id: '2023-08-14T054428F718593',
  })

  const freezeData = useMemo(() => {
    if (!freeze) return null
    return freeze.map(({ timestamp, duration }) => ({ date: new Date(timestamp), duration: duration * 1000 }))
  }, [freeze])

  if (!freezeData) return <div />
  return <RangeChart scaleX={scaleX} data={freezeData} color="blue" />
}

export default FreezeChart

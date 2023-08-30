import React, { useMemo } from 'react'
import { useRecoilValue } from 'recoil'
import { scenarioIdState } from '@global/atom'
import { PointChart, RangeChart } from '@global/ui'
import { RangeChartData } from '@global/types'
import { useBoot, useResume } from '../api/hook'

interface ResumeBootChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * Resume(warm booting), Boot(cold booting) 시간 차트
 */
const ResumeBootChart: React.FC<ResumeBootChartProps> = ({ scaleX, startTime, endTime }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const { resume } = useResume({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    // FIXME: 동적으로 주입되도록 변경 필요
    testrun_id: '2023-08-14T054428F718593',
  })
  const { boot } = useBoot({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    // FIXME: 동적으로 주입되도록 변경 필요
    testrun_id: '2023-08-14T054428F718593',
  })

  const data: RangeChartData | null = useMemo(() => {
    if (!resume || !boot) return null

    return [...resume, ...boot]
      .map(({ timestamp, measure_time }) => ({
        date: new Date(timestamp),
        duration: measure_time,
      }))
      .sort(({ date: aDate }, { date: bDate }) => (aDate.getTime() > bDate.getTime() ? 1 : 0))
  }, [resume, boot])

  if (!data) return <div />
  return <RangeChart scaleX={scaleX} data={data} color="green" />
}

export default ResumeBootChart

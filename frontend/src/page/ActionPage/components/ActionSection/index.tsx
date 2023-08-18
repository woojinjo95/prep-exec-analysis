import React, { useState } from 'react'

import { useScenarios } from '@global/api/hook'
import ActionBlockArea from './components/ActionBlockArea'
import BlockControls from './components/BlockControls'

/**
 * 액션 영역
 */
const ActionSection: React.FC = () => {
  // current scenarioId
  // TODO: 나중에 진입 시에 scenario_id를 받을 수 있어야함
  const [scenarioId, setScenarioId] = useState<string | null>(null)

  useScenarios({
    onSuccess: (res) => {
      if (res && res.items.length > 0) {
        setScenarioId(res.items[0].id)
      }
    },
    onError: (err) => {
      console.error(err)
    },
  })

  return (
    <section className="border border-black row-span-2 h-full grid grid-rows-[1fr_auto]">
      <ActionBlockArea scenarioId={scenarioId} />
      <BlockControls scenarioId={scenarioId} />
    </section>
  )
}

export default ActionSection

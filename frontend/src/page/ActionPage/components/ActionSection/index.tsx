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

  return (
    <section className="border border-black row-span-3 h-full grid grid-rows-[1fr_auto]">
      <ActionBlockArea />
      <BlockControls />
    </section>
  )
}

export default ActionSection

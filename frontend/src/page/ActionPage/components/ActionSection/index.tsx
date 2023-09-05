import React from 'react'

import ActionBlockArea from './components/ActionBlockArea'
import BlockControls from './components/BlockControls'

/**
 * 액션 영역
 */
const ActionSection: React.FC = () => {
  return (
    <section className="border border-black row-span-3 h-full grid grid-rows-[1fr_auto]">
      <ActionBlockArea />
      <BlockControls />
    </section>
  )
}

export default ActionSection

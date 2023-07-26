import React from 'react'

import ActionBlockArea from './components/ActionBlockArea'

/**
 * 액션 영역
 */
const ActionSection: React.FC = () => {
  return (
    <section className="border border-black row-span-2 h-full">
      <ActionBlockArea />
    </section>
  )
}

export default ActionSection

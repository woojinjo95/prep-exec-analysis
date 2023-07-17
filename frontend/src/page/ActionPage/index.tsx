import React from 'react'
import { PageContainer } from '@global/ui'
import ActionSection from './components/ActionSection'
import MonitorSection from './components/MonitorSection'
import RemoconSection from './components/RemoconSection'
import TerminalSection from './components/TerminalSection'

/**
 * 동작 제어 페이지
 */
const ActionPage: React.FC = () => {
  return (
    <PageContainer className="grid grid-cols-[1.5fr_3fr_1.5fr] grid-rows-[2fr_1.5fr]">
      <ActionSection />
      <MonitorSection />
      <RemoconSection />
      <TerminalSection />
    </PageContainer>
  )
}

export default ActionPage

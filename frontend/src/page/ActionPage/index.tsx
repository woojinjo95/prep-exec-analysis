import React, { useEffect, useState } from 'react'
import { PageContainer } from '@global/ui'

import ActionSection from './components/ActionSection'
import MonitorSection from './components/MonitorSection'
import RemoconSection from './components/RemoconSection'
import TerminalSection from './components/TerminalSection'
import ServiceStateSection from './components/ServiceStateSection'
import { KeyEvent } from './types'

/**
 * 동작 제어 페이지
 */
const ActionPage: React.FC = () => {
  const [keyEvent, setKeyEvent] = useState<KeyEvent | null>(null)

  useEffect(() => {
    const keyDownHandler = (e: KeyEvent) => {
      if (e.altKey) {
        setKeyEvent(e)
        e.preventDefault()
      }
    }

    const keyUpHandler = (e: KeyEvent) => {
      if (!e.altKey) {
        setKeyEvent(null)
        e.preventDefault()
      }
    }

    window.addEventListener('keydown', keyDownHandler)
    window.addEventListener('keyup', keyUpHandler)
    return () => {
      window.removeEventListener('keydown', keyDownHandler)
      window.removeEventListener('keyup', keyUpHandler)
    }
  }, [])

  return (
    <PageContainer className="grid grid-cols-[2fr_3fr_1.5fr] grid-rows-[57%_3%_40%]">
      <ActionSection />
      <MonitorSection />
      <RemoconSection keyEvent={keyEvent} />
      <ServiceStateSection />
      <TerminalSection />
    </PageContainer>
  )
}

export default ActionPage

import React, { useEffect, useState } from 'react'
import { PageContainer } from '@global/ui'
import ActionSection from './components/ActionSection'
import MonitorSection from './components/MonitorSection'
import RemoconSection from './components/RemoconSection'
import TerminalSection from './components/TerminalSection'
import { KeyEvent } from './constants'

/**
 * 동작 제어 페이지
 */
const ActionPage: React.FC = () => {
  const [event, setEvent] = useState<KeyEvent | null>(null)

  useEffect(() => {
    const keyDownHandler = (e: KeyEvent) => {
      if (e.altKey) {
        setEvent(e)
        e.preventDefault()
      }
    }

    const keyUpHandler = (e: KeyEvent) => {
      if (!e.altKey) {
        setEvent(null)
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
    <PageContainer className="grid grid-cols-[1.5fr_3fr_1.5fr] grid-rows-[60%_39%]">
      <ActionSection />
      <MonitorSection />
      <RemoconSection event={event} />
      <TerminalSection />
    </PageContainer>
  )
}

export default ActionPage

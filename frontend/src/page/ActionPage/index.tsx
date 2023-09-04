import React, { useEffect, useState } from 'react'
import { PageContainer } from '@global/ui'

import { useScenarioById } from '@global/api/hook'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState, scenarioIdState } from '@global/atom'
import { useWebsocket } from '@global/hook'
import { useNavigate } from 'react-router-dom'
import cx from 'classnames'
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
  const navigate = useNavigate()
  const [keyEvent, setKeyEvent] = useState<KeyEvent | null>(null)

  useEffect(() => {
    const keyDownHandler = (e: KeyboardEvent) => {
      if (e.repeat) return

      if (e.altKey) {
        setKeyEvent(e)
        e.preventDefault()
      }
    }

    const keyUpHandler = (e: KeyboardEvent) => {
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

  const scenarioId = useRecoilValue(scenarioIdState)

  const isBlockRecordMode = useRecoilValue(isBlockRecordModeState)

  const { sendMessage } = useWebsocket()

  const { scenario } = useScenarioById({
    scenarioId,
  })

  useEffect(() => {
    if (!scenarioId || scenario) {
      navigate('/', { replace: true })
    }

    sendMessage({ level: 'info', msg: 'action_mode' })
  }, [])

  return (
    <PageContainer
      className={cx('grid grid-cols-[2fr_3fr_1.5fr] grid-rows-[57%_3%_40%]', {
        'border-4 border-red': !!isBlockRecordMode,
      })}
    >
      <ActionSection />
      <MonitorSection />
      <RemoconSection keyEvent={keyEvent} />
      <ServiceStateSection />
      <TerminalSection />
    </PageContainer>
  )
}

export default ActionPage

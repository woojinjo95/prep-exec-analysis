import React from 'react'
import TerminalShell from '@global/ui/Terminal/TerminalShell'
import { Terminal } from '@global/types'
import { useSearchParams } from 'react-router-dom'

/**
 * Terminal pop up page
 */

const TerminalPage: React.FC = () => {
  const [searchParams] = useSearchParams()

  const currentTerminal: Terminal = {
    id: searchParams.get('id') as string,
    mode: searchParams.get('mode') as 'adb' | 'ssh',
  }

  return (
    <div className="w-full h-screen overflow-y-auto bg-black">
      {currentTerminal && <TerminalShell terminal={currentTerminal} currentTerminal={currentTerminal} />}
    </div>
  )
}

export default TerminalPage

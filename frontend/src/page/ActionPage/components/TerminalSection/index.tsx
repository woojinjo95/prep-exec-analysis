import { Tabs } from '@global/ui'
import React from 'react'

/**
 * 터미널 영역
 */
const TerminalSection: React.FC = () => {
  return (
    <section className="border border-black col-span-2">
      <Tabs header={['Settings & Controls', 'Terminal']} className="px-5 pb-5 pt-2" theme="dark">
        <div>
          <span>setting</span>
        </div>
        <div>
          <span>terminal</span>
        </div>
      </Tabs>
    </section>
  )
}

export default TerminalSection

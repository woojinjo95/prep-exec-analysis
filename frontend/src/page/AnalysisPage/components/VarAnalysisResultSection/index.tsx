import React from 'react'
import { Button, Tabs } from '@global/ui'
import useWebsocket from '@global/module/websocket'
import SetROIButton from './components/SetROIButton'

/**
 * 분석변수 설정 및 결과 영역
 */
const VarAnalysisResultSection: React.FC = () => {
  const { sendMessage } = useWebsocket()

  return (
    <section className="border-l border-[#37383E] row-span-3 bg-black text-white">
      <Tabs header={['Var/Analysis Results']} colorScheme="dark" className="pl-5 pr-1 py-1">
        <div>
          <SetROIButton />
          <Button
            colorScheme="primary"
            onClick={() => {
              sendMessage({
                msg: 'analysis',
                data: {
                  measurement: ['freeze'],
                },
              })
            }}
          >
            Analysis
          </Button>
          <video src="" />
        </div>
      </Tabs>
    </section>
  )
}

export default VarAnalysisResultSection

import React from 'react'
import { Button, OptionItem, Select } from '@global/ui'
import useWebsocket from '@global/module/websocket'
import { AnalysisTypeLabel } from '../../../constant'

interface HeaderProps {
  selectedAnalysisItems: (keyof typeof AnalysisTypeLabel)[]
  setSelectedAnalysisItems: React.Dispatch<React.SetStateAction<(keyof typeof AnalysisTypeLabel)[]>>
}

/**
 * 분석 아이템 설정 패널 헤더
 */
const Header: React.FC<HeaderProps> = ({ selectedAnalysisItems, setSelectedAnalysisItems }) => {
  const { sendMessage } = useWebsocket()

  return (
    <div className="flex gap-x-4 w-full">
      <Select colorScheme="dark" value="Add Item" className="grow">
        {Object.keys(AnalysisTypeLabel)
          .filter((type) => !selectedAnalysisItems.includes(type as keyof typeof AnalysisTypeLabel))
          .map((_analysisType) => {
            const analysisType = _analysisType as keyof typeof AnalysisTypeLabel

            return (
              <OptionItem
                colorScheme="dark"
                key={`set-analysis-items-${analysisType}`}
                onClick={() => {
                  setSelectedAnalysisItems((prev) =>
                    prev.find((type) => type === analysisType)
                      ? prev.filter((type) => type === analysisType)
                      : [...prev, analysisType],
                  )
                }}
              >
                {AnalysisTypeLabel[analysisType]}
              </OptionItem>
            )
          })}
      </Select>

      {/* TODO: 분석 시작 명령 전송 후 응답(analysis_response) 오기 전까지 로딩 표시 */}
      <Button
        colorScheme="primary"
        onClick={() => {
          sendMessage({
            msg: 'analysis',
            data: {
              measurement: selectedAnalysisItems,
            },
          })
        }}
      >
        Analysis
      </Button>
    </div>
  )
}

export default Header

import React from 'react'
import { Button, OptionItem, Select, Text } from '@global/ui'
import { AnalysisService } from '@global/service'
import { useServiceState } from '@global/api/hook'
import { AnalysisTypeLabel, ConfigurableAnalysisTypes } from '../../../constant'

interface HeaderProps {
  selectedAnalysisItems: (keyof typeof AnalysisTypeLabel)[]
  setSelectedAnalysisItems: React.Dispatch<React.SetStateAction<(keyof typeof AnalysisTypeLabel)[]>>
}

/**
 * 분석 아이템 설정 패널 헤더
 */
const Header: React.FC<HeaderProps> = ({ selectedAnalysisItems, setSelectedAnalysisItems }) => {
  const { serviceState } = useServiceState()

  return (
    <div className="flex gap-x-4 w-full">
      <Select
        colorScheme="dark"
        header={
          <Text weight="bold" colorScheme="light">
            Add Item
          </Text>
        }
        className="grow"
      >
        {ConfigurableAnalysisTypes.filter((type) => !selectedAnalysisItems.includes(type)).map((analysisType) => (
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
        ))}
      </Select>

      {/* TODO: 분석 시작 명령 전송 후 응답(analysis_response) 오기 전까지 로딩 표시 */}
      <Button
        colorScheme="primary"
        disabled={serviceState === 'analysis'}
        onClick={() => {
          AnalysisService.startAnalysis({ msg: 'analysis' })
        }}
      >
        Analysis
      </Button>
    </div>
  )
}

export default Header

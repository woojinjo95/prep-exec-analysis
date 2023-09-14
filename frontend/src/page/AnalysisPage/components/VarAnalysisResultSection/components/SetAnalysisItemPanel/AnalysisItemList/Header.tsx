import React, { useState } from 'react'
import { Button, OptionItem, Select, Text } from '@global/ui'
import { AnalysisService } from '@global/service'
import { useServiceState } from '@global/api/hook'
import { useObservableState } from '@global/hook'
import { AnalysisTypeLabel, AnalyzableTypes } from '@global/constant'

interface HeaderProps {
  selectedAnalysisItems: (typeof AnalyzableTypes)[number][]
  setSelectedAnalysisItems: React.Dispatch<React.SetStateAction<(typeof AnalyzableTypes)[number][]>>
}

/**
 * 분석 아이템 설정 패널 헤더
 */
const Header: React.FC<HeaderProps> = ({ selectedAnalysisItems, setSelectedAnalysisItems }) => {
  const [isStartAnalysis, setIsStartAnalysis] = useState<boolean>(false)
  const { serviceState } = useServiceState({
    onSuccess: (state) => {
      if (isStartAnalysis && state !== 'analysis') {
        setIsStartAnalysis(false)
      }
    },
  })

  useObservableState({
    obs$: AnalysisService.onAnalysis$(),
    callback: (state) => {
      if (state?.msg !== 'not_validate_analysis') return
      setIsStartAnalysis(false)
    },
  })

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
        {AnalyzableTypes.filter((type) => !selectedAnalysisItems.includes(type)).map((analysisType) => (
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

      <Button
        colorScheme="primary"
        disabled={isStartAnalysis || serviceState === 'analysis' || serviceState === 'recording'}
        onClick={() => {
          AnalysisService.startAnalysis({ msg: 'analysis' })
          setIsStartAnalysis(true)
        }}
      >
        Analysis
      </Button>
    </div>
  )
}

export default Header

import React from 'react'
import { DropdownWithMoreButton, OptionItem, Text } from '@global/ui'
import { AnalysisConfig } from '@page/AnalysisPage/components/VarAnalysisResultSection/api/entity'

interface LogPatternProps {
  logPattern: NonNullable<AnalysisConfig['log_pattern_matching']>['items'][number]
}

/**
 * 단일 로그 패턴 컴포넌트
 */
const LogPattern: React.FC<LogPatternProps> = ({ logPattern }) => {
  return (
    <div className="flex justify-between items-center">
      <div className="flex gap-x-3 items-center">
        <div className="w-4 h-4" style={{ backgroundColor: logPattern.color }} />
        <Text size="sm" weight="medium">
          {logPattern.name}
        </Text>
      </div>

      {/* TODO: 수정 모달, 삭제 기능 */}
      <DropdownWithMoreButton colorScheme="charcoal" type="icon">
        <OptionItem colorScheme="charcoal">Modify</OptionItem>
        <OptionItem colorScheme="charcoal">Delete</OptionItem>
      </DropdownWithMoreButton>
    </div>
  )
}

export default LogPattern

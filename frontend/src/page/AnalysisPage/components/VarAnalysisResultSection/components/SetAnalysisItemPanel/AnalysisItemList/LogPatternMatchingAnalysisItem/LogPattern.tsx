import React, { useState } from 'react'
import { DropdownWithMoreButton, OptionItem, Text } from '@global/ui'
import { AnalysisConfig } from '@page/AnalysisPage/api/entity'
import { UnsavedAnalysisConfig } from '@page/AnalysisPage/components/VarAnalysisResultSection/types'
import LogPatternModal from './LogPatternModal'

interface LogPatternProps {
  logPattern: NonNullable<AnalysisConfig['log_pattern_matching']>['items'][number]
  patterns: NonNullable<UnsavedAnalysisConfig['log_pattern_matching']>['items']
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * 단일 로그 패턴 컴포넌트
 */
const LogPattern: React.FC<LogPatternProps> = ({ logPattern, patterns, setUnsavedAnalysisConfig }) => {
  const [isOpenModifyLogPatternModal, setIsOpenModifyLogPatternModal] = useState<boolean>(false)

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
        <OptionItem colorScheme="charcoal" onClick={() => setIsOpenModifyLogPatternModal(true)}>
          Modify
        </OptionItem>
        <OptionItem
          colorScheme="charcoal"
          onClick={() =>
            setUnsavedAnalysisConfig((prev) => ({
              ...prev,
              log_pattern_matching: {
                ...prev.log_pattern_matching!,
                items: prev.log_pattern_matching!.items.filter((p) => p.name !== logPattern.name),
              },
            }))
          }
        >
          Delete
        </OptionItem>
      </DropdownWithMoreButton>

      {isOpenModifyLogPatternModal && (
        <LogPatternModal
          isOpen={isOpenModifyLogPatternModal}
          close={() => setIsOpenModifyLogPatternModal(false)}
          patterns={patterns}
          pattern={logPattern}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
        />
      )}
    </div>
  )
}

export default LogPattern

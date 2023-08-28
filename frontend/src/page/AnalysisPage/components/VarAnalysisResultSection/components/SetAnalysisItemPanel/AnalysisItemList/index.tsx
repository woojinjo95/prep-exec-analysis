import React, { useCallback, useState } from 'react'
import { Title } from '@global/ui'

import { AnalysisTypeLabel } from '../../../constant'
import FreezeAnalysisItem from './FreezeAnalysisItem'
import BootAnalysisItem from './BootAnalysisItem'
import ResumeAnalysisItem from './ResumeAnalysisItem'
import ChannelChangeTimeAnalysisItem from './ChannelChangeTimeAnalysisItem'
import LogLevelFinderAnalysisItem from './LogLevelFinderAnalysisItem'
import LogPatternMatchingAnalysisItem from './LogPatternMatchingAnalysisItem'
import { useAnalysisConfig } from '../../../api/hook'
import { UnsavedAnalysisConfig } from '../../../types'

interface AnalysisItemListProps {
  selectedAnalysisItems: (keyof typeof AnalysisTypeLabel)[]
  setSelectedAnalysisItems: React.Dispatch<React.SetStateAction<(keyof typeof AnalysisTypeLabel)[]>>
}

/**
 * 분석 아이템 리스트
 */
const AnalysisItemList: React.FC<AnalysisItemListProps> = ({ selectedAnalysisItems, setSelectedAnalysisItems }) => {
  const [unsavedAnalysisConfig, setUnsavedAnalysisConfig] = useState<UnsavedAnalysisConfig>({})
  const { analysisConfig } = useAnalysisConfig({
    onSuccess: (data) => {
      setUnsavedAnalysisConfig(data)
    },
  })

  const onClickDeleteItem = useCallback(
    (type: keyof typeof AnalysisTypeLabel) => () => {
      setSelectedAnalysisItems((prev) => prev.filter((_type) => _type !== type))
    },
    [],
  )

  if (!selectedAnalysisItems.length) {
    return (
      <div className="w-full h-full flex justify-center items-center">
        <Title colorScheme="light" as="h2">
          Please add items to be analyzed.
        </Title>
      </div>
    )
  }

  if (!analysisConfig) return <div />
  return (
    <div className="overflow-y-auto flex flex-col gap-y-1">
      {selectedAnalysisItems.includes('freeze') && (
        <FreezeAnalysisItem
          duration={unsavedAnalysisConfig.freeze?.duration}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('freeze')}
        />
      )}

      {selectedAnalysisItems.includes('resume') && (
        <ResumeAnalysisItem onClickDeleteItem={onClickDeleteItem('resume')} />
      )}

      {selectedAnalysisItems.includes('boot') && <BootAnalysisItem onClickDeleteItem={onClickDeleteItem('boot')} />}

      {selectedAnalysisItems.includes('channel_change_time') && (
        <ChannelChangeTimeAnalysisItem onClickDeleteItem={onClickDeleteItem('channel_change_time')} />
      )}

      {selectedAnalysisItems.includes('log_level_finder') && (
        <LogLevelFinderAnalysisItem onClickDeleteItem={onClickDeleteItem('log_level_finder')} />
      )}

      {selectedAnalysisItems.includes('log_pattern_matching') && (
        <LogPatternMatchingAnalysisItem onClickDeleteItem={onClickDeleteItem('log_pattern_matching')} />
      )}
    </div>
  )
}

export default AnalysisItemList

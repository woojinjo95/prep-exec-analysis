import React, { useCallback, useState } from 'react'
import { Title } from '@global/ui'

import FreezeAnalysisItem from './FreezeAnalysisItem'
import BootAnalysisItem from './BootAnalysisItem'
import ResumeAnalysisItem from './ResumeAnalysisItem'
import ChannelChangeTimeAnalysisItem from './ChannelChangeTimeAnalysisItem'
import LogLevelFinderAnalysisItem from './LogLevelFinderAnalysisItem'
import LogPatternMatchingAnalysisItem from './LogPatternMatchingAnalysisItem'
import { AnalysisTypeLabel } from '../../../constant'
import { useAnalysisConfig } from '../../../api/hook'
import { UnsavedAnalysisConfig } from '../../../types'
import LoudnessAnalysisItem from './LoudnessAnalysisItem'

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

      {selectedAnalysisItems.includes('loudness') && (
        <LoudnessAnalysisItem onClickDeleteItem={onClickDeleteItem('loudness')} />
      )}

      {selectedAnalysisItems.includes('resume') && (
        <ResumeAnalysisItem
          resumeType={unsavedAnalysisConfig.resume?.type}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('resume')}
        />
      )}

      {selectedAnalysisItems.includes('boot') && (
        <BootAnalysisItem
          bootType={unsavedAnalysisConfig.boot?.type}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('boot')}
        />
      )}

      {selectedAnalysisItems.includes('channel_change_time') && (
        <ChannelChangeTimeAnalysisItem
          isCheckedAdjointChannel={unsavedAnalysisConfig.channel_change_time?.targets?.includes('adjoint_channel')}
          isCheckedNonadjointChannel={unsavedAnalysisConfig.channel_change_time?.targets?.includes(
            'nonadjoint_channel',
          )}
          onClickDeleteItem={onClickDeleteItem('channel_change_time')}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
        />
      )}

      {selectedAnalysisItems.includes('log_level_finder') && (
        <LogLevelFinderAnalysisItem
          targets={unsavedAnalysisConfig.log_level_finder?.targets}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('log_level_finder')}
        />
      )}

      {selectedAnalysisItems.includes('log_pattern_matching') && (
        <LogPatternMatchingAnalysisItem onClickDeleteItem={onClickDeleteItem('log_pattern_matching')} />
      )}
    </div>
  )
}

export default AnalysisItemList

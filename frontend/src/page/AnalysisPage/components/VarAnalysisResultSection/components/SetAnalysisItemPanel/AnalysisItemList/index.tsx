import React, { useCallback, useEffect, useState } from 'react'
import { Title } from '@global/ui'

import { AnalysisTypeLabel } from '../../../constant'
import { useAnalysisConfig } from '../../../api/hook'
import { UnsavedAnalysisConfig } from '../../../types'
import FreezeAnalysisItem from './FreezeAnalysisItem'
import BootAnalysisItem from './BootAnalysisItem'
import ResumeAnalysisItem from './ResumeAnalysisItem'
import ChannelChangeTimeAnalysisItem from './ChannelChangeTimeAnalysisItem'
import LogLevelFinderAnalysisItem from './LogLevelFinderAnalysisItem'
import LogPatternMatchingAnalysisItem from './LogPatternMatchingAnalysisItem'
import LoudnessAnalysisItem from './LoudnessAnalysisItem'

const DefaultAnalysisConfig: Required<UnsavedAnalysisConfig> = {
  freeze: {
    color: '#42FF00',
    duration: 3,
  },
  loudness: {
    color: '#0106FF',
  },
  resume: {
    color: '#F88686',
    type: 'image_matching',
    frame: undefined,
  },
  boot: {
    color: '#97A442',
    type: 'image_matching',
    frame: undefined,
  },
  channel_change_time: {
    color: '#8242A7',
    targets: [],
  },
  log_level_finder: {
    color: '#FF9900',
    targets: [],
  },
  log_pattern_matching: {
    color: '#E93535',
    items: [],
  },
}

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

  useEffect(() => {
    if (!selectedAnalysisItems.length) return

    // 분석아이템을 추가할 경우 -> 아이템별 default값 설정
    Object.keys(AnalysisTypeLabel).forEach((_type) => {
      const type = _type as keyof typeof AnalysisTypeLabel
      // 분석 아이템 리스트에 없거나 이미 값이 있을 경우 -> escape
      if (!selectedAnalysisItems.includes(type) || unsavedAnalysisConfig[type]) return

      // redis 분석설정(analysisConfig)이 있을 경우 -> 해당 config로 설정
      if (analysisConfig?.[type]) {
        setUnsavedAnalysisConfig((prev) => ({
          ...prev,
          [type]: analysisConfig[type],
        }))
        return
      }

      // redis 분석설정(analysisConfig)이 없을 경우 -> default config로 설정
      setUnsavedAnalysisConfig((prev) => ({
        ...prev,
        [type]: DefaultAnalysisConfig[type],
      }))
    })
  }, [selectedAnalysisItems, analysisConfig])

  /**
   * 분석 아이템 삭제
   */
  const onClickDeleteItem = useCallback(
    (type: keyof typeof AnalysisTypeLabel) => () => {
      setSelectedAnalysisItems((prev) => prev.filter((_type) => _type !== type))
      setUnsavedAnalysisConfig((prev) => ({
        ...prev,
        [type]: undefined,
      }))
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
      {selectedAnalysisItems.includes('freeze') && unsavedAnalysisConfig.freeze && (
        <FreezeAnalysisItem
          color={unsavedAnalysisConfig.freeze.color}
          duration={unsavedAnalysisConfig.freeze.duration}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('freeze')}
        />
      )}

      {selectedAnalysisItems.includes('loudness') && unsavedAnalysisConfig.loudness && (
        <LoudnessAnalysisItem onClickDeleteItem={onClickDeleteItem('loudness')} />
      )}

      {selectedAnalysisItems.includes('resume') && unsavedAnalysisConfig.resume && (
        <ResumeAnalysisItem
          resumeType={unsavedAnalysisConfig.resume.type}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('resume')}
        />
      )}

      {selectedAnalysisItems.includes('boot') && unsavedAnalysisConfig.boot && (
        <BootAnalysisItem bootType={unsavedAnalysisConfig.boot.type} onClickDeleteItem={onClickDeleteItem('boot')} />
      )}

      {selectedAnalysisItems.includes('channel_change_time') && unsavedAnalysisConfig.channel_change_time && (
        <ChannelChangeTimeAnalysisItem
          targets={unsavedAnalysisConfig.channel_change_time.targets}
          onClickDeleteItem={onClickDeleteItem('channel_change_time')}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
        />
      )}

      {selectedAnalysisItems.includes('log_level_finder') && unsavedAnalysisConfig.log_level_finder && (
        <LogLevelFinderAnalysisItem
          targets={unsavedAnalysisConfig.log_level_finder.targets}
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

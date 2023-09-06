import React, { useCallback, useEffect, useState } from 'react'
import { Title } from '@global/ui'
import { AnalysisService } from '@global/service'
import { useObservableState, useWebsocket } from '@global/hook'
import { AnalysisType, AnalyzableType, AnalyzableTypes } from '@global/constant'

import { useAnalysisConfig } from '@page/AnalysisPage/api/hook'
import { AnalysisConfig } from '@page/AnalysisPage/api/entity'
import { AnalysisTypeLabel } from '../../../constant'
import { useRemoveAnalysisConfig, useUpdateAnalysisConfig } from '../../../api/hook'
import { UnsavedAnalysisConfig } from '../../../types'
import FreezeAnalysisItem from './FreezeAnalysisItem'
import BootAnalysisItem from './BootAnalysisItem'
import ResumeAnalysisItem from './ResumeAnalysisItem'
// import ChannelChangeTimeAnalysisItem from './ChannelChangeTimeAnalysisItem'
import LogLevelFinderAnalysisItem from './LogLevelFinderAnalysisItem'
import LogPatternMatchingAnalysisItem from './LogPatternMatchingAnalysisItem'
// import LoudnessAnalysisItem from './LoudnessAnalysisItem'

const DefaultAnalysisConfig: Required<UnsavedAnalysisConfig> = {
  freeze: {
    color: '#42FF00',
    duration: '3',
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
  const { sendMessage } = useWebsocket()
  const [unsavedAnalysisConfig, setUnsavedAnalysisConfig] = useState<UnsavedAnalysisConfig>({})
  const [warningMessage, setWarningMessage] = useState<{ [key in keyof typeof AnalysisType]?: string }>({})
  const { analysisConfig, refetch } = useAnalysisConfig({
    onSuccess: (data) => {
      if (Object.keys(unsavedAnalysisConfig).length) return

      // 처음 페이지에 진입했을 경우
      setSelectedAnalysisItems(
        Object.keys(data).filter((key) => !!data[key as keyof AnalysisConfig]) as (keyof AnalysisConfig)[],
      )
      setUnsavedAnalysisConfig(() => ({
        ...data,
        freeze: data.freeze
          ? {
              ...data.freeze,
              duration: String(data.freeze.duration),
            }
          : undefined,
      }))
    },
  })

  const { updateAnalysisConfig } = useUpdateAnalysisConfig({
    onSuccess: (_, config) => {
      if (!Object.keys(config).length) return

      const measurement = Object.keys(config).filter(
        (type) => AnalyzableTypes.includes(type as AnalyzableType) && !!config[type as AnalyzableType],
      ) as AnalyzableType[]

      // 설정한 분석아이템이 없을 경우
      if (!measurement.length) return

      // 분석 설정 수정에 성공하면 -> 분석 시작 메시지 전송
      sendMessage({
        msg: 'analysis',
        data: {
          measurement,
        },
      })
    },
  })

  const { removeAnalysisConfig } = useRemoveAnalysisConfig({
    onSuccess: (_, { analysis_type }) => {
      setSelectedAnalysisItems((prev) => prev.filter((type) => type !== analysis_type))
      setUnsavedAnalysisConfig((prev) => ({
        ...prev,
        [analysis_type]: undefined,
      }))
      setWarningMessage((prev) => ({
        ...prev,
        [analysis_type]: undefined,
      }))
      refetch()
    },
  })

  /**
   * 분석 아이템 삭제
   */
  const onClickDeleteItem = useCallback(
    (type: keyof typeof AnalysisTypeLabel): React.MouseEventHandler<SVGSVGElement> =>
      (e) => {
        e.stopPropagation()
        removeAnalysisConfig(type)
      },
    [],
  )

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

      // TODO: Remember current setting으로 설정된 경우 -> localstorage에 저장된 설정값으로 설정

      // default config로 설정
      setUnsavedAnalysisConfig((prev) => ({
        ...prev,
        [type]: DefaultAnalysisConfig[type],
      }))
    })
  }, [selectedAnalysisItems, analysisConfig])

  useObservableState({
    obs$: AnalysisService.onAnalysis$(),
    callback: (state) => {
      let isValid = false
      if (state?.msg !== 'analysis') return

      // 로그 패턴을 하나도 추가하지 않은 경우
      if (unsavedAnalysisConfig.log_pattern_matching && !unsavedAnalysisConfig.log_pattern_matching.items.length) {
        setWarningMessage((prev) => ({ ...prev, log_pattern_matching: 'Please set log pattern.' }))
        isValid = true
      } else {
        setWarningMessage((prev) => ({ ...prev, log_pattern_matching: undefined }))
      }

      // 로그레벨을 하나도 선택하지 않은 경우
      if (unsavedAnalysisConfig.log_level_finder && !unsavedAnalysisConfig.log_level_finder.targets.length) {
        setWarningMessage((prev) => ({ ...prev, log_level_finder: 'Please select log level.' }))
        isValid = true
      } else {
        setWarningMessage((prev) => ({ ...prev, log_level_finder: undefined }))
      }

      // boot frame을 설정하지 않은 경우
      if (
        unsavedAnalysisConfig.boot &&
        unsavedAnalysisConfig.boot.type === 'image_matching' &&
        !unsavedAnalysisConfig.boot.frame
      ) {
        setWarningMessage((prev) => ({ ...prev, boot: 'Please set ROI.' }))
        isValid = true
      } else {
        setWarningMessage(({ ...prev }) => ({ ...prev, boot: undefined }))
      }

      // resume frame을 설정하지 않은 경우
      if (
        unsavedAnalysisConfig.resume &&
        unsavedAnalysisConfig.resume.type === 'image_matching' &&
        !unsavedAnalysisConfig.resume.frame
      ) {
        setWarningMessage((prev) => ({ ...prev, resume: 'Please set ROI.' }))
        isValid = true
      } else {
        setWarningMessage(({ ...prev }) => ({ ...prev, resume: undefined }))
      }

      if (isValid) return

      updateAnalysisConfig({
        ...(unsavedAnalysisConfig as AnalysisConfig),
        freeze: unsavedAnalysisConfig.freeze
          ? {
              ...unsavedAnalysisConfig.freeze,
              duration: Number(unsavedAnalysisConfig.freeze.duration),
            }
          : undefined,
      })
    },
  })

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

      {/* {selectedAnalysisItems.includes('loudness') && unsavedAnalysisConfig.loudness && (
        <LoudnessAnalysisItem
          color={unsavedAnalysisConfig.loudness.color}
          onClickDeleteItem={onClickDeleteItem('loudness')}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
        />
      )} */}

      {selectedAnalysisItems.includes('resume') && unsavedAnalysisConfig.resume && (
        <ResumeAnalysisItem
          color={unsavedAnalysisConfig.resume.color}
          frame={unsavedAnalysisConfig.resume.frame}
          resumeType={unsavedAnalysisConfig.resume.type}
          warningMessage={warningMessage.resume}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('resume')}
        />
      )}

      {selectedAnalysisItems.includes('boot') && unsavedAnalysisConfig.boot && (
        <BootAnalysisItem
          color={unsavedAnalysisConfig.boot.color}
          frame={unsavedAnalysisConfig.boot.frame}
          bootType={unsavedAnalysisConfig.boot.type}
          warningMessage={warningMessage.boot}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('boot')}
        />
      )}

      {/* {selectedAnalysisItems.includes('channel_change_time') && unsavedAnalysisConfig.channel_change_time && (
        <ChannelChangeTimeAnalysisItem
          color={unsavedAnalysisConfig.channel_change_time.color}
          targets={unsavedAnalysisConfig.channel_change_time.targets}
          onClickDeleteItem={onClickDeleteItem('channel_change_time')}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
        />
      )} */}

      {selectedAnalysisItems.includes('log_level_finder') && unsavedAnalysisConfig.log_level_finder && (
        <LogLevelFinderAnalysisItem
          color={unsavedAnalysisConfig.log_level_finder.color}
          targets={unsavedAnalysisConfig.log_level_finder.targets}
          warningMessage={warningMessage.log_level_finder}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('log_level_finder')}
        />
      )}

      {selectedAnalysisItems.includes('log_pattern_matching') && unsavedAnalysisConfig.log_pattern_matching && (
        <LogPatternMatchingAnalysisItem
          color={unsavedAnalysisConfig.log_pattern_matching.color}
          patterns={unsavedAnalysisConfig.log_pattern_matching.items}
          warningMessage={warningMessage.log_pattern_matching}
          setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          onClickDeleteItem={onClickDeleteItem('log_pattern_matching')}
        />
      )}
    </div>
  )
}

export default AnalysisItemList

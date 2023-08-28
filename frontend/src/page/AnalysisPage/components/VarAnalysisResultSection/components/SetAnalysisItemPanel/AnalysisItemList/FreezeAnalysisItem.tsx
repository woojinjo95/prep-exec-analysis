import React, { useCallback, useEffect, useState } from 'react'
import { Accordion, Checkbox, Input, OptionItem, Select, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'
import { UnsavedAnalysisConfig } from '../../../types'

const DurationUnits = ['Sec', 'Min'] as const

interface FreezeAnalysisItemProps {
  duration?: number
  onClickDeleteItem: () => void
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * freeze 분석 아이템
 */
const FreezeAnalysisItem: React.FC<FreezeAnalysisItemProps> = ({
  duration: defaultDuration,
  onClickDeleteItem,
  setUnsavedAnalysisConfig,
}) => {
  const [duration, setDuration] = useState<string>('3')
  const [durationUnit, setDurationUnit] = useState<'Sec' | 'Min'>('Sec')
  const [isRememberChecked, setIsRememberChecked] = useState<boolean>(false)

  useEffect(() => {
    if (!defaultDuration || defaultDuration > 60 * 60 || defaultDuration < 0) {
      setDuration('3')
      setDurationUnit('Sec')
      return
    }

    if (defaultDuration > 60) {
      setDuration(String(Math.floor(defaultDuration % 60)))
      setDurationUnit('Min')
      return
    }

    setDuration(String(defaultDuration))
    setDurationUnit('Sec')
  }, [defaultDuration])

  const onChangeDuration: React.ChangeEventHandler<HTMLInputElement> = useCallback((e) => {
    const { value } = e.target

    if (Number.isNaN(value)) return

    if (value.length > 1 && value.charAt(0) === '0') {
      setUnsavedAnalysisConfig((prev) => ({
        ...prev,
        freeze: {
          ...prev.freeze,
          duration: Number(value.slice(1)),
        },
      }))
      setDuration(value.slice(1))
      return
    }

    if (Number(value) > 60) {
      setDuration('60')
      return
    }
    if (Number(value) < 1) {
      setDuration('1')
      return
    }

    setDuration(value)
  }, [])

  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.freeze}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-5">
        <div className="grid grid-rows-1 grid-cols-[3fr_1.5fr_2.5fr] gap-x-1 items-center">
          <Text colorScheme="light" weight="medium">
            Duration
          </Text>
          <Input colorScheme="charcoal" placeholder="3" value={duration} onChange={onChangeDuration} />
          <Select colorScheme="charcoal" value={durationUnit}>
            {DurationUnits.map((unit) => (
              <OptionItem
                colorScheme="charcoal"
                key={`freeze-analysis-item-duration-unit-${unit}`}
                onClick={() => setDurationUnit(unit)}
                isActive={durationUnit === unit}
              >
                {unit}
              </OptionItem>
            ))}
          </Select>
        </div>

        {/* TODO: local storage에 저장 */}
        <Checkbox
          colorScheme="light"
          isChecked={isRememberChecked}
          label="Remember current settings"
          onClick={(isChecked) => setIsRememberChecked(isChecked)}
        />
      </div>
    </Accordion>
  )
}

export default FreezeAnalysisItem

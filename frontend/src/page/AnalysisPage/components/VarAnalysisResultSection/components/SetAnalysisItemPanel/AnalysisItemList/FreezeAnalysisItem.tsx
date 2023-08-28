import React, { useCallback, useEffect, useMemo, useState } from 'react'
import { Accordion, Checkbox, ColorPickerBox, Input, OptionItem, Select, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'
import { UnsavedAnalysisConfig } from '../../../types'

const DurationUnits = ['Sec', 'Min'] as const

interface FreezeAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['freeze']>['color']
  duration: NonNullable<UnsavedAnalysisConfig['freeze']>['duration']
  onClickDeleteItem: () => void
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * freeze 분석 아이템
 */
const FreezeAnalysisItem: React.FC<FreezeAnalysisItemProps> = ({
  color,
  duration,
  onClickDeleteItem,
  setUnsavedAnalysisConfig,
}) => {
  const [durationUnit, setDurationUnit] = useState<'Sec' | 'Min'>(Number(duration) > 60 ? 'Min' : 'Sec')
  const [isRememberChecked, setIsRememberChecked] = useState<boolean>(false)

  const displayDuration = useMemo(() => {
    if (!duration) return ''

    if (Number(duration) > 60) return String(Math.floor(Number(duration) % 60))

    return String(Number(duration))
  }, [duration])

  const setDuration = useCallback((_duration: string) => {
    setUnsavedAnalysisConfig((prev) => ({
      ...prev,
      freeze: {
        ...prev.freeze!,
        duration: _duration,
      },
    }))
  }, [])

  useEffect(() => {
    if (Number(duration) > 60 * 60 || Number(duration) < 0) {
      setDuration('3')
      return
    }

    if (Number(duration) > 60) {
      setDurationUnit('Min')
      return
    }

    setDurationUnit('Sec')
  }, [duration])

  const onChangeDuration: React.ChangeEventHandler<HTMLInputElement> = useCallback((e) => {
    const { value } = e.target

    if (Number.isNaN(Number(value))) return

    if (!value.length) {
      setDuration('')
      return
    }

    if (value.length > 1 && value.charAt(0) === '0') {
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
          <div className="flex items-center gap-x-3">
            <ColorPickerBox
              color={color}
              onChange={(newColor) => {
                setUnsavedAnalysisConfig((prev) => ({
                  ...prev,
                  freeze: {
                    ...prev.freeze!,
                    color: newColor,
                  },
                }))
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.freeze}
            </Text>
          </div>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-5">
        <div className="grid grid-rows-1 grid-cols-[3fr_1.5fr_2.5fr] gap-x-1 items-center">
          <Text colorScheme="light" weight="medium">
            Duration
          </Text>
          <Input colorScheme="charcoal" placeholder="3" value={displayDuration} onChange={onChangeDuration} />
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

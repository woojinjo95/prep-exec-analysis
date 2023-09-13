import React, { useCallback } from 'react'
import { Accordion, Checkbox, ColorPickerBox, Input, OptionItem, Select, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisType } from '@global/constant'
import { AnalysisTypeLabel } from '../../../constant'
import { UnsavedAnalysisConfig } from '../../../types'

const DurationUnits = ['Sec', 'Min'] as const

interface FreezeAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['freeze']>['color']
  duration: NonNullable<UnsavedAnalysisConfig['freeze']>['duration']
  unit: NonNullable<UnsavedAnalysisConfig['freeze']>['unit']
  warningMessage?: string
  onClickDeleteItem: React.MouseEventHandler<SVGSVGElement>
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
  isRememberChecked: boolean
  setIsRememberedConfig: React.Dispatch<React.SetStateAction<{ [key in keyof typeof AnalysisType]?: boolean }>>
}

/**
 * freeze 분석 아이템
 */
const FreezeAnalysisItem: React.FC<FreezeAnalysisItemProps> = ({
  color,
  duration,
  unit,
  warningMessage,
  onClickDeleteItem,
  setUnsavedAnalysisConfig,
  isRememberChecked,
  setIsRememberedConfig,
}) => {
  const setDuration = useCallback((_duration: string) => {
    setUnsavedAnalysisConfig((prev) => ({
      ...prev,
      freeze: {
        ...prev.freeze!,
        duration: _duration,
      },
    }))
  }, [])

  const setDurationUnit = useCallback((_unit: typeof unit) => {
    setUnsavedAnalysisConfig((prev) => ({
      ...prev,
      freeze: {
        ...prev.freeze!,
        unit: _unit,
      },
    }))
  }, [])

  return (
    <Accordion
      warningMessage={warningMessage}
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
          <Input
            colorScheme="charcoal"
            placeholder="3"
            type="number"
            value={duration}
            onChange={(e) => {
              if (
                e.target.value.length > 1 &&
                e.target.value.slice(0, 1) === '0' &&
                e.target.value.slice(1, 2) !== '.'
              ) {
                setDuration(e.target.value.slice(1, e.target.value.length))
                return
              }
              setDuration(e.target.value)
            }}
          />
          <Select
            colorScheme="charcoal"
            header={
              <Text weight="bold" colorScheme="light">
                {unit}
              </Text>
            }
          >
            {DurationUnits.map((_unit) => (
              <OptionItem
                colorScheme="charcoal"
                key={`freeze-analysis-item-duration-unit-${_unit}`}
                onClick={() => setDurationUnit(_unit)}
                isActive={unit === _unit}
              >
                {_unit}
              </OptionItem>
            ))}
          </Select>
        </div>

        <Checkbox
          colorScheme="light"
          isChecked={isRememberChecked}
          label="Remember current settings"
          onClick={(isChecked) => setIsRememberedConfig((prev) => ({ ...prev, freeze: isChecked }))}
        />
      </div>
    </Accordion>
  )
}

export default FreezeAnalysisItem

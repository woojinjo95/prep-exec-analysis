import { Button, Input, Modal, OptionItem, Select, Text, ToggleButton } from '@global/ui'
import React, { useEffect, useRef, useState } from 'react'
import { useHardwareConfiguration, useScenarioById } from '@global/api/hook'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, selectedRemoconNameState } from '@global/atom'
import { useMutation } from 'react-query'
import { TimeUnit } from '../types'
import { profiles, timeUnit } from '../constants'
import { postBlock } from '../api/func'

interface AddIntelligentMonkeyTestBlockModalProps {
  isOpen: boolean
  close: () => void
}
const AddIntelligentMonkeyTestBlockModal: React.FC<AddIntelligentMonkeyTestBlockModalProps> = ({ isOpen, close }) => {
  const [profile, setProfile] = useState<'Roku' | 'SKB'>('Roku')

  const [duration, setDuration] = useState<number>(60)
  const [durationTimeUnit, setDurationTimeUnit] = useState<Extract<TimeUnit, 'Sec' | 'Min'>>('Sec')

  const [interval, setInterval] = useState<number>(1)
  const [intervalTimeUnit, setIntervalTimeUnit] = useState<Extract<TimeUnit, 'Sec' | 'ms'>>('Sec')

  const [isSmartSense, setIsSmartSense] = useState<boolean>(false)

  const [waitingTime, setWaitingTime] = useState<number>(5)
  const [waitingTimeTimeUnit, setWaitingTimeTimeUnit] = useState<Extract<TimeUnit, 'Sec' | 'Min'>>('Sec')

  const firstFocusableElementRef = useRef<HTMLButtonElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  const scenarioId = useRecoilValue(scenarioIdState)

  const { refetch } = useScenarioById({ scenarioId })

  const { mutate: postBlockMutate } = useMutation(postBlock, {
    onSuccess: () => {
      refetch()
      close()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Tab') {
        // shift : 역으로 이동
        if (event.shiftKey) {
          if (document.activeElement === firstFocusableElementRef.current) {
            event.preventDefault()
            lastFocusableElementRef.current?.focus()
          }
        } else if (document.activeElement === lastFocusableElementRef.current) {
          event.preventDefault()
          firstFocusableElementRef.current?.focus()
        }
      }
    }

    firstFocusableElementRef.current?.focus()

    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  const selectedRemocon = useRecoilValue(selectedRemoconNameState)

  const { hardwareConfiguration } = useHardwareConfiguration()

  return (
    <Modal
      isOpen={isOpen}
      close={() => {
        close()
      }}
      title="Intelligent Monkey Test Block Option"
    >
      <div className="flex flex-col w-[580px] justify-between">
        <div className="flex flex-col">
          <div className="flex w-full items-center h-[50px]">
            <div className="w-[180px]">
              <Text className="bg-transparent">Profile</Text>
            </div>
            <div className="flex">
              <Select
                className="!w-[300px]"
                colorScheme="charcoal"
                header={<Text colorScheme="light">{profile}</Text>}
                ref={firstFocusableElementRef}
              >
                {profiles.map((_profile) => (
                  <OptionItem
                    colorScheme="charcoal"
                    key={`profile-${_profile}`}
                    onClick={() => {
                      setProfile(_profile)
                    }}
                  >
                    {_profile}
                  </OptionItem>
                ))}
              </Select>
            </div>
          </div>
          <div className="flex w-full items-center mt-2 h-[50px]">
            <div className="w-[180px]">
              <Text className="bg-transparent">Duration per Menu</Text>
            </div>
            <div className="flex">
              <Input
                className="!w-[100px]"
                type="number"
                value={duration}
                onChange={(e) => {
                  setDuration(Number(e.target.value))
                }}
              />
              <Select
                className="!w-[140px] ml-1"
                colorScheme="charcoal"
                header={<Text colorScheme="light">{durationTimeUnit}</Text>}
              >
                {timeUnit
                  .filter((_unit) => _unit !== 'ms')
                  .map((unit) => (
                    <OptionItem
                      colorScheme="charcoal"
                      key={`duration-time-unit-${unit}`}
                      onClick={() => {
                        setDurationTimeUnit(unit as Extract<TimeUnit, 'Sec' | 'Min'>)
                      }}
                    >
                      {unit}
                    </OptionItem>
                  ))}
              </Select>
            </div>
          </div>
          <div className="flex w-full mt-2 items-center h-[50px]">
            <div className="w-[180px]">
              <Text className="bg-transparent">Interval</Text>
            </div>
            <div className="flex">
              <Input
                className="!w-[100px]"
                type="number"
                value={interval}
                onChange={(e) => {
                  setInterval(Number(e.target.value))
                }}
              />
              <Select
                className="!w-[140px] ml-1"
                colorScheme="charcoal"
                header={<Text colorScheme="light">{intervalTimeUnit}</Text>}
              >
                {timeUnit
                  .filter((_unit) => _unit !== 'Min')
                  .map((unit) => (
                    <OptionItem
                      colorScheme="charcoal"
                      key={`interval-time-unit-${unit}`}
                      onClick={() => {
                        setIntervalTimeUnit(unit as Extract<TimeUnit, 'Sec' | 'ms'>)
                      }}
                    >
                      {unit}
                    </OptionItem>
                  ))}
              </Select>
            </div>
          </div>
          <div className="flex w-full mt-2 items-center h-[50px]">
            <div className="w-[180px]">
              <Text className="bg-transparent">Smart Sense</Text>
            </div>
            <ToggleButton
              isOn={!!isSmartSense}
              onClick={() => {
                setIsSmartSense((prev) => !prev)
              }}
            />
          </div>
          <div className="flex w-full mt-2 items-center h-[50px] opacity-40">
            <div className="w-[180px]">
              <Text className="bg-transparent">Waiting Time</Text>
            </div>
            <div className="flex">
              <Input
                className="!w-[100px]"
                type="number"
                disabled
                value={waitingTime}
                onChange={(e) => {
                  setWaitingTime(Number(e.target.value))
                }}
              />
              <Select
                className="!w-[140px] ml-1"
                disabled
                colorScheme="charcoal"
                header={<Text colorScheme="light">{waitingTimeTimeUnit}</Text>}
              >
                {timeUnit
                  .filter((_unit) => _unit !== 'ms')
                  .map((unit) => (
                    <OptionItem
                      colorScheme="charcoal"
                      key={`waiting-time-time-unit-${unit}`}
                      onClick={() => {
                        setWaitingTimeTimeUnit(unit as Extract<TimeUnit, 'Sec' | 'Min'>)
                      }}
                    >
                      {unit}
                    </OptionItem>
                  ))}
              </Select>
            </div>
          </div>
        </div>
        <div className="flex justify-end mt-6">
          <Button
            colorScheme="primary"
            className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
            onClick={() => {
              if (!selectedRemocon || !hardwareConfiguration || !scenarioId) return

              postBlockMutate({
                newBlock: {
                  type: 'intelligent_monkey_test',
                  name: 'Intelligent Monkey Test',
                  args: [
                    {
                      key: 'profile',
                      value: profile.toLowerCase(),
                    },
                    {
                      key: 'duration_per_menu',
                      value: durationTimeUnit === 'Sec' ? duration : duration * 60,
                    },
                    {
                      key: 'interval',
                      value: intervalTimeUnit === 'ms' ? interval : interval * 1000,
                    },
                    {
                      key: 'enable_smart_sense',
                      value: isSmartSense,
                    },
                    {
                      key: 'remocon_name',
                      value: selectedRemocon,
                    },
                    {
                      key: 'remote_control_type',
                      value: hardwareConfiguration.remote_control_type,
                    },
                  ],
                  delay_time: 3000,
                },
                scenario_id: scenarioId,
              })
            }}
          >
            OK
          </Button>
          <Button
            colorScheme="grey"
            className="w-[132px] h-[48px] text-white rounded-3xl"
            ref={lastFocusableElementRef}
            onClick={() => {
              close()
            }}
          >
            Cancel
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default AddIntelligentMonkeyTestBlockModal

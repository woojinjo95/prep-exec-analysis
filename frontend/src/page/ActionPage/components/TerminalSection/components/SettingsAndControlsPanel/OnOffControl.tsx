import React from 'react'

import { ToggleButton, Text, Divider, Title } from '@global/ui'
import { useWebsocket } from '@global/hook'
import { useHardwareConfiguration } from '@global/api/hook'

type OnOffControlResponseMessageBody = {
  service: string
  level: string
  time: number
  msg: string
  data: {
    vac: 'on' | 'off'
  }
}

const OnOffControl: React.FC = () => {
  const { hardwareConfiguration, refetch } = useHardwareConfiguration()
  const { sendMessage } = useWebsocket<OnOffControlResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'on_off_control_response') {
        refetch()
      }
    },
  })

  return (
    <div className="bg-light-black p-5 rounded-lg h-fit">
      <Title as="h3" colorScheme="light" className="px-1">
        On/Off Control
      </Title>

      <Divider />

      <ul className="grid grid-cols-1 gap-y-4 px-1">
        <li className="flex items-center justify-between">
          <Text weight="medium">DUT Power</Text>
          <ToggleButton
            isOn={!!hardwareConfiguration?.enable_dut_power}
            onClick={(isOn) => {
              sendMessage({ msg: 'on_off_control', data: { enable_dut_power: isOn } })
            }}
          />
        </li>
        <li className="flex items-center justify-between">
          <Text weight="medium">HDMI(HPD)</Text>
          <ToggleButton
            isOn={!!hardwareConfiguration?.enable_hdmi}
            onClick={(isOn) => {
              sendMessage({ msg: 'on_off_control', data: { enable_hdmi: isOn } })
            }}
          />
        </li>
        <li className="flex items-center justify-between">
          <Text weight="medium">DUT WAN</Text>
          <ToggleButton
            isOn={!!hardwareConfiguration?.enable_dut_wan}
            onClick={(isOn) => {
              sendMessage({ msg: 'on_off_control', data: { enable_dut_wan: isOn } })
            }}
          />
        </li>
        <li className="flex items-center justify-between">
          <Text weight="medium">Screen</Text>
          <button
            type="button"
            className="bg-primary w-20 h-7 rounded-full"
            onClick={() => {
              sendMessage({ msg: 'capture_board', data: { action: 'refresh' } })
            }}
          >
            <Text colorScheme="light" size="xs" weight="medium">
              Reset
            </Text>
          </button>
        </li>
      </ul>
    </div>
  )
}

export default OnOffControl

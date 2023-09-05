import React, { useState } from 'react'

import { ToggleButton, Text, Divider, Title } from '@global/ui'
import { useWebsocket } from '@global/hook'
import { useHardwareConfiguration, useScenarioById } from '@global/api/hook'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState, scenarioIdState } from '@global/atom'
import { useMutation } from 'react-query'
import { postBlock } from '@page/ActionPage/components/ActionSection/api/func'

type OnOffControlResponseMessageBody = {
  vac?: 'on' | 'off'
  enable_dut_power_transition?: string
  sensor_time: number
  hpd?: 'on' | 'off'
  enable_hdmi_transition?: string
  lan?: 'on' | 'off'
  enable_dut_wan_transition?: string
}

const OnOffControl: React.FC = () => {
  const { hardwareConfiguration, refetch } = useHardwareConfiguration()

  const scenarioId = useRecoilValue(scenarioIdState)

  const { refetch: scenarioRefetch } = useScenarioById({ scenarioId })

  const { mutate: postBlockMutate } = useMutation(postBlock, {
    onSuccess: () => {
      scenarioRefetch()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  const isBlockRecordMode = useRecoilValue(isBlockRecordModeState)

  const { sendMessage } = useWebsocket<OnOffControlResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'on_off_control_response') {
        refetch()

        if (!scenarioId || !isBlockRecordMode) return

        let blockType = ''
        let blockArgKey: 'enable_dut_power' | 'enable_hdmi' | 'enable_dut_wan' = 'enable_dut_power'
        let blockArgValueType: 'vac' | 'hpd' | 'lan' = 'vac'

        if (message.data.enable_dut_power_transition) {
          blockType = 'DUT Power'
          blockArgKey = 'enable_dut_power'
          blockArgValueType = 'vac'
        }
        if (message.data.enable_hdmi_transition) {
          blockType = 'HDMI'
          blockArgKey = 'enable_hdmi'
          blockArgValueType = 'hpd'
        }
        if (message.data.enable_dut_wan_transition) {
          blockType = 'DUT Wan'
          blockArgKey = 'enable_dut_wan'
          blockArgValueType = 'lan'
        }

        postBlockMutate({
          newBlock: {
            type: 'on_off_control',
            name: `Control: ${blockType} ${message.data[blockArgValueType]!}`,
            delay_time: 3000,
            args: [
              {
                key: blockArgKey,
                value: message.data[blockArgValueType],
              },
            ],
          },
          scenario_id: scenarioId,
        })
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

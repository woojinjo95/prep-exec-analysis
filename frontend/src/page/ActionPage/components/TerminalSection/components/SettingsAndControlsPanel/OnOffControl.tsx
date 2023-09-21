import React, { useCallback } from 'react'

import { ToggleButton, Text, Divider, Title, Skeleton } from '@global/ui'
import { useWebsocket } from '@global/hook'
import { useHardwareConfiguration, useScenarioById } from '@global/api/hook'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState, scenarioIdState, testRunIdState } from '@global/atom'
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

type blockType = 'DUT Power' | 'HDMI' | 'DUT Wan'
type blockArgKey = 'enable_dut_power' | 'enable_hdmi' | 'enable_dut_wan'

const OnOffControl: React.FC = () => {
  const { hardwareConfiguration, refetch } = useHardwareConfiguration()

  const scenarioId = useRecoilValue(scenarioIdState)

  const testrunId = useRecoilValue(testRunIdState)

  const { refetch: scenarioRefetch } = useScenarioById({ scenarioId, testrunId })

  const { mutate: postBlockMutate } = useMutation(postBlock, {
    onSuccess: () => {
      scenarioRefetch()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  const isBlockRecordMode = useRecoilValue(isBlockRecordModeState)

  const postBlockWithMessageData = useCallback(
    ({
      blockType,
      blockArgKey,
      blockValue,
    }: {
      blockType: blockType
      blockArgKey: blockArgKey
      blockValue: 'on' | 'off'
    }) => {
      if (!scenarioId) return
      postBlockMutate({
        newBlock: {
          type: 'on_off_control',
          name: `Control: ${blockType} ${blockValue}`,
          delay_time: 3000,
          args: [
            {
              key: blockArgKey,
              value: blockValue,
            },
          ],
        },
        scenario_id: scenarioId,
      })
    },
    [],
  )

  const { sendMessage } = useWebsocket<OnOffControlResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'on_off_control_response') {
        refetch()

        if (!scenarioId) return

        if (!isBlockRecordMode) return

        if (message.data.enable_dut_power_transition) {
          postBlockWithMessageData({
            blockType: 'DUT Power',
            blockArgKey: 'enable_dut_power',
            blockValue: message.data.vac!,
          })
        }
        if (message.data.enable_hdmi_transition) {
          postBlockWithMessageData({
            blockType: 'HDMI',
            blockArgKey: 'enable_hdmi',
            blockValue: message.data.hpd!,
          })
        }
        if (message.data.enable_dut_wan_transition) {
          postBlockWithMessageData({
            blockType: 'DUT Wan',
            blockArgKey: 'enable_dut_wan',
            blockValue: message.data.lan!,
          })
        }
      }
      if (message.msg === 'capture_board_response') {
        refetch()

        if (!scenarioId) return

        if (!isBlockRecordMode) return

        postBlockMutate({
          newBlock: {
            type: 'capture_board',
            delay_time: 3000,
            name: 'Screen: refresh',
            args: [
              {
                key: 'action',
                value: 'refresh',
              },
            ],
          },
          scenario_id: scenarioId,
        })
      }
    },
  })

  return (
    <>
      {!hardwareConfiguration && <Skeleton colorScheme="dark" className="p-5 rounded-lg h-[260px]" />}
      {hardwareConfiguration && (
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
      )}
    </>
  )
}

export default OnOffControl

import React from 'react'

import { ReactComponent as IRIcon } from '@assets/images/icon_remote_ir_w.svg'
import { ReactComponent as BluetoothIcon } from '@assets/images/icon_remote_bt_w.svg'
import { ButtonGroup, Divider, GroupButton, Skeleton, Title } from '@global/ui'
import { useWebsocket } from '@global/hook'
import { useHardwareConfiguration, useScenarioById } from '@global/api/hook'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState, scenarioIdState, testRunIdState } from '@global/atom'
import { useMutation } from 'react-query'
import { postBlock } from '@page/ActionPage/components/ActionSection/api/func'

type RemoteControlResponseMessageBody = {
  type: 'ir' | 'bt'
}

const RemoteControl: React.FC = () => {
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

  const { sendMessage } = useWebsocket<RemoteControlResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'remocon_properties_response') {
        refetch()

        if (!scenarioId) return
        if (!isBlockRecordMode) return
        postBlockMutate({
          newBlock: {
            type: 'remocon_properties',
            name: `Remote Control: ${message.data.type}`,
            delay_time: 3000,
            args: [
              {
                key: 'type',
                value: message.data.type,
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
      {!hardwareConfiguration && <Skeleton colorScheme="dark" className="p-5 rounded-lg h-[150px]" />}
      {hardwareConfiguration && (
        <div className="bg-light-black p-5 rounded-lg h-fit">
          <Title as="h3" colorScheme="light" className="px-1">
            Remote Control
          </Title>

          <Divider />

          <ButtonGroup>
            <GroupButton
              isActive={hardwareConfiguration?.remote_control_type === 'ir'}
              icon={<IRIcon />}
              onClick={() => {
                if (hardwareConfiguration?.remote_control_type === 'ir') return
                sendMessage({ msg: 'remocon_properties', data: { type: 'ir' } })
              }}
            >
              IR
            </GroupButton>
            <GroupButton
              isActive={hardwareConfiguration?.remote_control_type === 'bt'}
              icon={<BluetoothIcon />}
              onClick={() => {
                if (hardwareConfiguration?.remote_control_type === 'bt') return
                sendMessage({ msg: 'remocon_properties', data: { type: 'bt' } })
              }}
            >
              Bluetooth
            </GroupButton>
          </ButtonGroup>
        </div>
      )}
    </>
  )
}

export default RemoteControl

import React from 'react'

import { ReactComponent as IRIcon } from '@assets/images/icon_remote_ir_w.svg'
import { ReactComponent as BluetoothIcon } from '@assets/images/icon_remote_bt_w.svg'
import { ButtonGroup, Divider, GroupButton, Title } from '@global/ui'
import { useWebsocket } from '@global/hook'
import { useHardwareConfiguration } from '@global/api/hook'

const RemoteControl: React.FC = () => {
  const { hardwareConfiguration, refetch } = useHardwareConfiguration()
  const { sendMessage } = useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'remocon_properties_response') {
        refetch()
      }
    },
  })

  return (
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
  )
}

export default RemoteControl

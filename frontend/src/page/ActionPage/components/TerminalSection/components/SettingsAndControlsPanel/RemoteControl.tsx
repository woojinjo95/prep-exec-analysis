import React from 'react'
import { useMutation } from 'react-query'
import { useToast } from '@chakra-ui/react'

import { ReactComponent as IRIcon } from '@assets/images/icon_remote_ir_w.svg'
import { ReactComponent as BluetoothIcon } from '@assets/images/icon_remote_bt_w.svg'
import { ButtonGroup, Divider, GroupButton, Title } from '@global/ui'
import { useHardwareConfiguration } from '../../api/hook'
import { putHardwareConfiguration } from '../../api/func'

const RemoteControl: React.FC = () => {
  const toast = useToast({ duration: 3000, isClosable: true })
  const { hardwareConfiguration, refetch } = useHardwareConfiguration()
  const { mutate: updateHardwareConfiguration } = useMutation(putHardwareConfiguration, {
    onSuccess: () => {
      refetch()
    },
    onError: () => {
      toast({ status: 'error', title: 'An error has occurred. Please try again.' })
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
            updateHardwareConfiguration({ remote_control_type: 'ir' })
          }}
        >
          IR
        </GroupButton>
        <GroupButton
          isActive={hardwareConfiguration?.remote_control_type === 'bluetooth'}
          icon={<BluetoothIcon />}
          onClick={() => {
            if (hardwareConfiguration?.remote_control_type === 'bluetooth') return
            updateHardwareConfiguration({ remote_control_type: 'bluetooth' })
          }}
        >
          Bluetooth
        </GroupButton>
      </ButtonGroup>
    </div>
  )
}

export default RemoteControl

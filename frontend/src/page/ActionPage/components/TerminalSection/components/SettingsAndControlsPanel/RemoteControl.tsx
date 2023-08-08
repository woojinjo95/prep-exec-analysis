import React from 'react'
import { useMutation } from 'react-query'
import { useToast } from '@chakra-ui/react'
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
    <div className="bg-white">
      <h4>Remote Control</h4>
      <button
        type="button"
        onClick={() => {
          if (hardwareConfiguration?.remote_control_type === 'ir') return
          updateHardwareConfiguration({ remote_control_type: 'ir' })
        }}
      >
        <input type="radio" readOnly checked={hardwareConfiguration?.remote_control_type === 'ir'} />
        <span className="mr-4">IR</span>
      </button>

      <button
        type="button"
        onClick={() => {
          if (hardwareConfiguration?.remote_control_type === 'bluetooth') return
          updateHardwareConfiguration({ remote_control_type: 'bluetooth' })
        }}
      >
        <input type="radio" readOnly checked={hardwareConfiguration?.remote_control_type === 'bluetooth'} />
        <span>Bluetooth</span>
      </button>
    </div>
  )
}

export default RemoteControl

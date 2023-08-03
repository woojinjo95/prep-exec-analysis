import React from 'react'
import { ToggleButton } from '@global/ui'
import { useToast } from '@chakra-ui/react'
import { useMutation } from 'react-query'
import { useHardwareConfiguration } from '../../api/hook'
import { putHardwareConfiguration } from '../../api/func'

const OnOffControl: React.FC = () => {
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
    <div className="bg-white h-fit">
      <h4>On/Off Control</h4>

      <ul>
        <li>
          <span>DUT Power</span>
          <ToggleButton
            isOn={!!hardwareConfiguration?.enable_dut_power}
            onClick={(isOn) => updateHardwareConfiguration({ enable_dut_power: isOn })}
          />
        </li>
        <li>
          <span>HDMI(HPD)</span>
          <ToggleButton
            isOn={!!hardwareConfiguration?.enable_hdmi}
            onClick={(isOn) => updateHardwareConfiguration({ enable_hdmi: isOn })}
          />
        </li>
        <li>
          <span>DUT WAN</span>
          <ToggleButton
            isOn={!!hardwareConfiguration?.enable_dut_wan}
            onClick={(isOn) => updateHardwareConfiguration({ enable_dut_wan: isOn })}
          />
        </li>
      </ul>
    </div>
  )
}

export default OnOffControl

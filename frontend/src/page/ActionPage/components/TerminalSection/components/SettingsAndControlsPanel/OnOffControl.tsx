import React from 'react'
import { ToggleButton, Text, Divider, Title } from '@global/ui'
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
    <div className="bg-light-black p-5 rounded-lg h-fit">
      <Title as="h3" colorScheme="light">
        On/Off Control
      </Title>

      <Divider />

      <ul className="grid grid-cols-1 gap-y-4">
        <li className="flex items-center justify-between">
          <Text weight="medium">DUT Power</Text>
          <ToggleButton
            isOn={!!hardwareConfiguration?.enable_dut_power}
            onClick={(isOn) => updateHardwareConfiguration({ enable_dut_power: isOn })}
          />
        </li>
        <li className="flex items-center justify-between">
          <Text weight="medium">HDMI(HPD)</Text>
          <ToggleButton
            isOn={!!hardwareConfiguration?.enable_hdmi}
            onClick={(isOn) => updateHardwareConfiguration({ enable_hdmi: isOn })}
          />
        </li>
        <li className="flex items-center justify-between">
          <Text weight="medium">DUT WAN</Text>
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

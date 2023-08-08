import React, { useCallback, useState } from 'react'
import { useMutation } from 'react-query'
import { useToast } from '@chakra-ui/react'
import { Input, ToggleButton } from '@global/ui'

import { useHardwareConfiguration } from '../../../api/hook'
import { putHardwareConfiguration } from '../../../api/func'
import IPLimitItem from './IPLimitItem'

/**
 * 네트워크 에뮬레이션 컴포넌트
 */
const NetworkEmulation: React.FC = () => {
  const toast = useToast({ duration: 3000, isClosable: true })
  const [bandwidth, setBandwidth] = useState<number | null>(null)
  const [delay, setDelay] = useState<number | null>(null)
  const [loss, setLoss] = useState<number | null>(null)
  const { hardwareConfiguration, refetch } = useHardwareConfiguration({
    onSuccess: (data) => {
      setBandwidth(data.packet_bandwidth)
      setDelay(data.packet_delay)
      setLoss(data.packet_loss)
    },
  })
  const { mutate: updateHardwareConfiguration } = useMutation(putHardwareConfiguration, {
    onSuccess: () => {
      refetch()
    },
    onError: () => {
      toast({ status: 'error', title: 'An error has occurred. Please try again.' })
    },
  })
  const [isAddingIPLimit, setIsAddingIPLimit] = useState<boolean>(false)

  const onBlurInput = useCallback(
    (key: 'bandwidth' | 'delay' | 'loss', value: number | null): React.FocusEventHandler<HTMLInputElement> =>
      () => {
        // TODO: validate bandwidth, delay, loss
        if (value === hardwareConfiguration?.[`packet_${key}`] || value === null) return
        updateHardwareConfiguration({ [`packet_${key}`]: value })
      },
    [hardwareConfiguration],
  )

  const onKeyDownInput = useCallback(
    (key: 'bandwidth' | 'delay' | 'loss', value: number | null): React.KeyboardEventHandler<HTMLInputElement> =>
      (e) => {
        if (e.key !== 'Enter') return
        e.currentTarget.blur()
        // TODO: validate bandwidth, delay, loss
        if (value === hardwareConfiguration?.[`packet_${key}`] || value === null) return
        updateHardwareConfiguration({ [`packet_${key}`]: value })
      },
    [hardwareConfiguration],
  )

  return (
    <div className="bg-white row-span-2">
      <div>
        <h4>Network Emulation</h4>
        <ToggleButton
          isOn={!!hardwareConfiguration?.enable_network_emulation}
          onClick={(isOn) => updateHardwareConfiguration({ enable_network_emulation: isOn })}
        />
      </div>

      <div className="grid grid-cols-3 grid-rows-[auto_1fr] gap-2">
        <div className="col-span-3">
          <h6>Packet Contorl (Inbound)</h6>
        </div>

        <div>
          <p>Bandwidth</p>
          <Input
            value={bandwidth || 0}
            type="number"
            pattern="[0-9]*"
            onChange={(e) => setBandwidth(Number(e.target.value))}
            onBlur={onBlurInput('bandwidth', bandwidth)}
            onKeyDown={onKeyDownInput('bandwidth', bandwidth)}
          />
        </div>

        <div>
          <p>Delay</p>
          <Input
            value={delay || 0}
            type="number"
            pattern="[0-9]*"
            onChange={(e) => setDelay(Number(e.target.value))}
            onBlur={onBlurInput('delay', delay)}
            onKeyDown={onKeyDownInput('delay', delay)}
          />
        </div>

        <div>
          <p>Loss</p>
          <Input
            value={loss || 0}
            type="number"
            pattern="[0-9]*"
            onChange={(e) => setLoss(Number(e.target.value))}
            onBlur={onBlurInput('loss', loss)}
            onKeyDown={onKeyDownInput('loss', loss)}
          />
        </div>
      </div>

      <div>
        <h6>Configuring IP Limit</h6>

        {isAddingIPLimit && <IPLimitItem isFocusDefault cancelAddIPLimit={() => setIsAddingIPLimit(false)} />}
        {hardwareConfiguration?.ip_limit?.map(({ id, ip, port, protocol }) => (
          <IPLimitItem key={`hardware-configuration-ip-limit-${id}`} ip={ip} port={port} protocol={protocol} />
        ))}

        {!isAddingIPLimit && (
          <button type="button" onClick={() => setIsAddingIPLimit(true)}>
            Add Item
          </button>
        )}
      </div>
    </div>
  )
}

export default NetworkEmulation

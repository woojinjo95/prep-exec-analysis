import React, { useCallback, useState } from 'react'
import { useMutation } from 'react-query'
import { useToast } from '@chakra-ui/react'

import { ReactComponent as RefreshIcon } from '@assets/images/icon_refresh_w.svg'
import { Input, Title, ToggleButton, Text, Divider, Button } from '@global/ui'
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
    <div className="row-span-2 bg-light-black p-5 rounded-lg h-fit">
      <div className="flex items-center gap-x-5 px-1">
        <Title as="h3" colorScheme="light">
          Network Emulation
        </Title>

        <ToggleButton
          isOn={!!hardwareConfiguration?.enable_network_emulation}
          onClick={(isOn) => updateHardwareConfiguration({ enable_network_emulation: isOn })}
        />

        {/* FIXME: 이 아이콘의 용도 찾기 */}
        <button type="button" className="ml-auto">
          <RefreshIcon className="w-5 h-5" />
        </button>
      </div>

      <Divider />

      <div className="pb-1 px-1">
        <div>
          <Text weight="medium">Packet Contorl (Inbound)</Text>
        </div>

        <div className="pt-2 flex justify-between">
          <div className="w-1/3">
            <Text weight="medium" size="xs">
              Bandwidth
            </Text>
            <div className="mt-1 grid grid-rows-1 grid-cols-[55%_40%] gap-x-2 items-center">
              <Input
                colorScheme="charcoal"
                value={bandwidth || 0}
                type="number"
                pattern="[0-9]*"
                onChange={(e) => setBandwidth(Number(e.target.value))}
                onBlur={onBlurInput('bandwidth', bandwidth)}
                onKeyDown={onKeyDownInput('bandwidth', bandwidth)}
              />
              <Text weight="medium" size="xs" className="mr-2">
                Mbps
              </Text>
            </div>
          </div>

          <div className="w-1/3">
            <Text weight="medium" size="xs">
              Delay
            </Text>
            <div className="mt-1 grid grid-rows-1 grid-cols-[55%_40%] gap-x-2 items-center">
              <Input
                colorScheme="charcoal"
                value={delay || 0}
                type="number"
                pattern="[0-9]*"
                onChange={(e) => setDelay(Number(e.target.value))}
                onBlur={onBlurInput('delay', delay)}
                onKeyDown={onKeyDownInput('delay', delay)}
              />
              <Text weight="medium" size="xs" className="mr-2">
                ms
              </Text>
            </div>
          </div>

          <div className="w-1/3">
            <Text weight="medium" size="xs">
              Loss
            </Text>
            <div className="mt-1 grid grid-rows-1 grid-cols-[55%_40%] gap-x-2 items-center">
              <Input
                colorScheme="charcoal"
                value={loss || 0}
                type="number"
                pattern="[0-9]*"
                onChange={(e) => setLoss(Number(e.target.value))}
                onBlur={onBlurInput('loss', loss)}
                onKeyDown={onKeyDownInput('loss', loss)}
              />
              <Text weight="medium" size="xs" className="mr-2">
                %
              </Text>
            </div>
          </div>
        </div>
      </div>

      <Divider />

      <div className="grid grid-cols-1 px-1">
        <Text weight="medium" className="pb-4">
          Configuring IP Limit
        </Text>

        {isAddingIPLimit && <IPLimitItem isFocusDefault cancelAddIPLimit={() => setIsAddingIPLimit(false)} />}
        {hardwareConfiguration?.ip_limit?.map(({ id, ip, port, protocol }) => (
          <IPLimitItem key={`hardware-configuration-ip-limit-${id}`} ip={ip} port={port} protocol={protocol} />
        ))}

        {!isAddingIPLimit && (
          <Button type="button" colorScheme="charcoal" onClick={() => setIsAddingIPLimit(true)}>
            Add Item
          </Button>
        )}
      </div>
    </div>
  )
}

export default NetworkEmulation

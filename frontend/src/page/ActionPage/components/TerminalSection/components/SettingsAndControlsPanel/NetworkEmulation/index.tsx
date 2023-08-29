import React, { useCallback, useState } from 'react'
import { useToast } from '@chakra-ui/react'

import { ReactComponent as RefreshIcon } from '@assets/images/icon_refresh_w.svg'
import { Input, Title, ToggleButton, Text, Divider, Button } from '@global/ui'
import { useHardwareConfiguration } from '@global/api/hook'
import { useWebsocket } from '@global/hook'
import IPLimitItem from './IPLimitItem'

/**
 * 네트워크 에뮬레이션 컴포넌트
 */
const NetworkEmulation: React.FC = () => {
  const toast = useToast({ duration: 3000, isClosable: true })
  const [input, setInput] = useState<{ bandwidth: string | null; delay: string | null; loss: string | null }>({
    bandwidth: null,
    delay: null,
    loss: null,
  })
  const { hardwareConfiguration, refetch } = useHardwareConfiguration({
    onSuccess: (data) => {
      setInput({
        bandwidth: String(data.packet_bandwidth),
        delay: String(data.packet_delay),
        loss: String(data.packet_loss),
      })
    },
  })
  const { sendMessage } = useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'network_emulation_response') {
        refetch()
      }
    },
  })

  const [isAddingIPLimit, setIsAddingIPLimit] = useState<boolean>(false)

  /**
   * Packet Control 업데이트 함수
   */
  const updatePacketControl = useCallback(
    (key: 'bandwidth' | 'delay' | 'loss', value: string | null) => {
      if (!hardwareConfiguration) return

      if (value === String(hardwareConfiguration?.[`packet_${key}`])) return

      if (value === '') {
        sendMessage({
          msg: 'network_emulation',
          data: {
            action: 'update',
            [`packet_${key}`]: key === 'bandwidth' ? 1000 : 0,
          },
        })
        return
      }

      const newValue = Number(value)

      if (key === 'bandwidth' && (newValue < 0 || newValue > 1000)) {
        toast({ status: 'warning', title: 'For bandwidth, only values ​​between 0Mbps and 1000Mbps can be entered.' })
        setInput((prev) => ({
          ...prev,
          [key]: String(hardwareConfiguration[`packet_${key}`]),
        }))
        return
      }

      if (key === 'delay' && (newValue < 0 || newValue > 100000)) {
        toast({ status: 'warning', title: 'For delay, only values ​​between 0ms and 100000ms(100s) can be entered.' })
        setInput((prev) => ({
          ...prev,
          [key]: String(hardwareConfiguration[`packet_${key}`]),
        }))
        return
      }

      if (key === 'loss' && (newValue < 0 || newValue > 100)) {
        toast({ status: 'warning', title: 'For loss, only values ​​between 0% and 100% can be entered.' })
        setInput((prev) => ({
          ...prev,
          [key]: String(hardwareConfiguration[`packet_${key}`]),
        }))
        return
      }

      sendMessage({
        msg: 'network_emulation',
        data: {
          action: 'update',
          [`packet_${key}`]: newValue,
        },
      })
    },
    [hardwareConfiguration],
  )

  const onChangeInput = useCallback(
    (key: keyof typeof input): React.ChangeEventHandler<HTMLInputElement> =>
      (e) => {
        const { value } = e.target

        if (Number.isNaN(value)) return

        if (value.length > 1 && value.charAt(0) === '0') {
          setInput((prev) => ({
            ...prev,
            [key]: value.slice(1),
          }))
          return
        }

        setInput((prev) => ({
          ...prev,
          [key]: value,
        }))
      },
    [],
  )

  const onBlurInput = useCallback(
    (key: 'bandwidth' | 'delay' | 'loss'): React.FocusEventHandler<HTMLInputElement> =>
      () => {
        updatePacketControl(key, input[key])
      },
    [updatePacketControl, input],
  )

  const onKeyDownInput: React.KeyboardEventHandler<HTMLInputElement> = useCallback(
    (e) => {
      if (e.key !== 'Enter') return
      e.currentTarget.blur()
    },
    [updatePacketControl, input],
  )

  return (
    <div className="row-span-2 bg-light-black p-5 rounded-lg h-fit">
      <div className="flex items-center gap-x-5 px-1">
        <Title as="h3" colorScheme="light">
          Network Emulation
        </Title>

        <ToggleButton
          isOn={!!hardwareConfiguration?.enable_network_emulation}
          onClick={(isOn) => {
            sendMessage({ msg: 'network_emulation', data: { action: isOn ? 'start' : 'stop' } })
          }}
        />

        <button
          type="button"
          className="ml-auto"
          onClick={() => {
            // FIXME: confirm 함수 -> custom confirm으로 대체
            if (
              !window.confirm('Do you want to set all values ​​related to Network Emulation to their initial values?')
            )
              return
            sendMessage({ msg: 'network_emulation', data: { action: 'reset' } })
          }}
        >
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
                value={input.bandwidth === null ? '' : input.bandwidth}
                placeholder="1000"
                type="number"
                onChange={onChangeInput('bandwidth')}
                onBlur={onBlurInput('bandwidth')}
                onKeyDown={onKeyDownInput}
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
                value={input.delay === null ? '' : input.delay}
                placeholder="0"
                type="number"
                onChange={onChangeInput('delay')}
                onBlur={onBlurInput('delay')}
                onKeyDown={onKeyDownInput}
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
                value={input.loss === null ? '' : input.loss}
                placeholder="0"
                type="number"
                onChange={onChangeInput('loss')}
                onBlur={onBlurInput('loss')}
                onKeyDown={onKeyDownInput}
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

        {hardwareConfiguration?.packet_block?.map(({ id, ip, port, protocol }) => (
          <IPLimitItem key={`hardware-configuration-ip-limit-${id}`} id={id} ip={ip} port={port} protocol={protocol} />
        ))}
        {isAddingIPLimit && <IPLimitItem isCreating close={() => setIsAddingIPLimit(false)} />}

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

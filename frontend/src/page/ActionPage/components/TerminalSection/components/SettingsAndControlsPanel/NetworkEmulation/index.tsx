/* eslint-disable no-nested-ternary */
import React, { useCallback, useState } from 'react'
import { useToast } from '@chakra-ui/react'

import { ReactComponent as RefreshIcon } from '@assets/images/icon_refresh_w.svg'
import { Input, Title, ToggleButton, Text, Divider, Button, Skeleton } from '@global/ui'
import { useHardwareConfiguration, useScenarioById } from '@global/api/hook'
import { useWebsocket } from '@global/hook'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState, scenarioIdState, testRunIdState } from '@global/atom'
import { SubscribeMessage } from '@global/hook/useWebsocket/types'
import { useMutation } from 'react-query'
import { postBlock, postBlocks } from '@page/ActionPage/components/ActionSection/api/func'
import { Block } from '@global/api/entity'
import IPLimitItem from './IPLimitItem'

type NetworkEmulationMessageBody = {
  action: 'create' | 'update' | 'delete' | 'reset' | 'start' | 'stop'
  log: string
  updated: {
    create?: {
      ip?: string
      port?: string
      protocol: string
    }
    update?: {
      id: string
      ip?: string
      port?: string
      protocol: string
    }
    delete?: {
      id?: string
      ip: string
      port?: string
      protocol: string
    }
    packet_bandwidth?: number
    packet_delay?: number
    packet_loss?: number
  }
}

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

  const isBlockRecordMode = useRecoilValue(isBlockRecordModeState)

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

  // updated에 따라 block을 만들어주는 함수
  const makeBlockByUpdated: (message: SubscribeMessage<NetworkEmulationMessageBody>) => Omit<Block, 'id'> | null =
    useCallback((message: SubscribeMessage<NetworkEmulationMessageBody>) => {
      // reset 일 때
      if (message.data.action === 'reset') {
        return {
          type: 'network_emulation',
          name: `Reset: Network emulation`,
          delay_time: 3000,
          args: [
            {
              key: 'action',
              value: 'reset',
            },
          ],
        }
      }

      // toggle stop일 때 (toggle on 일 때는 postBlocks이므로 따로 처리)
      if (message.data.action === 'stop') {
        return {
          type: 'network_emulation',
          name: `Network Emulation: All Allow`,
          delay_time: 3000,
          args: [
            {
              key: 'action',
              value: 'stop',
            },
          ],
        }
      }

      // ip limit 일 때
      if (message.data.updated.create || message.data.updated.update || message.data.updated.delete) {
        if (message.data.updated.create) {
          return {
            type: 'network_emulation',
            name: `IP Limit (Registered) : ${message.data.updated.create.ip || ''}:${
              message.data.updated.create.port || ''
            } (${message.data.updated.create.protocol})`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: message.data.action,
              },
              {
                key: 'packet_block',
                value: message.data.updated.create,
              },
            ],
          }
        }
        if (message.data.updated.update) {
          return {
            type: 'network_emulation',
            name: `IP Limit (Modified) : ${message.data.updated.update.ip || ''}:${
              message.data.updated.update.port || ''
            } (${message.data.updated.update.protocol})`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: message.data.action,
              },
              {
                key: 'packet_block',
                value: message.data.updated.update,
              },
            ],
          }
        }
        if (message.data.updated.delete) {
          return {
            type: 'network_emulation',
            name: `IP Limit (Deleted) : ${message.data.updated.delete.ip || ''}${
              message.data.updated.delete.port || ''
            } (${message.data.updated.delete.protocol})`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: message.data.action,
              },
              {
                key: 'packet_block',
                value: message.data.updated.delete,
              },
            ],
          }
        }
      }

      // packet Control 일 때
      if (
        message.data.updated.packet_bandwidth ||
        message.data.updated.packet_delay ||
        message.data.updated.packet_loss
      ) {
        if (message.data.updated.packet_bandwidth) {
          return {
            type: 'network_emulation',
            name: `Packet Control: BandWidth ${message.data.updated.packet_bandwidth}Mbps`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: 'update',
              },
              {
                key: 'packet_bandwidth',
                value: message.data.updated.packet_bandwidth,
              },
            ],
          }
        }

        if (message.data.updated.packet_delay) {
          return {
            type: 'network_emulation',
            name: `Packet Control: Delay ${message.data.updated.packet_delay}ms`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: 'update',
              },
              {
                key: 'packet_delay',
                value: message.data.updated.packet_delay,
              },
            ],
          }
        }

        if (message.data.updated.packet_loss) {
          return {
            type: 'network_emulation',
            name: `Packet Control: Loss ${message.data.updated.packet_loss}%`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: 'update',
              },
              {
                key: 'packet_loss',
                value: message.data.updated.packet_loss,
              },
            ],
          }
        }
      }

      return null
    }, [])

  const { mutate: postBlocksMutate } = useMutation(postBlocks, {
    onSuccess: () => {
      scenarioRefetch()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  const { sendMessage } = useWebsocket<NetworkEmulationMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'network_emulation_response') {
        refetch()

        if (!scenarioId) return

        // 녹화중인 상태일 때만
        if (!isBlockRecordMode) return

        // toggle start일 때
        if (message.data.action === 'start' && hardwareConfiguration) {
          const bandwidthBlock: Omit<Block, 'id'> = {
            type: 'network_emulation',
            name: `Packet Control: BandWidth ${hardwareConfiguration.packet_bandwidth}Mbps`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: 'update',
              },
              {
                key: 'packet_bandwidth',
                value: hardwareConfiguration.packet_bandwidth,
              },
            ],
          }
          const delayBlock: Omit<Block, 'id'> = {
            type: 'network_emulation',
            name: `Packet Control: Delay ${hardwareConfiguration.packet_delay}ms`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: 'update',
              },
              {
                key: 'packet_delay',
                value: hardwareConfiguration.packet_delay,
              },
            ],
          }
          const lossBlock: Omit<Block, 'id'> = {
            type: 'network_emulation',
            name: `Packet Control: Loss ${hardwareConfiguration.packet_loss}%`,
            delay_time: 3000,
            args: [
              {
                key: 'action',
                value: 'update',
              },
              {
                key: 'packet_loss',
                value: hardwareConfiguration.packet_loss,
              },
            ],
          }
          const ipLimitBlocks: Omit<Block, 'id'>[] | undefined = hardwareConfiguration.packet_block?.map(
            (ip_limit) => ({
              type: 'network_emulation',
              name: `IP Limit (Registered) : ${ip_limit.ip || ''}:${ip_limit.port || ''} (${ip_limit.protocol})`,
              delay_time: 3000,
              args: [
                {
                  key: 'action',
                  value: 'create',
                },
                {
                  key: 'packet_block',
                  value: {
                    ip: ip_limit.ip || '',
                    port: ip_limit.port || '',
                    protocol: ip_limit.protocol,
                  },
                },
              ],
            }),
          )
          const newBlocks: Omit<Block, 'id'>[] = ipLimitBlocks
            ? [bandwidthBlock, delayBlock, lossBlock, ...ipLimitBlocks]
            : [bandwidthBlock, delayBlock, lossBlock]

          postBlocksMutate({
            newBlocks,
            scenario_id: scenarioId,
          })
        }

        // toggle on 이외의 상황
        if (!makeBlockByUpdated(message)) return

        postBlockMutate({
          newBlock: makeBlockByUpdated(message)!,
          scenario_id: scenarioId,
        })
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
    <Skeleton isLoaded={!!hardwareConfiguration} colorScheme="dark" className="row-span-2 rounded-lg h-fit">
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
            <Text weight="medium">Packet Control (Inbound)</Text>
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
            <IPLimitItem
              key={`hardware-configuration-ip-limit-${id}`}
              id={id}
              ip={ip}
              port={port}
              protocol={protocol}
            />
          ))}
          {isAddingIPLimit && <IPLimitItem isCreating close={() => setIsAddingIPLimit(false)} />}

          {!isAddingIPLimit && (
            <Button type="button" colorScheme="charcoal" onClick={() => setIsAddingIPLimit(true)}>
              Add Item
            </Button>
          )}
        </div>
      </div>
    </Skeleton>
  )
}

export default NetworkEmulation

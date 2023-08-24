import React, { useCallback, useRef, useState } from 'react'
import classnames from 'classnames/bind'

import { Input, OptionItem, Select } from '@global/ui'
import { IPLimit } from '@global/api/entity'
import useWebsocket from '@global/module/websocket'
import { IPRegex } from '@global/constant'
import { ReactComponent as EditIcon } from '@assets/images/icon_edit.svg'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { ReactComponent as CancelIcon } from '@assets/images/x.svg'
import { ReactComponent as SaveIcon } from '@assets/images/checked.svg'

import { useToast } from '@chakra-ui/react'
import styles from './IPLimitItem.module.scss'

const validateIP = (ip?: string | null): string => {
  if (!!ip && !IPRegex.test(ip)) return 'Please enter ip in correct format.'
  return ''
}

const validatePort = (port?: string | null): string => {
  if (!port) return ''

  // number일 경우
  if (!Number.isNaN(Number(port))) {
    if (Number(port) < 0 || Number(port) > 65535) {
      return 'For the port, only values ​​between 0 and 65535 can be entered.'
    }
    return ''
  }

  const portA = Number(port.split(':')[0])
  const portB = Number(port.split(':')[1])
  // string일 경우
  if (!port.includes(':') || !portA || !portB || Number.isNaN(portA) || Number.isNaN(portB)) {
    return 'Please enter the correct port format. The port can be entered as a number or {number:number} format.'
  }

  if (portA < 0 || portA > 65535 || portB < 0 || portB > 65535) {
    return 'For the port, only values ​​between 0 and 65535 can be entered.'
  }

  return ''
}

const cx = classnames.bind(styles)

const Protocols: readonly IPLimit['protocol'][] = ['all', 'tcp', 'udp'] as const

interface IPLimitItemProps {
  id?: IPLimit['id']
  ip?: IPLimit['ip']
  port?: IPLimit['port']
  protocol?: IPLimit['protocol']
  isCreating?: boolean
  close?: () => void
}

/**
 * 네트워크 에뮬레이션 - 제한 IP 아이템
 *
 * @param id IP Limit 아이템 id. 추가 모드일 경우 값 없음
 * @param mode 아이템 추가 / 수정 모드 여부
 */
const IPLimitItem: React.FC<IPLimitItemProps> = ({
  id,
  ip: defaultIP = '',
  port: defaultPort = '',
  protocol: defaultProtocol = 'all',
  isCreating = false,
  close,
}) => {
  const toast = useToast({ duration: 3000, isClosable: true })
  const firstFoucsableInputRef = useRef<HTMLInputElement | null>(null)
  const [isEditing, setIsEditing] = useState<boolean>(isCreating)
  const [ip, setIP] = useState<string>(defaultIP)
  const [port, setPort] = useState<string>(defaultPort)
  const [protocol, setProtocol] = useState<IPLimit['protocol']>(defaultProtocol)

  const { sendMessage } = useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'network_emulation_response') {
        // TODO: 네트워크 에뮬레이션 - IP Limit 관련 변경항목만 체크 => 현재 updated.update.ip 이렇게 접근해야 함 ..

        // created
        close?.()

        // updated
        setIsEditing(false)
      }
    },
  })

  /**
   * IP 제한 아이템 추가
   */
  const onSubmitCreateIPLimit = useCallback(() => {
    if (validateIP(ip)) {
      toast({ status: 'warning', title: validateIP(ip) })
      return
    }

    if (validatePort(port)) {
      toast({ status: 'warning', title: validatePort(port) })
      return
    }

    sendMessage({
      msg: 'network_emulation',
      data: {
        action: 'create',
        packet_block: {
          ip,
          port,
          protocol,
        },
      },
    })
  }, [ip, port, protocol])

  /**
   * IP 제한 아이템 수정
   */
  const onSubmitUpdateIPLimit = useCallback(() => {
    if (!id) return

    if (validateIP(ip)) {
      toast({ status: 'warning', title: validateIP(ip) })
      return
    }

    if (validatePort(port)) {
      toast({ status: 'warning', title: validatePort(port) })
      return
    }

    sendMessage({
      msg: 'network_emulation',
      data: {
        action: 'update',
        packet_block: {
          id,
          ip,
          port,
          protocol,
        },
      },
    })
  }, [id, ip, port, protocol])

  /**
   * IP 제한 아이템 삭제
   */
  const onSubmitDeleteIPLimit = useCallback(() => {
    // FIXME: 멈춰있는 만큼 스트리밍 delay됨. 변경 필요
    if (!window.confirm('Are you sure you want to delete?')) return

    sendMessage({
      msg: 'network_emulation',
      data: {
        action: 'delete',
        packet_block: {
          id,
        },
      },
    })
  }, [id])

  return (
    <div className="grid grid-cols-[80%_20%] pb-3">
      <div className="grid grid-cols-[45%_20%_30%] gap-x-2 items-center">
        <Input
          colorScheme="charcoal"
          ref={firstFoucsableInputRef}
          autoFocus={isCreating}
          placeholder="IP"
          value={ip || ''}
          disabled={!isEditing}
          onChange={(e) => setIP(e.target.value)}
        />
        <Input
          colorScheme="charcoal"
          placeholder="Port"
          value={port || ''}
          disabled={!isEditing}
          onChange={(e) => setPort(e.target.value)}
        />
        <Select colorScheme="charcoal" value={protocol} disabled={!isEditing}>
          {Protocols.map((p) => (
            <OptionItem
              colorScheme="charcoal"
              key={`ip-limit-select-protocol-${p}`}
              onClick={() => {
                setProtocol(p)
              }}
              isActive={p === protocol}
            >
              {p}
            </OptionItem>
          ))}
        </Select>
      </div>

      {isEditing ? (
        <div className="grid grid-rows-1 grid-cols-2 justify-center">
          <button
            type="button"
            className="flex justify-center items-center"
            onClick={() => {
              if (isCreating) {
                onSubmitCreateIPLimit()
                return
              }

              onSubmitUpdateIPLimit()
            }}
          >
            <SaveIcon className={cx('w-6', 'icon')} />
          </button>
          <button
            type="button"
            className="flex justify-center items-center"
            onClick={() => {
              if (isCreating) {
                close?.()
                return
              }

              setIP(defaultIP)
              setPort(defaultPort)
              setProtocol(defaultProtocol)
              setIsEditing(false)
            }}
          >
            <CancelIcon className={cx('w-5 h-5', 'icon')} />
          </button>
        </div>
      ) : (
        <div className="grid grid-rows-1 grid-cols-2 justify-center">
          <button
            type="button"
            className="flex justify-center items-center"
            onClick={() => {
              firstFoucsableInputRef.current?.focus()
              setIsEditing(true)
            }}
          >
            <EditIcon className={cx('h-6', 'icon')} />
          </button>
          <button type="button" className="flex justify-center items-center" onClick={onSubmitDeleteIPLimit}>
            <TrashIcon className={cx('h-6', 'icon')} />
          </button>
        </div>
      )}
    </div>
  )
}

export default IPLimitItem

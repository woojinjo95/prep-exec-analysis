import React, { useRef, useState } from 'react'
import { Input, OptionItem, Select, Text } from '@global/ui'
import { IPLimit } from '@global/api/entity'

const Protocols: readonly IPLimit['protocol'][] = ['all', 'tcp', 'udp'] as const

interface IPLimitItemProps {
  ip?: IPLimit['ip']
  port?: IPLimit['port']
  protocol?: IPLimit['protocol']
  isFocusDefault?: boolean
  cancelAddIPLimit?: () => void
}

/**
 * 네트워크 에뮬레이션 - 제한 IP 아이템
 */
const IPLimitItem: React.FC<IPLimitItemProps> = ({
  ip: defaultIP = '',
  port: defaultPort = '',
  protocol: defaultProtocol = 'all',
  isFocusDefault = false,
  cancelAddIPLimit,
}) => {
  const firstFoucsableInputRef = useRef<HTMLInputElement | null>(null)
  const [isEditing, setIsEditing] = useState<boolean>(isFocusDefault)
  const [ip, setIP] = useState<typeof defaultIP>(defaultIP)
  const [port, setPort] = useState<typeof defaultPort>(defaultPort)
  const [protocol, setProtocol] = useState<typeof defaultProtocol>(defaultProtocol)

  return (
    <div className="grid grid-cols-[80%_20%] pb-3">
      <div className="grid grid-cols-[45%_20%_30%] gap-x-2 items-center">
        <Input
          colorScheme="charcoal"
          ref={firstFoucsableInputRef}
          autoFocus={isFocusDefault}
          placeholder="IP"
          value={ip}
          onChange={(e) => setIP(e.target.value)}
        />
        <Input colorScheme="charcoal" placeholder="Port" value={port} onChange={(e) => setPort(e.target.value)} />
        <Select colorScheme="charcoal" value={protocol}>
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
        <div className="grid grid-cols-1 justify-center">
          <button type="button" onClick={cancelAddIPLimit}>
            <Text colorScheme="light">save</Text>
          </button>
          <button type="button" onClick={cancelAddIPLimit}>
            <Text colorScheme="light">cancel</Text>
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 justify-center">
          <button
            type="button"
            onClick={() => {
              firstFoucsableInputRef.current?.focus()
              setIsEditing(true)
            }}
          >
            <Text colorScheme="light">modify</Text>
          </button>
          <button type="button">
            <Text colorScheme="light">delete</Text>
          </button>
        </div>
      )}
    </div>
  )
}

export default IPLimitItem

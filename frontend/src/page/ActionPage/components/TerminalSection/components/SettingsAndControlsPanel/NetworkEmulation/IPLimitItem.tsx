import React, { useRef, useState } from 'react'
import { Input } from '@global/ui'
import { useActiveElement } from '@global/hook'
import { IPLimit } from '../../../api/entity'

const Protocols: readonly IPLimit['protocol'][] = ['all', 'tcp', 'udp'] as const

// const regexIP = /^((d{1,2}|1dd|2[0-4]d|25[0-5]).){3}(d{1,2}|1dd|2[0-4]d|25[0-5])$/

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
  const [isEditing, setIsEditing] = useState<boolean>(isFocusDefault)
  const focusableRefs = useRef<
    [HTMLInputElement, HTMLInputElement, HTMLSelectElement, HTMLButtonElement | undefined] | []
  >([])
  const [ip, setIP] = useState<typeof defaultIP>(defaultIP)
  const [port, setPort] = useState<typeof defaultPort>(defaultPort)
  const [protocol, setProtocol] = useState<typeof defaultProtocol>(defaultProtocol)

  useActiveElement((activeElement) => {
    // start editing
    if (focusableRefs.current.some((ref) => activeElement === ref)) {
      setIsEditing(true)
    }

    // end editing
    if (isEditing && focusableRefs.current.every((ref) => activeElement !== ref)) {
      if (!ip && !port) {
        console.log('IP or Port input is required.') // FIXME: Toast로 교체
        focusableRefs.current[0]?.focus()
        return
      }

      // TODO: save ip limit
      setIsEditing(false)
    }
  })

  return (
    <div className="grid grid-cols-[80%_20%] pb-3">
      <div className="grid grid-cols-[45%_20%_30%] gap-x-1 items-center">
        <Input
          colorScheme="charcoal"
          ref={(ref) => {
            if (!ref) return
            focusableRefs.current[0] = ref
          }}
          autoFocus={isFocusDefault}
          placeholder="IP"
          value={ip}
          onChange={(e) => setIP(e.target.value)}
        />

        <Input
          colorScheme="charcoal"
          ref={(ref) => {
            if (!ref) return
            focusableRefs.current[1] = ref
          }}
          placeholder="Port"
          value={port}
          onChange={(e) => setPort(e.target.value)}
        />

        <select
          ref={(ref) => {
            if (!ref) return
            focusableRefs.current[2] = ref
          }}
          value={protocol}
          onChange={(e) => setProtocol(e.target.value as typeof protocol)}
        >
          {Protocols.map((p) => (
            <option key={`ip-limit-select-protocol-${p}`} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>

      {isEditing ? (
        <button
          ref={(ref) => {
            if (!ref) return
            focusableRefs.current[3] = ref
          }}
          type="button"
          onClick={cancelAddIPLimit}
        >
          cancel
        </button>
      ) : (
        <button type="button">delete</button>
      )}
    </div>
  )
}

export default IPLimitItem

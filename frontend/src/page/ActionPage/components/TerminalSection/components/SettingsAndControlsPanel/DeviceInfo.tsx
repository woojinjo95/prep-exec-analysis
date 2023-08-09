import React, { useCallback, useState } from 'react'
import { useMutation } from 'react-query'

import { Button, Divider, Input, OptionItem, Select, Title } from '@global/ui'
import { IPRegex } from '@global/constant'
import { useHardwareConfiguration } from '../../api/hook'
import { postHardwareConfigurationSTBConnection, putHardwareConfigurationSTBConnection } from '../../api/func'
import { HardwareConfiguration } from '../../api/entity'

const validateIP = (ip: string) => {
  if (!ip) return 'Enter IP.'
  if (!IPRegex.test(ip)) return 'Please enter ip in correct format.'
  return ''
}
const validatePort = (port: string) => {
  if (!port) return 'Enter port.'
  if (Number.isNaN(Number(port))) return 'Port must be a number.'
  return ''
}
const validateUsername = (port: string) => {
  if (!port) return 'Enter username.'
  return ''
}
const validatePassword = (port: string) => {
  if (!port) return 'Enter password.'
  return ''
}

const ConnectionTypes = ['adb', 'ssh'] as const

const DeviceInfo: React.FC = () => {
  const [type, setType] = useState<'adb' | 'ssh' | null>(null)
  const [ip, setIP] = useState<string>('')
  const [port, setPort] = useState<string>('')
  const [username, setUsername] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [warningMessage, setWarningMessage] = useState<{
    ip: string
    port: string
    username: string
    password: string
  }>({ ip: '', port: '', username: '', password: '' })

  const { hardwareConfiguration, refetch } = useHardwareConfiguration({
    onSuccess: (data) => {
      setWarningMessage({ ip: '', port: '', username: '', password: '' })
      setType(data.stb_connection?.type || null)
      setIP(data.stb_connection?.ip || '')
      setPort(data.stb_connection?.port || '')
      setUsername(data.stb_connection?.username || '')
      setPassword(data.stb_connection?.password || '')
    },
  })
  const { mutate: createSTBConnection } = useMutation(postHardwareConfigurationSTBConnection, {
    onSuccess: () => {
      refetch()
    },
  })
  const { mutate: updateSTBConnection } = useMutation(putHardwareConfigurationSTBConnection, {
    onSuccess: () => {
      refetch()
    },
  })

  const clearFields = useCallback(() => {
    setIP('')
    setPort('')
    setUsername('')
    setPassword('')
    setWarningMessage({ ip: '', port: '', username: '', password: '' })
  }, [])

  const onClickSubmit = () => {
    if (!type) return

    const stbConnection: HardwareConfiguration['stb_connection'] =
      type === 'adb' ? { type, ip, port } : { type, ip, port, username, password }
    let isNotValid = false

    setWarningMessage((prev) => ({ ...prev, ip: validateIP(ip) }))
    if (validateIP(ip)) isNotValid = true

    setWarningMessage((prev) => ({ ...prev, port: validatePort(port) }))
    if (validatePort(port)) isNotValid = true

    if (type === 'ssh') {
      setWarningMessage((prev) => ({ ...prev, username: validateUsername(username) }))
      if (validateUsername(username)) isNotValid = true

      setWarningMessage((prev) => ({ ...prev, password: validatePassword(password) }))
      if (validatePassword(password)) isNotValid = true
    }

    if (isNotValid) return

    if (type !== hardwareConfiguration?.stb_connection?.type) {
      createSTBConnection(stbConnection)
      return
    }

    updateSTBConnection(stbConnection)
  }

  return (
    <div className="row-span-2 bg-light-black p-5 rounded-lg min-h-full h-fit">
      <Title as="h3" colorScheme="light" className="px-1">
        Device Info
      </Title>

      <Divider />

      <div className="grid grid-cols-1 gap-y-4 px-1">
        <Select colorScheme="charcoal" value={type || 'Type'}>
          {ConnectionTypes.map((connectionType) => (
            <OptionItem
              colorScheme="charcoal"
              key={`device-info-select-connection-type-${connectionType}`}
              onClick={() => {
                if (type !== connectionType) {
                  setType(connectionType)
                  clearFields()
                }
              }}
              isActive={connectionType === type}
            >
              {connectionType}
            </OptionItem>
          ))}
        </Select>

        {!!type && (
          <>
            <div className="grid grid-rows-1 grid-cols-[2fr_1fr] gap-x-2">
              <Input
                placeholder="IP"
                value={ip}
                onChange={(e) => setIP(e.target.value)}
                warningMessage={warningMessage.ip}
              />
              <Input
                placeholder="Port"
                value={port}
                onChange={(e) => setPort(e.target.value)}
                warningMessage={warningMessage.port}
              />
            </div>

            {type === 'ssh' && (
              <>
                <Input
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  warningMessage={warningMessage.username}
                />
                <Input
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  warningMessage={warningMessage.password}
                />
              </>
            )}

            {(type !== hardwareConfiguration?.stb_connection?.type ||
              ip !== hardwareConfiguration?.stb_connection?.ip ||
              port !== hardwareConfiguration?.stb_connection?.port ||
              username !== hardwareConfiguration?.stb_connection?.username ||
              password !== hardwareConfiguration?.stb_connection?.password) && (
              <Button colorScheme="primary" className="mb-2" isRoundedFull onClick={onClickSubmit}>
                Submit
              </Button>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default DeviceInfo

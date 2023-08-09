import React, { useMemo, useState } from 'react'
import { useMutation } from 'react-query'

import { Button, Divider, Input, OptionItem, Select, Title } from '@global/ui'
import { IPRegex } from '@global/constant'
import { useHardwareConfiguration } from '../../api/hook'
import { putHardwareConfigurationSTBConnection } from '../../api/func'
import { HardwareConfiguration } from '../../api/entity'

const validateIP = (ip?: string | null) => {
  if (!ip) return 'Enter IP.'
  if (!IPRegex.test(ip)) return 'Please enter ip in correct format.'
  return ''
}
const validatePort = (port?: string | null) => {
  if (!port) return 'Enter port.'
  if (Number.isNaN(Number(port))) return 'Port must be a number.'
  return ''
}
const validateUsername = (username?: string | null) => {
  if (!username) return 'Enter username.'
  return ''
}
const validatePassword = (password?: string | null) => {
  if (!password) return 'Enter password.'
  return ''
}

const ConnectionTypes = ['adb', 'ssh'] as const
type STBConnection = {
  type?: NonNullable<HardwareConfiguration['stb_connection']>['type'] | null
  ip?: NonNullable<HardwareConfiguration['stb_connection']>['ip'] | null
  port?: NonNullable<HardwareConfiguration['stb_connection']>['port'] | null
  username?: NonNullable<HardwareConfiguration['stb_connection']>['username'] | null
  password?: NonNullable<HardwareConfiguration['stb_connection']>['password'] | null
}
const DefaultSTBConnection = { type: null, ip: '', port: '', username: '', password: '' } as const
const DefaultWarningMessage = { ip: '', port: '', username: '', password: '' } as const

const DeviceInfo: React.FC = () => {
  const [stbConnection, setSTBConnection] = useState<STBConnection>(DefaultSTBConnection)
  const [warningMessage, setWarningMessage] = useState<{
    ip: string
    port: string
    username: string
    password: string
  }>(DefaultWarningMessage)

  const { hardwareConfiguration, refetch } = useHardwareConfiguration({
    onSuccess: (data) => {
      setWarningMessage(DefaultWarningMessage)
      setSTBConnection({
        type: data.stb_connection?.type,
        ip: data.stb_connection?.ip,
        port: data.stb_connection?.port,
        username: data.stb_connection?.username,
        password: data.stb_connection?.password,
      })
    },
  })
  const isChanged = useMemo(
    () =>
      Object.keys(stbConnection).some(
        (key) =>
          stbConnection[key as keyof STBConnection] !==
          hardwareConfiguration?.stb_connection?.[key as keyof STBConnection],
      ),
    [stbConnection, hardwareConfiguration],
  )
  const { mutate: updateSTBConnection } = useMutation(putHardwareConfigurationSTBConnection, {
    onSuccess: () => {
      refetch()
    },
  })

  const onClickSubmit = () => {
    const { type, ip, port, username, password } = stbConnection
    if (!type) return

    const data: Partial<HardwareConfiguration['stb_connection']> =
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
    updateSTBConnection(data as Parameters<typeof updateSTBConnection>[0])
  }

  return (
    <div className="row-span-2 bg-light-black p-5 rounded-lg min-h-full h-fit">
      <Title as="h3" colorScheme="light" className="px-1">
        Device Info
      </Title>

      <Divider />

      <div className="grid grid-cols-1 gap-y-4 px-1">
        <Select colorScheme="charcoal" value={stbConnection.type || 'Type'}>
          {ConnectionTypes.map((connectionType) => (
            <OptionItem
              colorScheme="charcoal"
              key={`device-info-select-connection-type-${connectionType}`}
              onClick={() => {
                if (stbConnection.type !== connectionType) {
                  setSTBConnection({ ...DefaultSTBConnection, type: connectionType })
                  setWarningMessage(DefaultWarningMessage)
                }
              }}
              isActive={connectionType === stbConnection.type}
            >
              {connectionType}
            </OptionItem>
          ))}
        </Select>

        {!!stbConnection.type && (
          <>
            <div className="grid grid-rows-1 grid-cols-[2fr_1fr] gap-x-2">
              <Input
                placeholder="IP"
                value={stbConnection.ip || ''}
                onChange={(e) => setSTBConnection((prev) => ({ ...prev, ip: e.target.value }))}
                warningMessage={warningMessage.ip}
              />
              <Input
                placeholder="Port"
                value={stbConnection.port || ''}
                onChange={(e) => setSTBConnection((prev) => ({ ...prev, port: e.target.value }))}
                warningMessage={warningMessage.port}
              />
            </div>

            {stbConnection.type === 'ssh' && (
              <>
                <Input
                  placeholder="Username"
                  value={stbConnection.username || ''}
                  onChange={(e) => setSTBConnection((prev) => ({ ...prev, username: e.target.value }))}
                  warningMessage={warningMessage.username}
                />
                <Input
                  placeholder="Password"
                  value={stbConnection.password || ''}
                  onChange={(e) => setSTBConnection((prev) => ({ ...prev, password: e.target.value }))}
                  warningMessage={warningMessage.password}
                />
              </>
            )}

            {isChanged && (
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

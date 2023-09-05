import React, { useEffect, useMemo, useState } from 'react'
import { useMutation } from 'react-query'

import { Button, Divider, Input, OptionItem, Select, Title, Text } from '@global/ui'
import { IPRegex } from '@global/constant'
import { HardwareConfiguration } from '@global/api/entity'
import { useHardwareConfiguration, useLogConnectionStatus, useScenarioById } from '@global/api/hook'
import { postBlock } from '@page/ActionPage/components/ActionSection/api/func'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState, scenarioIdState } from '@global/atom'
import { putHardwareConfigurationSTBConnection } from '../../api/func'

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
  mode?: NonNullable<HardwareConfiguration['stb_connection']>['mode'] | null
  host?: NonNullable<HardwareConfiguration['stb_connection']>['host'] | null
  port?: NonNullable<HardwareConfiguration['stb_connection']>['port'] | null
  username?: NonNullable<HardwareConfiguration['stb_connection']>['username'] | null
  password?: NonNullable<HardwareConfiguration['stb_connection']>['password'] | null
}
const DefaultSTBConnection = { mode: null, ip: '', port: '', username: '', password: '' } as const
const DefaultWarningMessage = { host: '', port: '', username: '', password: '' } as const

const DeviceInfo: React.FC = () => {
  const [stbConnection, setSTBConnection] = useState<STBConnection>(DefaultSTBConnection)
  const [warningMessage, setWarningMessage] = useState<{
    host: string
    port: string
    username: string
    password: string
  }>(DefaultWarningMessage)

  const { hardwareConfiguration, refetch } = useHardwareConfiguration({
    onSuccess: (data) => {
      setWarningMessage(DefaultWarningMessage)
      setSTBConnection({
        mode: data.stb_connection?.mode,
        host: data.stb_connection?.host,
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

  const scenarioId = useRecoilValue(scenarioIdState)

  const { refetch: scenarioRefetch } = useScenarioById({ scenarioId })

  const { mutate: postBlockMutate } = useMutation(postBlock, {
    onSuccess: () => {
      scenarioRefetch()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  const isBlockRecordMode = useRecoilValue(isBlockRecordModeState)

  const { logConnectionStatus } = useLogConnectionStatus()

  const [isStbConnectionUpdated, setIsStbConnectionUpdated] = useState<boolean>(false)

  const { mutate: updateSTBConnection } = useMutation(putHardwareConfigurationSTBConnection, {
    onSuccess: () => {
      refetch()
      setIsStbConnectionUpdated(true)
    },
  })

  // stbConnection이 updated 되고, logConnectionStatus가 성공적으로 connected 되었을 때만 block 추가
  useEffect(() => {
    if (isStbConnectionUpdated && logConnectionStatus === 'log_connected') {
      if (!scenarioId || !isBlockRecordMode) return

      // 이미 데이터 검증이 끝난 상태
      const { mode, host, port, username, password } = stbConnection
      if (!mode) return

      const data: Partial<HardwareConfiguration['stb_connection']> =
        mode === 'adb' ? { mode, host, port } : { mode, host, port, username, password }

      postBlockMutate({
        newBlock: {
          type: 'device_info',
          name: `Device Info: ${mode} / ${
            mode === 'adb'
              ? `${data.host!}:${data.port!}`
              : `${data.host!}:${data.port!} ID: ${data.username!} PW: ${data.password!}`
          }`,
          delay_time: 3000,
          args: [
            {
              key: 'host',
              value: data.host!,
            },
            {
              key: 'mode',
              value: data.mode!,
            },
            {
              key: 'port',
              value: data.port!,
            },
            {
              key: 'password',
              value: data.password ? data.password : null,
            },
            {
              key: 'username',
              value: data.username ? data.username : null,
            },
          ],
        },
        scenario_id: scenarioId,
      })

      setIsStbConnectionUpdated(false)
    }
  }, [logConnectionStatus, isStbConnectionUpdated])

  const onClickSubmit = () => {
    const { mode, host, port, username, password } = stbConnection
    if (!mode) return

    const data: Partial<HardwareConfiguration['stb_connection']> =
      mode === 'adb' ? { mode, host, port } : { mode, host, port, username, password }
    let isNotValid = false

    setWarningMessage((prev) => ({ ...prev, host: validateIP(host) }))
    if (validateIP(host)) isNotValid = true

    setWarningMessage((prev) => ({ ...prev, port: validatePort(port) }))
    if (validatePort(port)) isNotValid = true

    if (mode === 'ssh') {
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
        <Select
          colorScheme="charcoal"
          header={
            <Text weight="bold" colorScheme="light">
              {stbConnection.mode || 'Type'}
            </Text>
          }
        >
          {ConnectionTypes.map((connectionType) => (
            <OptionItem
              colorScheme="charcoal"
              key={`device-info-select-connection-mode-${connectionType}`}
              onClick={() => {
                if (stbConnection.mode !== connectionType) {
                  setSTBConnection({ ...DefaultSTBConnection, mode: connectionType })
                  setWarningMessage(DefaultWarningMessage)
                }
              }}
              isActive={connectionType === stbConnection.mode}
            >
              {connectionType}
            </OptionItem>
          ))}
        </Select>

        {!!stbConnection.mode && (
          <>
            <div className="grid grid-rows-1 grid-cols-[2fr_1fr] gap-x-2">
              <Input
                onClick={() => {
                  if (stbConnection.host) return

                  setSTBConnection((prev) => ({
                    ...prev,
                    host: hardwareConfiguration?.dut_ip,
                  }))
                }}
                placeholder={hardwareConfiguration?.dut_ip || 'IP'}
                value={stbConnection.host || ''}
                onChange={(e) => setSTBConnection((prev) => ({ ...prev, host: e.target.value }))}
                warningMessage={warningMessage.host}
              />
              <Input
                placeholder="Port"
                value={stbConnection.port || ''}
                onChange={(e) => setSTBConnection((prev) => ({ ...prev, port: e.target.value }))}
                warningMessage={warningMessage.port}
              />
            </div>

            {stbConnection.mode === 'ssh' && (
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

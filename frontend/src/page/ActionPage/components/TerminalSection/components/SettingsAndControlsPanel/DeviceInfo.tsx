import { Button, Divider, Input, OptionItem, Select, Title } from '@global/ui'
import React, { useState } from 'react'

const ConnectionTypes = ['adb', 'ssh'] as const

const DeviceInfo: React.FC = () => {
  const [type, setType] = useState<'adb' | 'ssh' | null>(null)

  return (
    <div className="row-span-2 bg-light-black p-5 rounded-lg h-fit">
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
                setType(connectionType)
              }}
              isActive={connectionType === type}
            >
              {connectionType}
            </OptionItem>
          ))}
        </Select>

        <div className="grid grid-rows-1 grid-cols-[2fr_1fr] gap-x-2">
          <Input placeholder="IP" />
          <Input placeholder="Port" />
        </div>

        <Input placeholder="Username" />
        <Input placeholder="Password" />

        <Button colorScheme="primary" className="mb-2" isRoundedFull>
          Submit
        </Button>
      </div>
    </div>
  )
}

export default DeviceInfo

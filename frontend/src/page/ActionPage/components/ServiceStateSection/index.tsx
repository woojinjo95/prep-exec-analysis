import React from 'react'
import { Text } from '@global/ui'
import { LogConnectionStatusLabel } from '@global/constant'
import { useLogConnectionStatus } from '@global/api/hook'
import { useServiceState } from './api/hook'

/**
 * 서비스 상태 표시 영역
 */
const ServiceStateSection: React.FC = () => {
  const { serviceState } = useServiceState()
  const { logConnectionStatus } = useLogConnectionStatus()

  return (
    <div className="w-full px-8 flex items-center bg-black border-b border-light-charcoal">
      <Text colorScheme="light" className="!text-[12px]">
        {serviceState}
      </Text>

      {logConnectionStatus && (
        <Text colorScheme="orange" className="ml-4 !text-[12px]">
          {LogConnectionStatusLabel[logConnectionStatus]}
        </Text>
      )}
    </div>
  )
}

export default ServiceStateSection

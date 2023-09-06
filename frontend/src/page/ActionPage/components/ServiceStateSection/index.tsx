import React, { useEffect, useState } from 'react'
import { Text } from '@global/ui'
import { LogConnectionStatusLabel } from '@global/constant'
import { useLogConnectionStatus, useServiceState } from '@global/api/hook'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState } from '@global/atom'
import cx from 'classnames'

/**
 * 서비스 상태 표시 영역
 */
const ServiceStateSection: React.FC = () => {
  const { serviceState } = useServiceState()
  const { logConnectionStatus } = useLogConnectionStatus()

  const isBlockRecordMode = useRecoilValue(isBlockRecordModeState)

  const [isBorderVisible, setIsBorderVisible] = useState<boolean>(true)

  useEffect(() => {
    const timer = setInterval(() => {
      setIsBorderVisible((prev) => !prev)
    }, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [])

  return (
    <div
      className={cx('w-full px-8 flex items-center bg-black border-b border-light-charcoal', {
        'border-red border-l-4 border-r-4 border-t-0 border-b-4': isBlockRecordMode && isBorderVisible,
        'border-primary border-l-4 border-t-4 border-r-4': serviceState === 'playblock' && isBorderVisible,
      })}
    >
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

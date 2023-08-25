import React from 'react'
import { Text } from '@global/ui'
import { useSetRecoilState } from 'recoil'
import { serviceStateState } from '@global/atom'
import { useServiceState } from './api/hook'

/**
 * 서비스 상태 표시 영역
 */
const ServiceStateSection: React.FC = () => {
  const setServiceState = useSetRecoilState(serviceStateState)
  const { serviceState } = useServiceState({
    onSuccess: (state) => {
      setServiceState(state)
    },
  })

  return (
    <div className="w-full px-8 flex items-center bg-black border-b border-light-charcoal">
      <Text colorScheme="light" className="!text-[12px]">
        {serviceState}
      </Text>
    </div>
  )
}

export default ServiceStateSection

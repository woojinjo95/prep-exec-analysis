import React from 'react'
import { ReactComponent as NoticeIcon } from '@assets/images/icon_notice.svg'
import { Text } from '..'

const ControlNotice: React.FC = () => {
  return (
    <div className="w-[224px] h-[112px] p-12 flex justify-center items-center">
      <NoticeIcon className="w-8" />
      <Text colorScheme="orange">You cannot control it</Text>
      <Text colorScheme="orange">while the tes in in progress.</Text>
    </div>
  )
}

export default ControlNotice

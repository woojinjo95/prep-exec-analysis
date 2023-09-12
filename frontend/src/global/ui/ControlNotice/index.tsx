import React from 'react'
import { ReactComponent as NoticeIcon } from '@assets/images/icon_notice.svg'
import { Text } from '..'

const ControlNotice: React.FC = () => {
  return (
    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[224px] h-[112px] flex flex-col justify-center items-center z-20 bg-black">
      <NoticeIcon className="w-8 h-8" />
      <Text colorScheme="orange">You cannot control it</Text>
      <Text colorScheme="orange">while the tes in in progress.</Text>
    </div>
  )
}

export default ControlNotice

import React, { useState } from 'react'
import { useQuery } from 'react-query'
import { OptionItem, Select, Skeleton, Text } from '@global/ui'
import BackgroundImage from '@assets/images/background_pattern.svg'

import { KeyEvent } from '@page/ActionPage/types'
import { useServiceState } from '@global/api/hook'
import { useRecoilState } from 'recoil'
import { selectedRemoconNameState } from '@global/atom'
import ControlNotice from '@global/ui/ControlNotice'
import { Remocon } from './api/entity'
import { getRemocon } from './api/func'
import RemoconComponent from './components/RemoconComponent'

interface RemoconSectionProps {
  keyEvent: KeyEvent | null
}

/**
 * 리모컨 영역
 */
const RemoconSection: React.FC<RemoconSectionProps> = ({ keyEvent }) => {
  const [selectedRemocon, setSelectedRemocon] = useState<Remocon | null>(null)

  const { serviceState } = useServiceState()

  // recoil 상태 set
  const [, _setSelectedRemoconName] = useRecoilState(selectedRemoconNameState)

  const { data: remocons } = useQuery<Remocon[]>(['remocon'], () => getRemocon(), {
    onSuccess: (res) => {
      if (res) {
        if (!selectedRemocon) {
          setSelectedRemocon(res[0])
          _setSelectedRemoconName(res[0].name)
        }

        const newSelectedRemocon = res.find((remocon) => remocon.name === selectedRemocon?.name)

        if (newSelectedRemocon) {
          setSelectedRemocon(newSelectedRemocon)
          _setSelectedRemoconName(newSelectedRemocon.name)
        }
      }
    },
    onError: (err) => {
      console.error(err)
    },
  })

  return (
    <section
      className="row-span-2 h-full p-[20px] pb-0 bg-[#F1F2F4] relative"
      style={{
        backgroundImage: `url(${BackgroundImage})`,
        backgroundSize: '100%',
      }}
    >
      <div className="grid grid-rows-1 grid-cols-[1fr_auto] w-full pb-3 items-center">
        {(!selectedRemocon || !remocons) && <Skeleton colorScheme="light" className="h-[60px] w-full rounded-xl" />}
        {selectedRemocon && remocons && (
          <Select
            header={
              <Text weight="bold" colorScheme="dark">
                {selectedRemocon.name}
              </Text>
            }
            colorScheme="light"
          >
            {remocons.map((remocon) => (
              <OptionItem
                colorScheme="light"
                key={`remocon_${remocon.name}`}
                onClick={() => {
                  setSelectedRemocon(remocon)
                  _setSelectedRemoconName(remocon.name)
                }}
                isActive={selectedRemocon.name === remocon.name}
              >
                {remocon.name}
              </OptionItem>
            ))}
          </Select>
        )}
      </div>

      {(!selectedRemocon || !remocons) && (
        <div className="w-full h-[calc(100%-62px)] grid grid-cols-2 grid-rows-1">
          <div className="w-full flex">
            <Skeleton colorScheme="light" className="h-full w-[95%] rounded-xl" />
          </div>
          <div className="w-full flex-col flex items-center">
            <div className="w-full flex justify-between">
              <Skeleton colorScheme="light" className="w-[65%] h-[48px] rounded-xl mb-[5px]" />
              <Skeleton colorScheme="light" className="h-[48px] w-[25%] rounded-xl mb-[5px]" />
            </div>
            <Skeleton colorScheme="light" className="h-[48px] w-[100%] rounded-xl mb-[5px]" />
            <Skeleton colorScheme="light" className="h-[48px] w-[100%] rounded-xl mb-[5px]" />
            <Skeleton colorScheme="light" className="h-[48px] w-[100%] rounded-xl mb-[5px]" />
          </div>
        </div>
      )}
      {selectedRemocon && <RemoconComponent remocon={selectedRemocon} keyEvent={keyEvent} />}
      {serviceState === 'playblock' && (
        <>
          <div className="absolute top-0 left-0 w-full h-full z-10 bg-black opacity-[0.6]" />
          <ControlNotice />
        </>
      )}
    </section>
  )
}

export default RemoconSection

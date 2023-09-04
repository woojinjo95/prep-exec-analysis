import React, { useState } from 'react'
import { useQuery } from 'react-query'
import { OptionItem, Select, Text } from '@global/ui'
import BackgroundImage from '@assets/images/background_pattern.svg'

import { KeyEvent } from '@page/ActionPage/types'
import { useServiceState } from '@global/api/hook'
import { useRecoilState } from 'recoil'
import { selectedRemoconState } from '@global/atom'
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
  const [, _setSelectedRemocon] = useRecoilState(selectedRemoconState)

  const { data: remocons } = useQuery<Remocon[]>(['remocon'], () => getRemocon(), {
    onSuccess: (res) => {
      if (res) {
        if (!selectedRemocon) {
          setSelectedRemocon(res[0])
          _setSelectedRemocon(res[0])
        }

        const newSelectedRemocon = res.find((remocon) => remocon.name === selectedRemocon?.name)

        if (newSelectedRemocon) {
          setSelectedRemocon(newSelectedRemocon)
          _setSelectedRemocon(newSelectedRemocon)
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
                  _setSelectedRemocon(remocon)
                }}
                isActive={selectedRemocon.name === remocon.name}
              >
                {remocon.name}
              </OptionItem>
            ))}
          </Select>
        )}
      </div>

      {selectedRemocon && <RemoconComponent remocon={selectedRemocon} keyEvent={keyEvent} />}
      {serviceState === 'playblock' && (
        <div className="absolute top-0 left-0 w-full h-full z-10 bg-black opacity-[0.6]" />
      )}
    </section>
  )
}

export default RemoconSection

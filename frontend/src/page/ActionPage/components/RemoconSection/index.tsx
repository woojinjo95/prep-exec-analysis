import React, { useState } from 'react'

// import RemoconImage from '@assets/images/btv_remote_control.png'

import InformationIcon from '@assets/images/information.png'
import { OptionItem, Select } from '@global/ui'

import { KeyEvent } from '@page/ActionPage/types'
import { useQuery } from 'react-query'
import BackgroundImage from '@assets/images/background_pattern.svg'
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

  const { data: remocons } = useQuery<Remocon[]>(['remocon'], () => getRemocon(), {
    onSuccess: (res) => {
      if (res) {
        if (!selectedRemocon) {
          setSelectedRemocon(res[0])
        }

        const newSelectedRemocon = res.find((remocon) => remocon.name === selectedRemocon?.name)

        if (newSelectedRemocon) {
          setSelectedRemocon(newSelectedRemocon)
        }
      }
    },
    onError: (err) => {
      console.error(err)
    },
  })

  return (
    <section
      className="border border-black h-full p-[20px] pb-0 bg-[#F1F2F4]"
      style={{
        backgroundImage: `url(${BackgroundImage})`,
        backgroundSize: '100%',
      }}
    >
      <div className="grid grid-rows-1 grid-cols-[1fr_auto] w-full h-[30px] items-center">
        {selectedRemocon && remocons && (
          <Select value={selectedRemocon.name} colorScheme="light">
            {remocons.map((remocon) => (
              <OptionItem
                colorScheme="light"
                key={`remocon_${remocon.name}`}
                onClick={() => {
                  setSelectedRemocon(remocon)
                }}
                isActive={selectedRemocon.name === remocon.name}
              >
                {remocon.name}
              </OptionItem>
            ))}
          </Select>
        )}

        <img alt="information_icon" src={InformationIcon} className="w-[20px] h-[20px] cursor-pointer" />
      </div>

      {selectedRemocon && <RemoconComponent remocon={selectedRemocon} keyEvent={keyEvent} />}
    </section>
  )
}

export default RemoconSection

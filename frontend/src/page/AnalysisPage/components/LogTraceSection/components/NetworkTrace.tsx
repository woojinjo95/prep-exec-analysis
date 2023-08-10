import React from 'react'
import { useQuery } from 'react-query'
import { Text } from '@global/ui'
import { Scrollbars } from 'react-custom-scrollbars-2'
import { Network } from '../api/entity'
import { getNetwork } from '../api/func'

// 차트 pin을 통해서 정해지는 전역적 시간 값
const tempTime = new Date('2023-08-08T14:49:40Z')

const NetworkTrace: React.FC = () => {
  const { data: networks } = useQuery<Network[]>(
    ['network'],
    () =>
      getNetwork({
        start_time: tempTime.toISOString(),
        end_time: new Date(tempTime.getTime() + 5 * 1000).toISOString(),
      }),
    {
      onSuccess: (res) => {
        console.log(res)
      },
      onError: (err) => {
        console.error(err)
      },
    },
  )

  return (
    <div className="w-full flex flex-col overflow-y-auto h-full overflow-x-hidden">
      <Scrollbars>
        {networks && (
          <>
            <div className="w-full grid grid-cols-[15%_9%_10%_6%_5%_55%] gap-x-2 text-[#8F949E] ">
              <Text size="sm" colorScheme="grey">
                Timestamp
              </Text>
              <Text size="sm" colorScheme="grey">
                Source
              </Text>
              <Text size="sm" colorScheme="grey">
                Destination
              </Text>
              <Text size="sm" colorScheme="grey">
                Protocol
              </Text>
              <Text size="sm" colorScheme="grey">
                Length
              </Text>
              <Text size="sm" colorScheme="grey">
                Info
              </Text>
            </div>
            <div className="flex flex-col w-full mt-1">
              {networks.map((network) => (
                <div
                  key={`network${network.timestamp}`}
                  className="w-full grid grid-cols-[15%_9%_10%_6%_5%_55%] gap-x-2 text-[#8F949E] text-sm"
                >
                  <Text size="sm" colorScheme="grey">
                    {network.timestamp.substring(0, network.timestamp.length - 6)}
                  </Text>
                  <Text size="sm" colorScheme="grey">
                    {network.source}
                  </Text>
                  <Text size="sm" colorScheme="grey">
                    {network.destination}
                  </Text>
                  <Text size="sm" colorScheme="grey">
                    {network.protocol}
                  </Text>
                  <Text size="sm" colorScheme="grey">
                    {network.length}
                  </Text>
                  <Text size="sm" colorScheme="grey" className="whitespace-pre-wrap">
                    {network.info}
                  </Text>
                </div>
              ))}
            </div>
          </>
        )}
      </Scrollbars>
    </div>
  )
}

export default NetworkTrace

import React from 'react'
import { Text } from '@global/ui'
import { Scrollbars } from 'react-custom-scrollbars-2'
import { useVideoSummary } from '@global/api/hook'
import { formatDateTo } from '@global/usecase'
import { useNetwork } from '../api/hook'

const NetworkTrace: React.FC = () => {
  const { videoSummary } = useVideoSummary()
  // FIXME: 시간 cursorDateTime에 맞춤
  const { networks } = useNetwork({
    start_time: videoSummary?.start_time!,
    end_time: videoSummary?.end_time!,
    enabled: !!videoSummary?.start_time,
  })

  return (
    <div className="w-full flex flex-col overflow-y-auto h-full overflow-x-hidden relative">
      <Scrollbars
        renderThumbVertical={({ ...props }) => <div {...props} className="bg-light-charcoal w-2 rounded-[5px]" />}
      >
        {networks && (
          <>
            <div className="w-[calc(100%-40px)] grid grid-cols-[16%_9%_10%_6%_5%_54%] gap-x-2 text-grey sticky top-0 bg-black">
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
              {networks.map(({ timestamp, source, destination, protocol, length, info }, index) => (
                <div
                  key={`network-trace-log-${timestamp}-${index}`}
                  className="w-[calc(100%-40px)] grid grid-cols-[16%_9%_10%_6%_5%_54%] gap-x-2 text-grey text-sm"
                >
                  <Text size="sm" colorScheme="grey">
                    {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}
                  </Text>
                  <Text size="sm" colorScheme="grey">
                    {source}
                  </Text>
                  <Text size="sm" colorScheme="grey">
                    {destination}
                  </Text>
                  <Text size="sm" colorScheme="grey">
                    {protocol}
                  </Text>
                  <Text size="sm" colorScheme="grey">
                    {length}
                  </Text>
                  <Text size="sm" colorScheme="grey" className="whitespace-pre-wrap">
                    {info}
                  </Text>
                </div>
              ))}
            </div>
          </>
        )}
      </Scrollbars>
      {/* <Button className="absolute top-0 right-6 border-none bg-black">
        <span className="text-base">Search</span>
      </Button>
      <Button className="absolute bottom-4 right-6 w-[132px] h-12 bg-charcoal rounded-3xl">
        <span className="text-base">Download</span>
      </Button> */}
    </div>
  )
}

export default NetworkTrace

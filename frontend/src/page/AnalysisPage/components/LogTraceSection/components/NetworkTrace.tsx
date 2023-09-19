import React from 'react'
import { useRecoilValue } from 'recoil'
import { Text } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import { cursorDateTimeState } from '@global/atom'
import ScrollComponent from '@global/ui/ScrollComponent'
import { useInfiniteNetwork } from '../api/hook'

/**
 * Network 로그 추적 영역
 */
const NetworkTrace: React.FC = () => {
  const cursorDateTime = useRecoilValue(cursorDateTimeState)
  const { networks, loadingRef, hasNextPage } = useInfiniteNetwork({
    start_time: cursorDateTime?.toISOString()!,
    enabled: !!cursorDateTime,
  })

  if (!networks) return null
  return (
    <div className="w-full flex flex-col overflow-y-auto h-full overflow-x-hidden relative">
      <div className="w-[calc(100%-40px)] grid grid-cols-[16%_9%_10%_6%_5%_54%] gap-x-2 text-grey bg-black">
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

      <ScrollComponent>
        <div className="flex flex-col w-full mt-1">
          {networks.map(({ timestamp, src, dst, protocol, length, info }, index) => (
            <div
              key={`network-trace-log-${timestamp}-${index}`}
              className="w-[calc(100%-40px)] grid grid-cols-[16%_9%_10%_6%_5%_54%] gap-x-2 text-grey text-sm"
            >
              <Text size="sm" colorScheme="grey">
                {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}
              </Text>
              <Text size="sm" colorScheme="grey">
                {src}
              </Text>
              <Text size="sm" colorScheme="grey">
                {dst}
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
        <div
          ref={loadingRef}
          className="p-2 flex items-center justify-center w-full"
          style={{ display: !hasNextPage ? 'none' : '' }}
        >
          {/* TODO: Loading spin 같은 로딩 UI가 필요 */}
          Loading...
        </div>
      </ScrollComponent>
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

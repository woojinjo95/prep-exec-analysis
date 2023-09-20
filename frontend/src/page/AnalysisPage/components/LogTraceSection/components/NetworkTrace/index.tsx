import React from 'react'
import { useRecoilValue } from 'recoil'
import { range } from 'd3'
import { Text, ScrollComponent } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import { cursorDateTimeState } from '@global/atom'
import { useInfiniteNetwork } from '../../api/hook'
import NetworkTraceRowLoading from './NetworkTraceRowLoading'

/**
 * Network 로그 추적 영역
 */
const NetworkTrace: React.FC = () => {
  const cursorDateTime = useRecoilValue(cursorDateTimeState)
  const { networks, isLoading, loadingRef, hasNextPage } = useInfiniteNetwork<HTMLTableRowElement>({
    start_time: cursorDateTime?.toISOString()!,
    enabled: !!cursorDateTime,
  })

  return (
    <div className="w-full h-full">
      <ScrollComponent>
        <table className="border-separate border-spacing-0 w-full">
          <colgroup>
            <col className="w-[166px]" />
            <col className="w-[11%]" />
            <col className="w-[11%]" />
            <col className="w-[6%]" />
            <col className="w-[6%]" />
            <col />
          </colgroup>
          <thead className="sticky top-0">
            <tr className="text-left bg-black">
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Timestamp
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Source
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Destination
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Protocol
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Length
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Info
                </Text>
              </th>
            </tr>
          </thead>

          {isLoading && (
            <tbody>
              {range(3).map((num) => (
                <NetworkTraceRowLoading key={`logcat-skeleton-${num}`} />
              ))}
            </tbody>
          )}

          {!!networks && (
            <tbody>
              {networks.map(({ timestamp, src, dst, protocol, length, info }, index) => (
                <tr key={`network-trace-log-${timestamp}-${index}`} className="hover:bg-light-black/50">
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey" className="truncate">
                      {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey" className="truncate">
                      {src}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey" className="truncate">
                      {dst}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey" className="truncate">
                      {protocol}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey">
                      {length}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey" className="whitespace-pre-wrap">
                      {info}
                    </Text>
                  </td>
                </tr>
              ))}

              <NetworkTraceRowLoading ref={loadingRef} style={{ display: !hasNextPage ? 'none' : '' }} />
            </tbody>
          )}
        </table>
      </ScrollComponent>
    </div>
  )
}

export default NetworkTrace

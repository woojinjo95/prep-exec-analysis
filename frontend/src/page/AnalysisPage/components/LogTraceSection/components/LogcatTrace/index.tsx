import React from 'react'
import { useRecoilValue } from 'recoil'
import { range } from 'd3'
import { ScrollComponent, Text } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import { cursorDateTimeState } from '@global/atom'
import { LogLevelColor } from '@global/constant'
import { useInfiniteLogcat } from '../../api/hook'
import LogcatTraceRowLoading from './LogcatTraceRowLoading'

/**
 * Logcat 로그 추적 영역
 */
const LogcatTrace: React.FC = () => {
  const cursorDateTime = useRecoilValue(cursorDateTimeState)
  const { logcats, loadingRef, hasNextPage } = useInfiniteLogcat<HTMLTableRowElement>({
    start_time: cursorDateTime?.toISOString()!,
    enabled: !!cursorDateTime,
  })

  return (
    <div className="w-full h-full">
      <ScrollComponent>
        <table className="border-separate border-spacing-0 w-full">
          <colgroup>
            <col className="w-[166px]" />
            <col className="w-[5%]" />
            <col className="w-[12%]" />
            <col className="w-[12%]" />
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
                <Text size="sm" colorScheme="grey" className="truncate">
                  Log Level
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Module
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Process
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  PID
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  TID
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Message
                </Text>
              </th>
            </tr>
          </thead>

          {!logcats && (
            <tbody>
              {range(3).map((num) => (
                <LogcatTraceRowLoading key={`logcat-skeleton-${num}`} />
              ))}
            </tbody>
          )}

          {!!logcats && (
            <tbody>
              {logcats.map(({ timestamp, module, log_level, process_name, pid, tid, message }, index) => (
                <tr key={`logcat-trace-log-${timestamp}-${index}`} className="hover:bg-light-black/50">
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey" className="truncate">
                      {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text
                      size="sm"
                      colorScheme={LogLevelColor[log_level]}
                      invertBackground
                      className="h-5 w-5 flex justify-center"
                    >
                      {log_level}
                    </Text>
                  </td>
                  <td className="px-2 max-w-[120px]">
                    <Text
                      size="sm"
                      colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}
                      className="break-all"
                    >
                      {module}
                    </Text>
                  </td>
                  <td className="px-2 max-w-[120px]">
                    <Text
                      size="sm"
                      colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}
                      className="break-all"
                    >
                      {process_name}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text
                      size="sm"
                      colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}
                      className="truncate"
                    >
                      {pid}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text
                      size="sm"
                      colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}
                      className="truncate"
                    >
                      {tid}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text
                      size="sm"
                      colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}
                      className="whitespace-pre-wrap"
                    >
                      {message}
                    </Text>
                  </td>
                </tr>
              ))}

              <LogcatTraceRowLoading ref={loadingRef} style={{ display: !hasNextPage ? 'none' : '' }} />
            </tbody>
          )}
        </table>
      </ScrollComponent>
    </div>
  )
}

export default LogcatTrace

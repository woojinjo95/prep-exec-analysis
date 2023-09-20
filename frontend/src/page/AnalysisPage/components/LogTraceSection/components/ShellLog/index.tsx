import React from 'react'
import { useRecoilValue } from 'recoil'
import { range } from 'd3'
import { cursorDateTimeState } from '@global/atom'
import { Text, ScrollComponent } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import { Shell } from '../../api/entity'
import { useInfiniteShellLogs } from '../../api/hook'
import ShellLogRowLoading from './ShellLogRowLoading'

interface ShellLogProps {
  shell_mode: Shell['mode']
}

/**
 * 쉘 로그 리스트 컴포넌트
 */
const ShellLog: React.FC<ShellLogProps> = ({ shell_mode }) => {
  const cursorDateTime = useRecoilValue(cursorDateTimeState)
  const { shellLogs, loadingRef, hasNextPage } = useInfiniteShellLogs<HTMLTableRowElement>({
    shell_mode,
    start_time: cursorDateTime?.toISOString()!,
    enabled: !!cursorDateTime,
  })

  return (
    <div className="w-full h-full">
      <ScrollComponent>
        <table className="border-separate border-spacing-0 w-full">
          <colgroup>
            <col className="w-[166px]" />
            <col className="w-[10%]" />
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
                  Module
                </Text>
              </th>
              <th className="px-2">
                <Text size="sm" colorScheme="grey">
                  Message
                </Text>
              </th>
            </tr>
          </thead>

          {!shellLogs && (
            <tbody>
              {range(3).map((num) => (
                <ShellLogRowLoading key={`logcat-skeleton-${num}`} />
              ))}
            </tbody>
          )}

          {!!shellLogs && (
            <tbody>
              {shellLogs.map(({ timestamp, module, message }, index) => (
                <tr
                  key={`shell-logs-${shell_mode}-${timestamp}-${module}-${index}`}
                  className="hover:bg-light-black/50"
                >
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey" className="truncate">
                      {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey" className="truncate">
                      {module}
                    </Text>
                  </td>
                  <td className="px-2">
                    <Text size="sm" colorScheme="grey">
                      {message}
                    </Text>
                  </td>
                </tr>
              ))}

              <ShellLogRowLoading ref={loadingRef} style={{ display: !hasNextPage ? 'none' : '' }} />
            </tbody>
          )}
        </table>
      </ScrollComponent>
    </div>
  )
}

export default ShellLog

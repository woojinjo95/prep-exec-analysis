import React from 'react'
import { useRecoilValue } from 'recoil'
import { cursorDateTimeState } from '@global/atom'
import { Text } from '@global/ui'
import Scrollbars from 'react-custom-scrollbars-2'
import { formatDateTo } from '@global/usecase'
import { Shell } from '../api/entity'
import { useInfiniteShellLogs } from '../api/hook'

interface ShellLogProps {
  shell_mode: Shell['mode']
}

/**
 * 쉘 로그 리스트 컴포넌트
 */
const ShellLog: React.FC<ShellLogProps> = ({ shell_mode }) => {
  const cursorDateTime = useRecoilValue(cursorDateTimeState)
  const { shellLogs, loadingRef, hasNextPage } = useInfiniteShellLogs({
    shell_mode,
    start_time: cursorDateTime?.toISOString()!,
    enabled: !!cursorDateTime,
  })

  return (
    <div className="w-full flex flex-col h-full overflow-x-hidden overflow-y-auto">
      <Scrollbars
        renderThumbVertical={({ ...props }) => <div {...props} className="bg-light-charcoal w-2 rounded-[5px]" />}
      >
        <div className="w-full grid grid-cols-[16%_9%_1fr] gap-2 sticky top-0 bg-black">
          <Text size="sm" colorScheme="grey">
            Timestamp
          </Text>
          <Text size="sm" colorScheme="grey">
            Module
          </Text>
          <Text size="sm" colorScheme="grey">
            Message
          </Text>
        </div>
        <div className="flex flex-col w-full mt-1">
          {shellLogs?.map(({ timestamp, module, message }, index) => (
            <div
              key={`shell-logs-${shell_mode}-${timestamp}-${module}-${index}`}
              className="w-full grid grid-cols-[16%_9%_1fr] gap-2"
            >
              <Text size="sm" colorScheme="grey">
                {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}
              </Text>
              <Text size="sm" colorScheme="grey">
                {module}
              </Text>
              <Text size="sm" colorScheme="grey">
                {message}
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
      </Scrollbars>
    </div>
  )
}

export default ShellLog

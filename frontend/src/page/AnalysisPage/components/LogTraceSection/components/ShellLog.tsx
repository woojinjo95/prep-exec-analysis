import React from 'react'
import { useRecoilValue } from 'recoil'
import Scrollbars from 'react-custom-scrollbars-2'
import { cursorDateTimeState } from '@global/atom'
import { Skeleton, Text } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import { ReactComponent as LoadingIcon } from '@assets/images/loading.svg'
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

  if (!shellLogs) return <Skeleton className="w-full h-full" colorScheme="dark" />
  return (
    <div className="w-full flex flex-col h-full overflow-x-hidden overflow-y-auto">
      <div className="w-full grid grid-cols-[16%_9%_1fr] gap-2 bg-black">
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

      <Scrollbars
        renderThumbVertical={({ ...props }) => <div {...props} className="bg-light-charcoal w-2 rounded-[5px]" />}
      >
        <div className="flex flex-col w-full mt-1">
          {shellLogs.map(({ timestamp, module, message }, index) => (
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
          <LoadingIcon className="fill-grey w-5 h-5 animate-spin" />
        </div>
      </Scrollbars>
    </div>
  )
}

export default ShellLog

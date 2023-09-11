import React from 'react'
import { useRecoilValue } from 'recoil'
import { Scrollbars } from 'react-custom-scrollbars-2'
import { Text } from '@global/ui'
import { formatDateTo } from '@global/usecase'
import { cursorDateTimeState } from '@global/atom'
import { LogLevelColor } from '@global/constant'
import { useLogcat } from '../api/hook'

/**
 * Logcat 로그 추적 영역
 */
const LogcatTrace: React.FC = () => {
  const cursorDateTime = useRecoilValue(cursorDateTimeState)
  const { logcats } = useLogcat({
    // cursorDateTime 기준 전후 30초씩(총 1분)
    start_time: new Date((cursorDateTime?.getTime() || 0) - 1000 * 30).toISOString(),
    end_time: new Date((cursorDateTime?.getTime() || 0) + 1000 * 30).toISOString(),
    enabled: !!cursorDateTime,
  })

  return (
    <div className="w-full flex flex-col h-full overflow-x-hidden overflow-y-auto">
      <Scrollbars
        renderThumbVertical={({ ...props }) => <div {...props} className="bg-light-charcoal w-2 rounded-[5px]" />}
      >
        <div className="w-[calc(100%-48px)] grid grid-cols-[16%_6%_9%_9%_5%_5%_50%] gap-x-2 text-grey sticky top-0 bg-black">
          <Text size="sm" colorScheme="grey">
            Timestamp
          </Text>
          <Text size="sm" colorScheme="grey">
            Log Level
          </Text>
          <Text size="sm" colorScheme="grey">
            Module
          </Text>
          <Text size="sm" colorScheme="grey">
            Process
          </Text>
          <Text size="sm" colorScheme="grey">
            Pid
          </Text>
          <Text size="sm" colorScheme="grey">
            Tid
          </Text>
          <Text size="sm" colorScheme="grey">
            Message
          </Text>
        </div>
        <div className="flex flex-col w-full mt-1">
          {logcats?.map(({ timestamp, module, log_level, process_name, pid, tid, message }, index) => (
            <div
              key={`logcat-trace-log-${timestamp}-${index}`}
              className="w-[calc(100%-48px)] grid grid-cols-[16%_6%_9%_9%_5%_5%_50%] gap-x-2 text-grey text-sm"
            >
              <Text size="sm" colorScheme="grey">
                {formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}
              </Text>
              <Text
                size="sm"
                colorScheme={LogLevelColor[log_level]}
                invertBackground
                className="h-5 w-5 flex justify-center"
              >
                {log_level}
              </Text>
              <Text size="sm" colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}>
                {module}
              </Text>
              <Text size="sm" colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}>
                {process_name}
              </Text>
              <Text size="sm" colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}>
                {pid}
              </Text>
              <Text size="sm" colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}>
                {tid}
              </Text>
              <Text
                size="sm"
                colorScheme={log_level !== 'I' ? LogLevelColor[log_level] : 'grey'}
                className="whitespace-pre-wrap"
              >
                {message}
              </Text>
            </div>
          ))}
        </div>
      </Scrollbars>
    </div>
  )
}

export default LogcatTrace

import React from 'react'
import { useQuery } from 'react-query'
import { Text } from '@global/ui'
import { Scrollbars } from 'react-custom-scrollbars-2'
import { Logcat } from '../api/entity'
import { getLogcat } from '../api/func'
import { LogcatLogLevelColors } from '../constants'

// 차트 pin을 통해서 정해지는 전역적 시간 값
const tempTime = new Date('2023-08-08T14:49:40Z')

const LogcatTrace: React.FC = () => {
  const { data: logcats } = useQuery<Logcat[]>(
    ['logcat'],
    () =>
      getLogcat({
        start_time: tempTime.toISOString(),
        end_time: new Date(tempTime.getTime() + 5 * 1000).toISOString(),
      }),
    {
      onError: (err) => {
        console.error(err)
      },
    },
  )

  return (
    <div className="w-full flex flex-col h-full overflow-x-hidden overflow-y-auto">
      <Scrollbars
        renderThumbVertical={({ ...props }) => <div {...props} className="bg-light-charcoal w-2 rounded-[5px]" />}
      >
        {logcats && (
          <>
            <div className="w-[calc(100%-48px)] grid grid-cols-[14%_6%_9%_9%_5%_5%_52%] gap-x-2 text-[#8F949E]">
              <Text size="sm" colorScheme="grey">
                Timestamp
              </Text>
              <Text size="sm" colorScheme="grey">
                log_level
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
              {logcats.map((logcat) => (
                <div
                  key={`logcat_${logcat.timestamp}`}
                  className="w-[calc(100%-48px)] grid grid-cols-[14%_6%_9%_9%_5%_5%_52%] gap-x-2 text-[#8F949E] text-sm"
                >
                  <Text size="sm" colorScheme="grey">
                    {logcat.timestamp.substring(0, logcat.timestamp.length - 6)}
                  </Text>
                  <Text
                    size="sm"
                    colorScheme={LogcatLogLevelColors[logcat.log_level]}
                    invertBackground
                    className="h-[20px] w-[20px] flex justify-center"
                  >
                    {logcat.log_level}
                  </Text>
                  <Text
                    size="sm"
                    colorScheme={logcat.log_level !== 'I' ? LogcatLogLevelColors[logcat.log_level] : 'grey'}
                  >
                    {logcat.module}
                  </Text>
                  <Text
                    size="sm"
                    colorScheme={logcat.log_level !== 'I' ? LogcatLogLevelColors[logcat.log_level] : 'grey'}
                  >
                    {logcat.process_name}
                  </Text>
                  <Text
                    size="sm"
                    colorScheme={logcat.log_level !== 'I' ? LogcatLogLevelColors[logcat.log_level] : 'grey'}
                  >
                    {logcat.pid}
                  </Text>
                  <Text
                    size="sm"
                    colorScheme={logcat.log_level !== 'I' ? LogcatLogLevelColors[logcat.log_level] : 'grey'}
                  >
                    {logcat.tid}
                  </Text>
                  <Text
                    size="sm"
                    colorScheme={logcat.log_level !== 'I' ? LogcatLogLevelColors[logcat.log_level] : 'grey'}
                    className="whitespace-pre-wrap"
                  >
                    {logcat.message}
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

export default LogcatTrace

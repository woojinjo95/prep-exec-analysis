import React from 'react'
import { Skeleton, Text } from '@global/ui'

const LogcatTraceRowLoading = React.forwardRef<
  HTMLTableRowElement,
  React.DetailedHTMLProps<React.HTMLAttributes<HTMLTableRowElement>, HTMLTableRowElement>
>((props, ref) => {
  return (
    <tr ref={ref} {...props} className="text-left bg-black h-6">
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            Timestamp
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey" className="truncate">
            Log Level
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            Module
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            Process
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            PID
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            TID
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            Message
          </Text>
        </Skeleton>
      </th>
    </tr>
  )
})

LogcatTraceRowLoading.displayName = 'LogcatTraceRowLoading'

export default LogcatTraceRowLoading

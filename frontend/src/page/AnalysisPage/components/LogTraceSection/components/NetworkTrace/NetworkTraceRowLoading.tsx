import React from 'react'
import { Skeleton, Text } from '@global/ui'

const NetworkTraceRowLoading = React.forwardRef<
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
          <Text size="sm" colorScheme="grey">
            Source
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            Destination
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            Protocol
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            Length
          </Text>
        </Skeleton>
      </th>
      <th className="px-2">
        <Skeleton colorScheme="dark" className="rounded-md h-[17px]">
          <Text size="sm" colorScheme="grey">
            Info
          </Text>
        </Skeleton>
      </th>
    </tr>
  )
})

NetworkTraceRowLoading.displayName = 'NetworkTraceRowLoading'

export default NetworkTraceRowLoading

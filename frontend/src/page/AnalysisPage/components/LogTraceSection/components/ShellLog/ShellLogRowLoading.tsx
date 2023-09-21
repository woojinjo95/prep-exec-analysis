import React from 'react'
import { Skeleton, Text } from '@global/ui'

const ShellLogRowLoading = React.forwardRef<
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
            Module
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

ShellLogRowLoading.displayName = 'ShellLogRowLoading'

export default ShellLogRowLoading

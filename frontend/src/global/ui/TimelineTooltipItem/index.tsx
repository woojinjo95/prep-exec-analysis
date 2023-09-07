import React from 'react'
import { Text } from '@global/ui'

interface TimelineTooltipItemProps {
  label: string
  children: React.ReactNode
}

/**
 * TimelineTooltip 컴포넌트 내부에서 사용하는 테이블 Row 컴포넌트
 *
 * @param label Row 이름
 */
const TimelineTooltipItem: React.FC<TimelineTooltipItemProps> = ({ label, children }) => {
  return (
    <tr>
      <th className="border-r border-b border-charcoal bg-charcoal py-2 px-4 text-left">
        <Text colorScheme="light" weight="medium" className="truncate">
          {label}
        </Text>
      </th>
      <td className="border-r border-b border-charcoal py-2 px-4 text-left break-all">{children}</td>
    </tr>
  )
}

export default TimelineTooltipItem

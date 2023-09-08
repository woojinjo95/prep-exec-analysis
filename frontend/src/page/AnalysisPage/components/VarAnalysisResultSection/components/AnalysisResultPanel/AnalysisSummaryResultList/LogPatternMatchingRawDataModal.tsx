import React from 'react'
import cx from 'classnames'
import { useSetRecoilState } from 'recoil'
import { CardModal, SimpleButton, Text } from '@global/ui'
import { ReactComponent as ShowIcon } from '@assets/images/icon_raw_data.svg'
import { useInfiniteLogPatternMatching } from '@page/AnalysisPage/api/hook'
import { formatDateTo, numberWithCommas } from '@global/usecase'
import { cursorDateTimeState } from '@global/atom'
import { AnalysisTypeLabel } from '../../../constant'

interface LogPatternMatchingRawDataModalProps {
  isOpen: boolean
  onClose: () => void
  startTime: string
  endTime: string
}

/**
 * Log Pattern Matching 원본데이터 모달
 */
const LogPatternMatchingRawDataModal: React.FC<LogPatternMatchingRawDataModalProps> = ({
  isOpen,
  onClose,
  startTime,
  endTime,
}) => {
  const { logPatternMatching, total, loadingRef, hasNextPage } = useInfiniteLogPatternMatching({
    start_time: startTime,
    end_time: endTime,
  })
  const setCursorDateTime = useSetRecoilState(cursorDateTimeState)

  if (!logPatternMatching) return null
  return (
    <CardModal
      isOpen={isOpen}
      onClose={onClose}
      title={AnalysisTypeLabel.log_pattern_matching}
      subtitle={`${numberWithCommas(total)} times`}
    >
      <div className="h-full w-full overflow-y-auto">
        <table className="border-separate border-spacing-0 w-full">
          <thead className="sticky top-0">
            <tr className="text-left">
              <th className="px-6 py-1 bg-charcoal border border-r-0 border-light-charcoal">
                <Text size="sm" weight="medium">
                  Timestamp
                </Text>
              </th>
              <th className="px-6 py-1 bg-charcoal border-t border-b border-light-charcoal whitespace-nowrap">
                <Text size="sm" weight="medium">
                  Log Pattern Name
                </Text>
              </th>
              <th className="px-6 py-1 bg-charcoal border-t border-b border-light-charcoal whitespace-nowrap">
                <Text size="sm" weight="medium">
                  Log Level
                </Text>
              </th>
              <th className="px-6 py-1 bg-charcoal border-t border-b border-light-charcoal">
                <Text size="sm" weight="medium">
                  Message
                </Text>
              </th>
              <th className="px-6 py-1 bg-charcoal border border-l-0 border-light-charcoal text-center">
                <Text size="sm" weight="medium">
                  Result
                </Text>
              </th>
            </tr>
          </thead>
          <tbody>
            {logPatternMatching.map(({ timestamp, log_pattern_name, log_level, message }, index) => (
              <tr
                key={`log-pattern-matching-raw-data-${timestamp}-${index}`}
                className="border-t border-light-charcoal hover:bg-charcoal/50"
              >
                <td className={cx('px-6 py-1 whitespace-nowrap', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}</Text>
                </td>
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{log_pattern_name}</Text>
                </td>
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{log_level}</Text>
                </td>
                <td className={cx('px-6 py-1 break-all', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{message}</Text>
                </td>
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <SimpleButton
                    isIcon
                    colorScheme="charcoal"
                    onClick={() => setCursorDateTime(new Date(timestamp))}
                    className="mx-auto"
                  >
                    <ShowIcon className="w-3 h-3" />
                  </SimpleButton>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <div
          ref={loadingRef}
          className="p-2 flex items-center justify-center w-full"
          style={{ display: !hasNextPage ? 'none' : '' }}
        >
          {/* TODO: Loading spin 같은 로딩 UI가 필요 */}
          Loading...
        </div>
      </div>
    </CardModal>
  )
}

export default LogPatternMatchingRawDataModal

import React, { useState } from 'react'
import cx from 'classnames'
import { useSetRecoilState } from 'recoil'
import { CardModal, SimpleButton, Text, SortButton } from '@global/ui'
import { ReactComponent as ShowIcon } from '@assets/images/icon_raw_data.svg'
import { convertRegexStringToHTML, formatDateTo, numberWithCommas } from '@global/usecase'
import { cursorDateTimeState } from '@global/atom'
import { AnalysisTypeLabel, LogLevelColor } from '@global/constant'
import { useInfiniteLogPatternMatching } from '@page/AnalysisPage/api/hook'

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
  const [sortBy, setSortBy] = useState<Parameters<typeof useInfiniteLogPatternMatching>[0]['sort_by']>('timestamp')
  const [sortDesc, setSortDesc] = useState<boolean>(false)
  const { logPatternMatching, total, loadingRef, hasNextPage } = useInfiniteLogPatternMatching({
    start_time: startTime,
    end_time: endTime,
    sort_by: sortBy,
    sort_desc: sortDesc,
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
                <div className="flex items-center gap-x-2">
                  <Text size="sm" weight="medium">
                    Timestamp
                  </Text>
                  <SortButton
                    value="timestamp"
                    sortBy={sortBy}
                    setSortBy={setSortBy}
                    sortDesc={sortDesc}
                    setSortDesc={setSortDesc}
                  />
                </div>
              </th>
              <th className="px-6 py-1 bg-charcoal border-t border-b border-light-charcoal whitespace-nowrap">
                <div className="flex items-center gap-x-2">
                  <Text size="sm" weight="medium">
                    Log Pattern Name
                  </Text>
                  <SortButton
                    value="log_pattern_name"
                    sortBy={sortBy}
                    setSortBy={setSortBy}
                    sortDesc={sortDesc}
                    setSortDesc={setSortDesc}
                  />
                </div>
              </th>
              <th className="px-6 py-1 bg-charcoal border-t border-b border-light-charcoal whitespace-nowrap">
                <div className="flex items-center gap-x-2">
                  <Text size="sm" weight="medium">
                    Log Level
                  </Text>
                  <SortButton
                    value="log_level"
                    sortBy={sortBy}
                    setSortBy={setSortBy}
                    sortDesc={sortDesc}
                    setSortDesc={setSortDesc}
                  />
                </div>
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
            {logPatternMatching.map(({ timestamp, log_pattern_name, log_level, message, regex, color }, index) => (
              <tr
                key={`log-pattern-matching-raw-data-${timestamp}-${index}`}
                className="border-t border-light-charcoal hover:bg-charcoal/50"
              >
                <td className={cx('px-6 py-1 whitespace-nowrap', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}</Text>
                </td>
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <div className="flex items-center gap-x-2">
                    <div className="w-4 h-4" style={{ backgroundColor: color }} />
                    <Text size="sm">{log_pattern_name}</Text>
                  </div>
                </td>
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text colorScheme={LogLevelColor[log_level]} invertBackground>
                    {log_level}
                  </Text>
                </td>
                <td className={cx('px-6 py-1 break-all', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">
                    <div
                      // eslint-disable-next-line react/no-danger
                      dangerouslySetInnerHTML={{
                        __html: convertRegexStringToHTML(message, regex, '#00B1FF'),
                      }}
                      className="text-white"
                    />
                  </Text>
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

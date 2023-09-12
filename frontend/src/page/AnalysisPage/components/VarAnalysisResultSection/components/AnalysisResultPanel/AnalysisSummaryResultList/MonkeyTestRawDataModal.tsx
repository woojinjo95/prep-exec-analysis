import React, { useState } from 'react'
import cx from 'classnames'
import { useSetRecoilState } from 'recoil'
import { CardModal, SimpleButton, SortButton, Text } from '@global/ui'
import { formatDateTo, numberWithCommas } from '@global/usecase'
import { ReactComponent as ShowIcon } from '@assets/images/icon_raw_data.svg'
import { useInfiniteMonkeySmartSense } from '@page/AnalysisPage/api/hook'
import { cursorDateTimeState } from '@global/atom'
import { AnalysisTypeLabel } from '../../../constant'

interface MonkeyTestRawDataModalProps {
  isOpen: boolean
  onClose: () => void
  startTime: string
  endTime: string
}

/**
 * Monkey Test 원본데이터 모달
 */
const MonkeyTestRawDataModal: React.FC<MonkeyTestRawDataModalProps> = ({ isOpen, onClose, startTime, endTime }) => {
  const [sortBy, setSortBy] = useState<Parameters<typeof useInfiniteMonkeySmartSense>[0]['sort_by']>('timestamp')
  const [sortDesc, setSortDesc] = useState<boolean>(false)
  const { monkeySmartSense, total, loadingRef, hasNextPage } = useInfiniteMonkeySmartSense({
    start_time: startTime,
    end_time: endTime,
    sort_by: sortBy,
    sort_desc: sortDesc,
  })
  const setCursorDateTime = useSetRecoilState(cursorDateTimeState)

  if (!monkeySmartSense) return null
  return (
    <CardModal
      isOpen={isOpen}
      onClose={onClose}
      title={AnalysisTypeLabel.monkey_test}
      subtitle={`${numberWithCommas(total)} times`}
    >
      <div className="h-full w-full overflow-y-auto">
        <table className="border-separate border-spacing-0 w-full">
          <thead className="sticky top-0">
            <tr className="text-left">
              <th className="px-6 py-1 bg-charcoal border border-r-0 border-light-charcoal flex items-center gap-x-2">
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
              <th className="px-6 py-1 bg-charcoal border-t border-b border-light-charcoal">
                <div className="flex items-center gap-x-2">
                  <Text size="sm" weight="medium">
                    Smart Sense Key
                  </Text>
                  <SortButton
                    value="smart_sense_key"
                    sortBy={sortBy}
                    setSortBy={setSortBy}
                    sortDesc={sortDesc}
                    setSortDesc={setSortDesc}
                  />
                </div>
              </th>
              <th className="px-6 py-1 bg-charcoal border border-l-0 border-light-charcoal text-center">
                <Text size="sm" weight="medium">
                  Result
                </Text>
              </th>
            </tr>
          </thead>
          <tbody>
            {monkeySmartSense.map(({ timestamp, smart_sense_key }, index) => (
              <tr
                key={`freeze-raw-data-${timestamp}-${index}`}
                className="border-t border-light-charcoal hover:bg-charcoal/50"
              >
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}</Text>
                </td>
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{smart_sense_key.join(', ')}</Text>
                </td>
                <td className={cx('px-6 py-1 flex justify-center', { 'border-t border-light-charcoal': index !== 0 })}>
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

export default MonkeyTestRawDataModal

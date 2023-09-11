import React, { useState } from 'react'
import cx from 'classnames'
import { useSetRecoilState } from 'recoil'
import { CardModal, IconButton, SortButton, Text } from '@global/ui'
import { convertDuration, formatDateTo, numberWithCommas } from '@global/usecase'
import { ReactComponent as PlayIcon } from '@assets/images/icon_play.svg'
import { useInfiniteBoot } from '@page/AnalysisPage/api/hook'
import { cursorDateTimeState } from '@global/atom'
import { AnalysisTypeLabel, BootTypeLabel } from '../../../constant'

interface BootRawDataModalProps {
  isOpen: boolean
  onClose: () => void
  startTime: string
  endTime: string
}

/**
 * Boot 원본데이터 모달
 */
const BootRawDataModal: React.FC<BootRawDataModalProps> = ({ isOpen, onClose, startTime, endTime }) => {
  const [sortBy, setSortBy] = useState<Parameters<typeof useInfiniteBoot>[0]['sort_by']>('timestamp')
  const [sortDesc, setSortDesc] = useState<boolean>(false)
  const { boot, total, loadingRef, hasNextPage } = useInfiniteBoot({
    start_time: startTime,
    end_time: endTime,
    sort_by: sortBy,
    sort_desc: sortDesc,
  })
  const setCursorDateTime = useSetRecoilState(cursorDateTimeState)

  if (!boot) return null
  return (
    <CardModal
      isOpen={isOpen}
      onClose={onClose}
      title={AnalysisTypeLabel.boot}
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
              <th className="px-6 py-1 bg-charcoal border-t border-b border-light-charcoal">
                <div className="flex items-center gap-x-2">
                  <Text size="sm" weight="medium">
                    Error Type
                  </Text>
                  <SortButton
                    value="target"
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
                    Duration Time
                  </Text>
                  <SortButton
                    value="measure_time"
                    sortBy={sortBy}
                    setSortBy={setSortBy}
                    sortDesc={sortDesc}
                    setSortDesc={setSortDesc}
                  />
                </div>
              </th>
              <th className="px-6 py-1 bg-charcoal border border-l-0 border-light-charcoal text-center">
                <Text size="sm" weight="medium">
                  Result Video
                </Text>
              </th>
            </tr>
          </thead>
          <tbody>
            {boot.map(({ timestamp, measure_time, target }, index) => (
              <tr
                key={`boot-raw-data-${timestamp}-${index}`}
                className="border-t border-light-charcoal hover:bg-charcoal/50"
              >
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{formatDateTo('YYYY-MM-DD HH:MM:SS:MS', new Date(timestamp))}</Text>
                </td>
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{BootTypeLabel[target]}</Text>
                </td>
                <td className={cx('px-6 py-1', { 'border-t border-light-charcoal': index !== 0 })}>
                  <Text size="sm">{convertDuration(measure_time)}</Text>
                </td>
                <td className={cx('px-6 py-1 flex justify-center', { 'border-t border-light-charcoal': index !== 0 })}>
                  <IconButton
                    icon={<PlayIcon className="!h-3" />}
                    colorScheme="charcoal"
                    size="sm"
                    onClick={() => setCursorDateTime(new Date(timestamp))}
                  />
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

export default BootRawDataModal

import React from 'react'
import { useRecoilState } from 'recoil'
import { Accordion, SimpleButton, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { numberWithCommas } from '@global/usecase'
import { logPatternMatchingNameFilterListState } from '@global/atom'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { AnalysisTypeLabel } from '../../../constant'

interface LogPatternMatchingSummaryItemProps {
  logPatternMatching: NonNullable<AnalysisResultSummary['log_pattern_matching']>
  setRawDataModalType: React.Dispatch<React.SetStateAction<keyof AnalysisResultSummary | null>>
}

/**
 * log pattern matching 분석 결과 아이템
 */
const LogPatternMatchingSummaryItem: React.FC<LogPatternMatchingSummaryItemProps> = ({
  logPatternMatching,
  setRawDataModalType,
}) => {
  const [logPatternMatchingNameFilterList, setLogPatternMatchingNameFilterList] = useRecoilState(
    logPatternMatchingNameFilterListState,
  )

  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: logPatternMatching.color,
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.log_pattern_matching}
            </Text>
          </div>

          <Text weight="medium">
            {numberWithCommas(logPatternMatching.results.reduce((acc, curr) => acc + curr.total, 0))} times
          </Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-4 pt-1">
        <div className="grid grid-cols-[1fr_auto_auto] gap-x-4 gap-y-1 items-center">
          {/* header */}
          <Text weight="medium" size="sm">
            Log Pattern Name
          </Text>
          <Text weight="medium" size="sm">
            Total
          </Text>
          <div />

          {logPatternMatching.results.map(({ total, log_pattern_name, color }, index) => (
            <React.Fragment key={`log-pattern-matching-summary-result-${index}`}>
              <div className="flex items-center gap-x-3">
                <div
                  className="w-4 h-4"
                  style={{
                    backgroundColor: color,
                  }}
                />
                <Text size="sm">{log_pattern_name}</Text>
              </div>
              <Text size="sm" className="text-right">
                {numberWithCommas(total)}
              </Text>
              {logPatternMatchingNameFilterList.includes(log_pattern_name) ? (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() =>
                    setLogPatternMatchingNameFilterList((prev) => prev.filter((type) => type !== log_pattern_name))
                  }
                >
                  <HiddenEyeIcon className="h-4 w-5" />
                </SimpleButton>
              ) : (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() => setLogPatternMatchingNameFilterList((prev) => [...prev, log_pattern_name])}
                >
                  <ShowEyeIcon className="h-4 w-5" />
                </SimpleButton>
              )}
            </React.Fragment>
          ))}
        </div>

        <SimpleButton
          colorScheme="charcoal"
          className="ml-auto"
          onClick={() => setRawDataModalType('log_pattern_matching')}
        >
          <ShowRawDataIcon className="w-4 h-4" />
          <Text colorScheme="light" weight="medium">
            Show Raw Data
          </Text>
        </SimpleButton>
      </div>
    </Accordion>
  )
}

export default LogPatternMatchingSummaryItem

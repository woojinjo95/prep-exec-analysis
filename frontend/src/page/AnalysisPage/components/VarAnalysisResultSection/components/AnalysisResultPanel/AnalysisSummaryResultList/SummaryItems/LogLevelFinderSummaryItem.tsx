import React, { useEffect } from 'react'
import { useRecoilState } from 'recoil'
import { Accordion, SimpleButton, Text } from '@global/ui'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { numberWithCommas } from '@global/usecase'
import { logLevelFinderLogLevelFilterListState } from '@global/atom'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { AnalysisTypeLabel } from '@global/constant'

interface LogLevelFinderSummaryItemProps {
  logLevelFinder: NonNullable<AnalysisResultSummary['log_level_finder']>
}

/**
 * log level finder 분석결과 요약 아이템
 */
const LogLevelFinderSummaryItem: React.FC<LogLevelFinderSummaryItemProps> = ({ logLevelFinder }) => {
  const [logLevelFinderLogLevelFilterList, setLogLevelFinderLogLevelFilterList] = useRecoilState(
    logLevelFinderLogLevelFilterListState,
  )

  useEffect(() => {
    setLogLevelFinderLogLevelFilterList([])
  }, [])

  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: logLevelFinder.color,
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.log_level_finder}
            </Text>
          </div>

          <Text size="sm" weight="medium">
            {numberWithCommas(logLevelFinder.results.reduce((acc, curr) => acc + curr.total, 0))} times
          </Text>
        </div>
      }
    >
      <div className="grid grid-cols-[1fr_auto_auto] gap-x-4 gap-y-1 pt-1 items-center">
        {/* header */}
        <Text weight="medium" size="sm">
          Target
        </Text>
        <Text weight="medium" size="sm">
          Total
        </Text>
        <div />

        {logLevelFinder.results.map(({ total, target }, index) => (
          <React.Fragment key={`log-level-finder-summary-result-${index}`}>
            <Text size="sm">Logcat {target}</Text>
            <Text size="sm" className="text-right">
              {numberWithCommas(total)}
            </Text>
            {logLevelFinderLogLevelFilterList.includes(target) ? (
              <SimpleButton
                isIcon
                colorScheme="charcoal"
                onClick={() => setLogLevelFinderLogLevelFilterList((prev) => prev.filter((type) => type !== target))}
              >
                <HiddenEyeIcon className="h-4 w-5" />
              </SimpleButton>
            ) : (
              <SimpleButton
                isIcon
                colorScheme="charcoal"
                onClick={() => setLogLevelFinderLogLevelFilterList((prev) => [...prev, target])}
              >
                <ShowEyeIcon className="h-4 w-5" />
              </SimpleButton>
            )}
          </React.Fragment>
        ))}
      </div>
    </Accordion>
  )
}

export default LogLevelFinderSummaryItem

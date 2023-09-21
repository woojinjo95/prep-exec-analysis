import React, { useEffect } from 'react'
import { useRecoilState } from 'recoil'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { Accordion, SimpleButton, Text } from '@global/ui'
import { convertDuration, numberWithCommas } from '@global/usecase'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { monkeyTestIdFilterListState } from '@global/atom'
import { AnalysisTypeLabel } from '@global/constant'

interface MonkeyTestSummaryItemProps {
  monkeyTest: NonNullable<AnalysisResultSummary['monkey_test']>
  setRawDataModalType: React.Dispatch<React.SetStateAction<keyof AnalysisResultSummary | null>>
}

/**
 * monkey test 분석 결과 요약 아이템
 */
const MonkeyTestSummaryItem: React.FC<MonkeyTestSummaryItemProps> = ({ monkeyTest, setRawDataModalType }) => {
  const [monkeyTestIdFilterList, setMonkeyTestIdFilterList] = useRecoilState(monkeyTestIdFilterListState)

  useEffect(() => {
    setMonkeyTestIdFilterList([])
  }, [])

  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: monkeyTest.color,
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.monkey_test}
            </Text>
          </div>

          <Text size="sm" weight="medium">
            {numberWithCommas(monkeyTest.results.length)} times
          </Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-4 pt-1">
        <div className="grid grid-cols-[1fr_auto_auto_auto] gap-x-4 gap-y-1 items-center">
          {/* header */}
          <Text weight="medium" size="sm">
            No.
          </Text>
          <Text weight="medium" size="sm">
            Duration Time
          </Text>
          <Text weight="medium" size="sm" className="ml-4">
            Smart Sense
          </Text>
          <div />

          {monkeyTest.results.map(({ id, duration_time, smart_sense }, index) => (
            <React.Fragment key={`monkey-test-summary-result-item-${index}`}>
              <Text size="sm">{index + 1}</Text>
              <Text size="sm" className="text-right">
                {convertDuration(duration_time)}
              </Text>
              <Text size="sm" className="text-right">
                {numberWithCommas(smart_sense)} times
              </Text>
              {monkeyTestIdFilterList.includes(id) ? (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() => setMonkeyTestIdFilterList((prev) => prev.filter((type) => type !== id))}
                >
                  <HiddenEyeIcon className="h-4 w-5" />
                </SimpleButton>
              ) : (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() => setMonkeyTestIdFilterList((prev) => [...prev, id])}
                >
                  <ShowEyeIcon className="h-4 w-5" />
                </SimpleButton>
              )}
            </React.Fragment>
          ))}
        </div>

        <SimpleButton colorScheme="charcoal" className="ml-auto" onClick={() => setRawDataModalType('monkey_test')}>
          <ShowRawDataIcon className="w-4 h-4" />
          <Text colorScheme="light" weight="medium">
            Show Raw Data
          </Text>
        </SimpleButton>
      </div>
    </Accordion>
  )
}

export default MonkeyTestSummaryItem

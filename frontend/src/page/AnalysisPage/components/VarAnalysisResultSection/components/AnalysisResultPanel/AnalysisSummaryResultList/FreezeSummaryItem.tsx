import React from 'react'
import { useRecoilState } from 'recoil'
import { Accordion, SimpleButton, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { numberWithCommas } from '@global/usecase'
import { freezeTypeFilterListState } from '@global/atom'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { AnalysisTypeLabel } from '@global/constant'
import { FreezeTypeLabel } from '../../../constant'

interface FreezeSummaryItemProps {
  freeze: NonNullable<AnalysisResultSummary['freeze']>
  setRawDataModalType: React.Dispatch<React.SetStateAction<keyof AnalysisResultSummary | null>>
}

/**
 * freeze 분석결과 요약 아이템
 */
const FreezeSummaryItem: React.FC<FreezeSummaryItemProps> = ({ freeze, setRawDataModalType }) => {
  const [freezeTypeFilterList, setFreezeTypeFilterList] = useRecoilState(freezeTypeFilterListState)

  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: freeze.color,
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.freeze}
            </Text>
          </div>

          <Text weight="medium">
            {numberWithCommas(freeze.results.reduce((acc, curr) => acc + curr.total, 0))} times
          </Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-4 pt-1">
        <div className="grid grid-cols-[1fr_auto_auto] gap-x-4 gap-y-1 items-center">
          {/* header */}
          <Text weight="medium" size="sm">
            Error Type
          </Text>
          <Text weight="medium" size="sm">
            Total
          </Text>
          <div />

          {freeze.results.map(({ total, error_type }, index) => (
            <React.Fragment key={`freeze-summary-result-${index}`}>
              <Text size="sm">{FreezeTypeLabel[error_type]}</Text>
              <Text size="sm" className="text-right">
                {numberWithCommas(total)}
              </Text>
              {freezeTypeFilterList.includes(error_type) ? (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() => setFreezeTypeFilterList((prev) => prev.filter((type) => type !== error_type))}
                >
                  <HiddenEyeIcon className="h-4 w-5" />
                </SimpleButton>
              ) : (
                <SimpleButton
                  colorScheme="charcoal"
                  isIcon
                  onClick={() => setFreezeTypeFilterList((prev) => [...prev, error_type])}
                >
                  <ShowEyeIcon className="h-4 w-5" />
                </SimpleButton>
              )}
            </React.Fragment>
          ))}
        </div>

        <SimpleButton colorScheme="charcoal" className="ml-auto" onClick={() => setRawDataModalType('freeze')}>
          <ShowRawDataIcon className="w-4 h-4" />
          <Text colorScheme="light" weight="medium">
            Show Raw Data
          </Text>
        </SimpleButton>
      </div>
    </Accordion>
  )
}

export default FreezeSummaryItem

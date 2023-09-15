import React, { useState } from 'react'
import { useRecoilState } from 'recoil'
import { AnalysisTypeLabel, AppURL } from '@global/constant'
import { numberWithCommas } from '@global/usecase'
import { Accordion, SimpleButton, Text } from '@global/ui'
import { intelligentMonkeyTestSectionIdFilterListState } from '@global/atom'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import ZoomInImageModal from './ZoomInImageModal'

interface IntelligentMonkeyTestSummaryItemProps {
  intelligentMonkeyTest: NonNullable<AnalysisResultSummary['intelligent_monkey_test']>
  setRawDataModalType: React.Dispatch<React.SetStateAction<keyof AnalysisResultSummary | null>>
}

/**
 * intelligent monkey test 분석 결과 요약 아이템
 */
const IntelligentMonkeyTestSummaryItem: React.FC<IntelligentMonkeyTestSummaryItemProps> = ({
  intelligentMonkeyTest,
  setRawDataModalType,
}) => {
  const [intelligentMonkeyTestSectionIdFilterList, setIntelligentMonkeyTestSectionIdFilterList] = useRecoilState(
    intelligentMonkeyTestSectionIdFilterListState,
  )
  const [zoomInImagePath, setZoomInImagePath] = useState<string | null>(null)

  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: intelligentMonkeyTest.color,
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.intelligent_monkey_test}
            </Text>
          </div>

          <Text weight="medium">{numberWithCommas(intelligentMonkeyTest.results.length)} Menus</Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-4 pt-1">
        <div className="grid grid-cols-[auto_1fr_auto_auto] gap-x-4 gap-y-1 items-center">
          {/* header */}
          <Text weight="medium" size="sm">
            Menu
          </Text>
          <Text weight="medium" size="sm" className="pl-3">
            Image
          </Text>
          <Text weight="medium" size="sm" className="ml-4">
            Smart Sense
          </Text>
          <div />

          {intelligentMonkeyTest.results.map(({ section_id, smart_sense, image_path }, index) => (
            <React.Fragment key={`monkey-test-summary-result-item-${index}`}>
              <Text size="sm"># {numberWithCommas(section_id + 1)}</Text>
              <div className="flex items-center">
                <SimpleButton colorScheme="charcoal" onClick={() => setZoomInImagePath(image_path)}>
                  <img
                    className="h-6"
                    src={`${AppURL.backendURL}/api/v1/file/download?path=${image_path}`}
                    alt="intelligent monkey test menu img"
                  />
                </SimpleButton>
              </div>
              <Text size="sm" className="text-right">
                {numberWithCommas(smart_sense)} times
              </Text>
              {intelligentMonkeyTestSectionIdFilterList.includes(section_id) ? (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() =>
                    setIntelligentMonkeyTestSectionIdFilterList((prev) => prev.filter((type) => type !== section_id))
                  }
                >
                  <HiddenEyeIcon className="h-4 w-5" />
                </SimpleButton>
              ) : (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() => setIntelligentMonkeyTestSectionIdFilterList((prev) => [...prev, section_id])}
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
          onClick={() => setRawDataModalType('intelligent_monkey_test')}
        >
          <ShowRawDataIcon className="w-4 h-4" />
          <Text colorScheme="light" weight="medium">
            Show Raw Data
          </Text>
        </SimpleButton>

        {!!zoomInImagePath && (
          <ZoomInImageModal
            isOpen={!!zoomInImagePath}
            close={() => setZoomInImagePath(null)}
            imagePath={zoomInImagePath}
          />
        )}
      </div>
    </Accordion>
  )
}

export default IntelligentMonkeyTestSummaryItem

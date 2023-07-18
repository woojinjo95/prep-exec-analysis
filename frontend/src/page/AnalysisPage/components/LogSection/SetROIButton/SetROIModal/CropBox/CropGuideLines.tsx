import React from 'react'

/**
 * 행 또는 열의 가이드라인 개수
 */
const LINE_COUNT = 2

interface CropGuideLinesProps {
  cropTwoPosX: [number, number]
  cropTwoPosY: [number, number]
}

/**
 * 크롭 영역 가이드 라인들 컴포넌트
 */
const CropGuideLines: React.FC<CropGuideLinesProps> = ({ cropTwoPosX, cropTwoPosY }) => {
  return [...new Array(LINE_COUNT).keys()].map((num) => (
    <React.Fragment key={`crop-guide-line-${num}`}>
      {/* 가로 */}
      <div
        className="absolute top-0 left-0 w-full border-[0.5px] border-dashed border-gray-300/60"
        style={{
          transform: `translateY(${((num + 1) / (LINE_COUNT + 1)) * Math.abs(cropTwoPosY[0] - cropTwoPosY[1])}px)`,
        }}
      />
      {/* 세로 */}
      <div
        className="absolute top-0 left-0 h-full border-[0.5px] border-dashed border-gray-300/60"
        style={{
          transform: `translateX(${((num + 1) / (LINE_COUNT + 1)) * Math.abs(cropTwoPosX[0] - cropTwoPosX[1])}px)`,
        }}
      />
    </React.Fragment>
  ))
}

export default CropGuideLines

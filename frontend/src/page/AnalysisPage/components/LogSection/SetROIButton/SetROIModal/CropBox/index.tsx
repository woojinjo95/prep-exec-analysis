import React, { useState } from 'react'
import cx from 'classnames'
import CropGuideLines from './CropGuideLines'
import ResizingPoints from './ResizingPoints'

interface CropBoxProps {
  cropWidth: number
  cropHeight: number
  setCropWidth: React.Dispatch<React.SetStateAction<number | null>>
  setCropHeight: React.Dispatch<React.SetStateAction<number | null>>
}

/**
 * 비디오 크롭 영역
 */
const CropBox: React.FC<CropBoxProps> = ({ cropWidth, cropHeight, setCropWidth, setCropHeight }) => {
  const [isDragging, setIsDragging] = useState<boolean>(false)
  const [cropPosX, setCropPosX] = useState<number>(0)
  const [cropPosY, setCropPosY] = useState<number>(0)

  return (
    <div
      draggable={false}
      className={cx('absolute top-0 left-0 z-10 backdrop-brightness-[4] cursor-grab transition-colors', {
        'cursor-grabbing': isDragging,
        'hover:bg-white/10': !isDragging,
        '!bg-none': isDragging,
      })}
      style={{
        transform: `translate(${cropPosX}px, ${cropPosY}px)`,
        width: cropWidth,
        height: cropHeight,
      }}
      onPointerDown={(e) => {
        e.currentTarget.setPointerCapture(e.pointerId)
        setIsDragging(true)
      }}
      onPointerMove={(e) => {
        if (!isDragging) return

        setCropPosX((prev) => prev + e.movementX)
        setCropPosY((prev) => prev + e.movementY)
      }}
      onPointerUp={(e) => {
        e.currentTarget.releasePointerCapture(e.pointerId)
        setIsDragging(false)
      }}
    >
      <div className="w-full h-full border border-red-500 outline outline-8 -outline-offset-4 outline-red-500/20" />
      <CropGuideLines cropWidth={cropWidth} cropHeight={cropHeight} />
      <ResizingPoints
        setCropPosX={setCropPosX}
        setCropPosY={setCropPosY}
        setCropWidth={setCropWidth}
        setCropHeight={setCropHeight}
      />
    </div>
  )
}

export default CropBox

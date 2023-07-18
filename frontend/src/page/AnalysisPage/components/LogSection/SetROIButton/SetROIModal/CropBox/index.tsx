import React, { useState } from 'react'
import cx from 'classnames'
import CropGuideLines from './CropGuideLines'
import ResizingPoints from './ResizingPoints'

interface CropBoxProps {
  cropTwoPosX: [number, number]
  cropTwoPosY: [number, number]
  cropWidth: number
  cropHeight: number
}

/**
 * 비디오 크롭 영역
 */
const CropBox: React.FC<CropBoxProps> = ({
  cropTwoPosX: defaultCropTwoPosX,
  cropTwoPosY: defaultCropTwoPosY,
  cropWidth,
  cropHeight,
}) => {
  const [isDragging, setIsDragging] = useState<boolean>(false)
  const [cropTwoPosX, setCropTwoPosX] = useState<[number, number]>(defaultCropTwoPosX)
  const [cropTwoPosY, setCropTwoPosY] = useState<[number, number]>(defaultCropTwoPosY)

  return (
    <div
      draggable={false}
      className={cx('absolute top-0 left-0 z-10 backdrop-brightness-[4] cursor-grab transition-colors', {
        'cursor-grabbing': isDragging,
        'hover:bg-white/10': !isDragging,
        'bg-none': isDragging,
      })}
      style={{
        transform: `translate(${Math.min(...cropTwoPosX)}px, ${Math.min(...cropTwoPosY)}px)`,
        width: Math.abs(cropTwoPosX[0] - cropTwoPosX[1]),
        height: Math.abs(cropTwoPosY[0] - cropTwoPosY[1]),
      }}
      onPointerDown={(e) => {
        e.preventDefault()
        e.currentTarget.setPointerCapture(e.pointerId)
        setIsDragging(true)
      }}
      onPointerMove={(e) => {
        e.preventDefault()
        if (!isDragging) return

        setCropTwoPosX((prev) => [prev[0] + e.movementX, prev[1] + e.movementX])
        setCropTwoPosY((prev) => [prev[0] + e.movementY, prev[1] + e.movementY])
      }}
      onPointerUp={(e) => {
        e.preventDefault()
        e.currentTarget.releasePointerCapture(e.pointerId)
        setIsDragging(false)
      }}
    >
      <div className="w-full h-full border border-red-500 outline outline-8 -outline-offset-4 outline-red-500/20" />
      <CropGuideLines cropTwoPosX={cropTwoPosX} cropTwoPosY={cropTwoPosY} />
      <ResizingPoints setCropTwoPosX={setCropTwoPosX} setCropTwoPosY={setCropTwoPosY} />
    </div>
  )
}

export default CropBox

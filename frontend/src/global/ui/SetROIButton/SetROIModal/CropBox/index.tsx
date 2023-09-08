import React, { useMemo, useState } from 'react'
import cx from 'classnames'
import CropGuideLines from './CropGuideLines'
import ResizingPoints from './ResizingPoints'

interface CropBoxProps {
  cropTwoPosX: [number, number]
  cropTwoPosY: [number, number]
  clientWidth: number
  clientHeight: number
  setCropTwoPosX: React.Dispatch<React.SetStateAction<[number, number]>>
  setCropTwoPosY: React.Dispatch<React.SetStateAction<[number, number]>>
}

/**
 * 비디오 크롭 영역
 *
 * FIXME: resize 이벤트 발생 시 크롭영역 비율 조정
 */
const CropBox: React.FC<CropBoxProps> = ({
  clientWidth,
  clientHeight,
  cropTwoPosX,
  cropTwoPosY,
  setCropTwoPosX,
  setCropTwoPosY,
}) => {
  const [isDragging, setIsDragging] = useState<boolean>(false)
  const cropWidth = useMemo(() => Math.abs(cropTwoPosX[0] - cropTwoPosX[1]), [cropTwoPosX])
  const cropHeight = useMemo(() => Math.abs(cropTwoPosY[0] - cropTwoPosY[1]), [cropTwoPosY])
  const translateX = useMemo(() => {
    const x = Math.min(...cropTwoPosX)
    if (x < 0) return 0
    if (x + cropWidth > clientWidth) return clientWidth - cropWidth

    return x
  }, [cropTwoPosX, cropWidth, clientWidth])
  const translateY = useMemo(() => {
    const y = Math.min(...cropTwoPosY)
    if (y < 0) return 0
    if (y + cropHeight > clientHeight) return clientHeight - cropHeight

    return y
  }, [cropTwoPosY, cropHeight, clientHeight])

  return (
    <div
      draggable={false}
      className={cx('absolute top-0 left-0 z-10 backdrop-brightness-[4] cursor-grab transition-colors', {
        'cursor-grabbing': isDragging,
        'hover:bg-white/10': !isDragging,
        'bg-none': isDragging,
      })}
      style={{
        transform: `translate(${translateX}px, ${translateY}px)`,
        width: cropWidth,
        height: cropHeight,
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
        e.currentTarget.releasePointerCapture(e.pointerId)
        setIsDragging(false)
        setCropTwoPosX([translateX, translateX + cropWidth])
        setCropTwoPosY([translateY, translateY + cropHeight])
      }}
      onLostPointerCapture={(e) => {
        e.currentTarget.releasePointerCapture(e.pointerId)
        setIsDragging(false)
        setCropTwoPosX([translateX, translateX + cropWidth])
        setCropTwoPosY([translateY, translateY + cropHeight])
      }}
    >
      <div className="w-full h-full border border-red outline outline-[7px] -outline-offset-[4px] outline-red/20" />
      <CropGuideLines cropWidth={cropWidth} cropHeight={cropHeight} />
      <ResizingPoints
        clientWidth={clientWidth}
        clientHeight={clientHeight}
        setCropTwoPosX={setCropTwoPosX}
        setCropTwoPosY={setCropTwoPosY}
      />
    </div>
  )
}

export default CropBox

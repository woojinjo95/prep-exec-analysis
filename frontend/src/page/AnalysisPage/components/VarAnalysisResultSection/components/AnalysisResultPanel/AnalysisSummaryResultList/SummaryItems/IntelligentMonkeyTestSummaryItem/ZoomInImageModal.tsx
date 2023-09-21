import { AppURL } from '@global/constant'
import { useOutsideClick } from '@global/hook'
import React from 'react'

interface ZoomInImageModalProps {
  imagePath: string
  isOpen: boolean
  close: () => void
}

/**
 * intelligent monkey test 요약 결과의 메뉴 이미지 Zoom in 모달
 */
const ZoomInImageModal: React.FC<ZoomInImageModalProps> = ({ imagePath, isOpen, close }) => {
  const { ref } = useOutsideClick<HTMLImageElement>({
    mode: 'position',
    onClickOutside: () => {
      close()
    },
  })

  if (!isOpen) return null
  return (
    <div className="fixed top-0 left-0 w-screen h-screen flex justify-center items-center z-20">
      <div className="fixed z-10">
        <img
          ref={ref}
          src={`${AppURL.backendURL}/api/v1/file/download?path=${imagePath}`}
          alt="intelligent monkey test menu img"
          className="max-w-[30vw] max-h-[30vh] w-[30vw]"
        />
      </div>

      <div className="w-full h-full z-[5] bg-black opacity-[0.6]" />
    </div>
  )
}

export default ZoomInImageModal

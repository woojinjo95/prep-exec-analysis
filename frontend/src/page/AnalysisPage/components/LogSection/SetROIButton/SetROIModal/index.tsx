import React, { useState } from 'react'
import {
  Button,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
} from '@chakra-ui/react'
import video from './video.mp4'
import CropBox from './CropBox'

interface SetROIModalProps {
  isOpen: boolean
  onClose: () => void
}

/**
 * ROI 설정 모달
 */
const SetROIModal: React.FC<SetROIModalProps> = ({ isOpen, onClose }) => {
  const [videoWidth, setVideoWidth] = useState<number | null>(null)
  const [videoHeight, setVideoHeight] = useState<number | null>(null)
  const [videoClientWidth, setVideoClientWidth] = useState<number | null>(null) // 비디오 크기에 맞는 비율 계산 시 사용
  const [videoClientHeight, setVideoClientHeight] = useState<number | null>(null) // 비디오 크기에 맞는 비율 계산 시 사용

  const [cropWidth, setCropWidth] = useState<number | null>(null)
  const [cropHeight, setCropHeight] = useState<number | null>(null)

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="3xl" isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Set ROI</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <div
            className="relative"
            ref={(ref) => {
              // video 렌더링 전
              if (!ref || videoWidth === null || videoHeight === null) return
              // 이미 넓이, 높이를 구했을 경우
              if (videoClientWidth !== null || cropWidth !== null) return

              setVideoClientWidth(ref.clientWidth)
              setVideoClientHeight(ref.clientHeight)
              setCropWidth(ref.clientWidth / 2)
              setCropHeight(ref.clientHeight / 2)
            }}
          >
            <video
              src={video}
              onLoadedData={(e) => {
                setVideoWidth(e.currentTarget.videoWidth)
                setVideoHeight(e.currentTarget.videoHeight)
              }}
              controls
            />
            {/* background 영역, brightness 1/4배 어둡게 */}
            <div className="absolute top-0 left-0 w-full h-full backdrop-brightness-[0.25]" />
            {/* crop 영역, brightness 4배 밝게 => 원본밝기 */}
            {cropWidth !== null && cropHeight !== null && (
              <CropBox
                cropWidth={cropWidth}
                cropHeight={cropHeight}
                setCropWidth={(value: React.SetStateAction<number>) => setCropWidth(value as typeof cropWidth)}
                setCropHeight={(value: React.SetStateAction<number>) => setCropHeight(value as typeof cropHeight)}
              />
            )}
          </div>
        </ModalBody>

        <ModalFooter>
          <Button mr={3} onClick={onClose}>
            Close
          </Button>
          <Button>Save</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  )
}

export default SetROIModal

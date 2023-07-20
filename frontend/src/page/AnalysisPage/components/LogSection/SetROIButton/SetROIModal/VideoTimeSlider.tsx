import React, { useState } from 'react'
import { Slider, SliderFilledTrack, SliderMark, SliderThumb, SliderTrack, Tooltip } from '@chakra-ui/react'

interface VideoTimeSliderProps {
  duration: number
  changeVideoTimeCallback: (time: number) => void
}

/**
 * 비디오 시간 조절 슬라이더
 */
const VideoTimeSlider: React.FC<VideoTimeSliderProps> = ({ duration, changeVideoTimeCallback }) => {
  const [videoCurrentTime, setVideoCurrentTime] = useState<number>(0)
  const [showTooltip, setShowTooltip] = useState<boolean>(false)

  return (
    <Slider
      defaultValue={0}
      max={duration}
      onChange={(time) => {
        setVideoCurrentTime(time)
        changeVideoTimeCallback(time)
      }}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
      className="!py-8"
    >
      <SliderMark value={0} className="mt-2 text-sm">
        0sec
      </SliderMark>
      <SliderMark value={duration} className="mt-2 text-sm -translate-x-full">
        {duration.toFixed(1)}sec
      </SliderMark>

      <SliderTrack>
        <SliderFilledTrack />
      </SliderTrack>

      <Tooltip hasArrow color="white" placement="top" isOpen={showTooltip} label={`${videoCurrentTime.toFixed(1)}sec`}>
        <SliderThumb />
      </Tooltip>
    </Slider>
  )
}

export default VideoTimeSlider

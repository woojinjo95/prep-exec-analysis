import React from 'react'
import { ReactComponent as GoToFirstIcon } from '@assets/images/icon_go_to_first_w.svg'
import { ReactComponent as StepBackIcon } from '@assets/images/icon_step_back_1sec_w.svg'
import { ReactComponent as PlayIcon } from '@assets/images/icon_play.svg'
import { ReactComponent as StepForwardIcon } from '@assets/images/icon_step_forward_1sec_w.svg'
import { ReactComponent as GoToLastIcon } from '@assets/images/icon_go_to_last_w.svg'
import { Button, IconButton, Text } from '@global/ui'
import AppURL from '@global/constant/appURL'

/**
 * 결과영상 및 정보 영역
 */
const VideoDetailSection: React.FC = () => {
  return (
    <section className="bg-black text-white grid grid-rows-1 grid-cols-[1fr_1.5fr_1fr]">
      <div className="flex flex-col justify-end py-5 px-6 gap-y-4">
        <Text colorScheme="light" weight="medium">
          07:20.5
        </Text>
        <div className="flex flex-wrap items-center gap-2">
          <IconButton colorScheme="charcoal" icon={<GoToFirstIcon />} />
          <IconButton colorScheme="charcoal" icon={<StepBackIcon />} />
          <IconButton colorScheme="charcoal" icon={<PlayIcon />} />
          <IconButton colorScheme="charcoal" icon={<StepForwardIcon />} />
          <IconButton colorScheme="charcoal" icon={<GoToLastIcon />} />
        </div>
      </div>

      <div className="aspect-video">
        <video
          muted
          controls
          className="h-full aspect-video"
          src={`${AppURL.baseURL}/api/v1/video?scenario_id=d70eede7-2faa-4345-aa46-ba36e1ab40fd`}
        />
      </div>

      <div className="ml-auto mt-auto py-4 px-3">
        <Button colorScheme="charcoal">Save</Button>
      </div>
    </section>
  )
}

export default VideoDetailSection

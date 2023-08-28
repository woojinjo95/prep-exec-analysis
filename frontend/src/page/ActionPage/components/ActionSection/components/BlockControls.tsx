import React from 'react'
import { ReactComponent as MoreIcon } from '@assets/images/button_more.svg'
import { ReactComponent as PlusIcon } from '@assets/images/icon_add.svg'
import { ReactComponent as RecordIcon } from '@assets/images/icon_record.svg'
import { ReactComponent as PlayIcon } from '@assets/images/icon_play.svg'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { ReactComponent as StopIcon } from '@assets/images/icon_stop.svg'

import { IconButton, Text } from '@global/ui'
import useWebsocket from '@global/module/websocket'
import { useRecoilValue } from 'recoil'
import { scenarioIdState } from '@global/atom'

const BlockControls: React.FC = () => {
  const { sendMessage } = useWebsocket()

  const scenarioId = useRecoilValue(scenarioIdState)

  return (
    <div className="flex flex-wrap items-center px-3 py-2 gap-y-2 border-t border-[#DFE0EE] bg-white">
      <div className="flex items-center">
        <IconButton className="h-8" icon={<MoreIcon className="h-1 w-[18px]" />} />
        <div className="flex justify-center items-center border border-[#DFE0EE] h-[40px] w-[74px] rounded-[20px] ml-3 text-[14px] font-medium cursor-pointer">
          <Text size="sm" colorScheme="dark" weight="medium">
            Clear
          </Text>
        </div>
      </div>

      <div className="flex items-center gap-x-1 ml-auto">
        <IconButton icon={<PlusIcon />} />
        <IconButton
          icon={<StopIcon />}
          onClick={() => {
            sendMessage({
              level: 'info',
              msg: 'stop_scenario',
            })
          }}
        />
        <IconButton icon={<RecordIcon className="fill-red" />} />
        <IconButton
          icon={<PlayIcon />}
          onClick={() => {
            if (!scenarioId) return
            sendMessage({
              level: 'info',
              msg: 'run_scenario',
              data: { scenario_id: scenarioId },
            })
          }}
        />
        <IconButton icon={<TrashIcon />} />
      </div>
    </div>
  )
}

export default BlockControls

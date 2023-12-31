import { AxiosError } from 'axios'

import API from '@global/api'
import { HardwareConfiguration } from '@global/api/entity'
import apiUrls from './url'

/**
 * 하드웨어 설정 수정 api
 */
export const putHardwareConfiguration = async (
  data: Partial<
    Pick<
      HardwareConfiguration,
      | 'remote_control_type'
      | 'enable_dut_power'
      | 'enable_hdmi'
      | 'enable_dut_wan'
      | 'enable_network_emulation'
      | 'packet_bandwidth'
      | 'packet_delay'
      | 'packet_loss'
    >
  >,
) => {
  try {
    await API.put(apiUrls.hardware_configuration, data)
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 하드웨어 설정 - STB 연결 설정 수정 api
 */
export const putHardwareConfigurationSTBConnection = async (data: HardwareConfiguration['stb_connection']) => {
  try {
    await API.put(`${apiUrls.hardware_configuration}/stb_connection`, data)
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

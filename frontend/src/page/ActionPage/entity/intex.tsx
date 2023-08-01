export interface BlockData {
  type: string
  value: string
  delay_time: number
  id: string
}

export interface BlockGroupData {
  id: string
  repeat_cnt: number
  block: BlockData[]
}

export interface ScenarioData {
  items: {
    block_group: BlockGroupData
  }
}

export interface Block {
  type: string
  value: string
  delay_time: number
  id: string
}

export interface BlockGroup {
  id: string
  repeat_cnt: number
  block: Block[]
}

export interface Scenario {
  items: {
    block_group: BlockGroup[]
  }
}

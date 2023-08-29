export interface Block {
  type: string
  args: { key: string; value: string | number }[]
  name: string
  delay_time: number
  id: string
}

export interface BlockGroup {
  id: string
  repeat_cnt: number
  block: Block[]
}

export interface Scenario {
  id: string
  name: string
  is_acive: boolean
  tags: string[]
  block_group: BlockGroup[]
}

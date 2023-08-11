import { PaginationResponse } from '@global/api/entity'

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
  block_group: BlockGroup[]
}

export interface ScenarioSummary {
  id: string
  name: string
  tags: string[]
  updated_at: number
}

export type ScenarioSummaryResponse = PaginationResponse<ScenarioSummary[]>

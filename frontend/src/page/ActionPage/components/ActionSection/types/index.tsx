// refIdx가 포함된 block type
export interface Block {
  id: string
  type: string
  delay_time: number
  value: string
  refIdx: number
}

export type ActionStatus = 'RFC' | 'playing' | 'normal'

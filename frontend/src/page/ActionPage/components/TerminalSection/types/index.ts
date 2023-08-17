export interface Terminal {
  id: string
}

export interface History {
  type: 'command' | 'response'
  message: string
}
export interface Message {
  msg: string
  level: string
  data: {
    shell_id: 1 | 2
    mode: 'adb' | 'ssh'
    data: { timestamp: string; module: 'stdin' | 'stdout' | 'stderr'; message: string }
  }
  time: string
}

export interface ShellMessage {
  shell_id: 1 | 2
  mode: 'adb' | 'ssh'
  data: { timestamp: string; module: 'stdin' | 'stdout' | 'stderr'; message: string }
}

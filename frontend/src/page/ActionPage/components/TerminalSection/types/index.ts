export interface Terminal {
  id: string
}

export interface History {
  type: 'command' | 'response'
  message: string
}

export interface ShellMessage {
  shell_id: 1 | 2
  mode: 'adb' | 'ssh'
  data: { timestamp: string; module: 'stdin' | 'stdout' | 'stderr'; message: string }
}

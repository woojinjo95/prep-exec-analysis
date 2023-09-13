type ApiName = 'scenario' | 'block' | 'blocks' | 'block_group' | 'run_block'

const apiUrls: {
  [key in ApiName]: string
} = {
  scenario: '/api/v1/scenario',
  block: '/api/v1/scenario/block',
  blocks: '/api/v1/scenario/blocks',
  block_group: '/api/v1/scenario/block_group',
  run_block: '/api/v1/scenario/block/run_block',
}

export default apiUrls

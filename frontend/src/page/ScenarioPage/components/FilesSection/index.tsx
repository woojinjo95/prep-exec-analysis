import { Text } from '@global/ui'
import React, { useState } from 'react'
import cx from 'classnames'
import { ReactComponent as MoreIcon } from '@assets/images/button_more.svg'
import { formatDateTo } from '@global/usecase'
import Scrollbars from 'react-custom-scrollbars-2'

const tempFiles: { name: string; tags: string[]; last_modified: Date }[] = [
  {
    name: 'blocks',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks1',
    tags: ['BKO-UA500', 'sw-11.531.10-0000', 'SKBroadband'],
    last_modified: new Date(),
  },
  {
    name: 'blocks2',
    tags: ['BKO-UA500', 'sw-11.531.10-0000', 'SKBroadband', 'SKBroadband1'],
    last_modified: new Date(),
  },
  {
    name: 'blocks3',
    tags: [],
    last_modified: new Date(),
  },
  {
    name: 'blocks4',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks5',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks6',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks7',
    tags: [],
    last_modified: new Date(),
  },
  {
    name: 'blocks8',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks9',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks10',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks11',
    tags: [],
    last_modified: new Date(),
  },
  {
    name: 'blocks12',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks13',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks14',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks15',
    tags: [],
    last_modified: new Date(),
  },
  {
    name: 'blocks16',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks17',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
  {
    name: 'blocks18',
    tags: ['BKO-UA500'],
    last_modified: new Date(),
  },
]

const FilesSection: React.FC = () => {
  const [selectedMenu, setSelectedMenu] = useState<'Blocks' | 'Analysis Results'>('Blocks')

  return (
    <div className="flex flex-col w-full h-full p-7 min-h-full border-r-[1px] border-b-grey">
      <div className="min-h-[100px]">
        <div className="flex justify-between mt-5">
          <span className="text-[24px] mb-5 text-white">Files</span>
          <div className="flex">
            <Text size="md" className="mr-6 cursor-pointer">
              Search
            </Text>
            <Text size="md" className="cursor-pointer">
              Filter
            </Text>
          </div>
        </div>
        <div className="flex">
          <span
            className={cx('text-[15px] mr-[23px] cursor-pointer', {
              'text-primary': selectedMenu === 'Blocks',
              'text-white': selectedMenu !== 'Blocks',
            })}
            onClick={() => {
              setSelectedMenu('Blocks')
            }}
          >
            Blocks
          </span>
          <span
            className={cx('text-[15px] cursor-pointer', {
              'text-primary': selectedMenu === 'Analysis Results',
              'text-white': selectedMenu !== 'Analysis Results',
            })}
            onClick={() => {
              setSelectedMenu('Analysis Results')
            }}
          >
            Analysis Results
          </span>
        </div>
      </div>
      <div className="mt-5 flex w-full min-h-[calc(100%-100px)]">
        <div className="flex flex-col w-full">
          <div className="w-full grid grid-cols-[30%_40%_25%_5%] border-b-grey border-b-[1px] h-8 items-center">
            <Text className="text-sm" colorScheme="grey">
              Name
            </Text>
            <Text className="text-sm" colorScheme="grey">
              Tag
            </Text>
            <Text className="text-sm" colorScheme="grey">
              Last modified
            </Text>
            <div />
          </div>
          <Scrollbars
            renderThumbVertical={({ ...props }) => <div {...props} className="bg-[#4E525A] w-2 rounded-[5px]" />}
          >
            {tempFiles?.map((file) => (
              <div className="flex flex-col w-full" key={`file_${file.name}`}>
                <div className="w-full grid grid-cols-[30%_40%_25%_5%] border-b-grey border-b-[1px] min-h-[48px] items-center">
                  <div>
                    <Text className="text-white mr-3" invertBackground colorScheme="light-orange">
                      B
                    </Text>
                    <Text size="md" colorScheme="light">
                      {file.name}
                    </Text>
                  </div>

                  <div className="flex flex-wrap w-full h-full pt-[10px] items-center">
                    {file.tags.map((tag) => (
                      <Text
                        className="text-white mr-2 mb-2"
                        invertBackground
                        colorScheme="dark-grey"
                        key={`${file.name}_tag_${tag}`}
                      >
                        {tag}
                      </Text>
                    ))}
                  </div>
                  <Text size="md" colorScheme="light">
                    {formatDateTo('M DD YYYY, HH:MM AA', file.last_modified)}
                  </Text>
                  <div className="flex justify-center cursor-pointer h-full">
                    <MoreIcon className="w-[20px] fill-white " />
                  </div>
                </div>
              </div>
            ))}
          </Scrollbars>
        </div>
      </div>
    </div>
  )
}

export default FilesSection

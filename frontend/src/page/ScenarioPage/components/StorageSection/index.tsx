import React from 'react'
import { contentColors } from '@page/ScenarioPage/constants'
import { Text } from '@global/ui'
import VolumnBar from './VolumnBar'

const storageItems: { name: string; volumn: number; fileNum: number }[] = [
  {
    name: 'Blocks',
    volumn: 10.846,
    fileNum: 1234,
  },
  {
    name: 'Videos',
    volumn: 310.5,
    fileNum: 530,
  },
  {
    name: 'Analysis Results',
    volumn: 45.2,
    fileNum: 807,
  },
]

const storage = 464
const used = 368.5

const StorageSection: React.FC = () => {
  return (
    <div className="flex flex-col w-full h-full p-7">
      <div className="flex justify-between">
        <p className="text-[28px]">
          <Text className="!text-[28px] mr-2" weight="bold" colorScheme="light">
            {used}
          </Text>
          <Text className="!text-[24px]" weight="bold" colorScheme="light">
            GB
          </Text>
        </p>
        <p className="text-[28px]">
          <Text className="!text-[28px] mr-2" weight="bold" colorScheme="grey">
            {storage}
          </Text>
          <Text className="!text-[24px]" weight="bold" colorScheme="grey">
            GB
          </Text>
        </p>
      </div>

      <div className="flex justify-between mb-4">
        <Text className="!text-sm" colorScheme="grey">
          Used
        </Text>
        <Text className="!text-sm" colorScheme="grey">
          Storage
        </Text>
      </div>

      <VolumnBar storageItems={storageItems} total={storage} />

      <div className="flex flex-col w-full mt-4">
        {storageItems?.map((storageItem) => (
          <div
            key={`storageItem_${storageItem.name}`}
            className="h-[54px] grid grid-cols-[56px_4fr_1.5fr] mb-4 gap-x-3"
          >
            <div className={`bg-${contentColors[storageItem.name]}`} />
            <div className="text-white flex flex-col items-start justify-center">
              <Text className="!text-[18px]" weight="bold" colorScheme="light">
                {storageItem.name}
              </Text>
              <Text className="!text-[14px]" colorScheme="light">{`${storageItem.fileNum} Files`}</Text>
            </div>
            <div className="text-white flex items-center justify-end text-[20px]">{`${storageItem.volumn} GB`}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default StorageSection

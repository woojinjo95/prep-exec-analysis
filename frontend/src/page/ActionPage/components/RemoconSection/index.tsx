import React, { useEffect, useRef, useState } from 'react'
import Remocon from '@assets/images/btv_remote_control.png'

/**
 * 리모컨 영역
 */
const RemoconSection: React.FC = () => {
  const remoconDivRef = useRef<HTMLDivElement>(null)

  const [remoconHeight, setRemoconHeight] = useState<number>(0)

  useEffect(() => {
    const updateRemoconHeight = () => {
      if (remoconDivRef.current) {
        setRemoconHeight(remoconDivRef.current.offsetHeight)
      }
    }

    updateRemoconHeight()

    const resizeHandler = () => {
      updateRemoconHeight()
    }

    window.addEventListener('resize', resizeHandler)
    return () => {
      window.removeEventListener('resize', resizeHandler)
    }
  }, [remoconDivRef, remoconHeight])

  return (
    <section className="border border-black h-full">
      <div className="flex flex-col w-full h-full p-[10px]">
        <div className="flex flex-row justify-between w-full h-[30px]">
          <p>dropdown</p>
          <p>help</p>
        </div>
        <div className="h-[calc(100%-30px)] flex flex-row">
          <div ref={remoconDivRef} className="w-[50%] h-full flex items-center justify-center">
            <img src={Remocon} alt="remocon" style={{ height: `${remoconHeight * 0.95}px` }} />
          </div>
          <div className="w-[50%] flex flex-col">
            <div className="flex flex-row justify-between">
              <p>Custom Key</p>
              <div className="flex flex-row justify-between">
                <p>+</p>
                <p>|</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default RemoconSection

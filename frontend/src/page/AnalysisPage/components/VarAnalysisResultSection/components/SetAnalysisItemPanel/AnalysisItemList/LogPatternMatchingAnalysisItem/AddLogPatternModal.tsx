import React, { useState } from 'react'
import { Button, ColorPickerBox, Input, Modal, Select, Title, Text, OptionItem, CodeEditor } from '@global/ui'
import { LogLevel } from '@global/constant'

interface AddLogPatternModalProps {
  isOpen: boolean
  close: () => void
}

/**
 * 로그 패턴 추가 모달
 *
 * TODO:
 */
const AddLogPatternModal: React.FC<AddLogPatternModalProps> = ({ isOpen, close }) => {
  const [name, setName] = useState<string>('')
  const [logLevel, setLogLevel] = useState<keyof typeof LogLevel>('V')
  const [regex, setRegex] = useState<string>('')
  const [isValidRegex, setIsValidRegex] = useState<boolean>(false)
  const [color, setColor] = useState<string>('red')
  const [warning, setWarning] = useState<{ name: string; regex: boolean }>({ name: '', regex: false })

  const onSubmit = () => {
    let isNotValid = false
    if (!name) {
      setWarning((prev) => ({ ...prev, name: 'Enter name.' }))
      isNotValid = true
    }
    if (!isValidRegex) {
      setWarning((prev) => ({ ...prev, regex: true }))
      isNotValid = true
    }

    if (isNotValid) return
    // TODO: setUnsavedAnalysisConfig
    console.log()
  }

  return (
    <Modal
      isOpen={isOpen}
      close={close}
      title="Add Log Pattern"
      className="w-[60vw] h-[60vh] min-h-[600px] min-w-[960px]"
    >
      <div className="w-full h-full grid grid-cols-[auto_1fr] grid-rows-[auto_auto_1fr_auto_auto] gap-x-10 gap-y-3">
        <Title as="h3" colorScheme="light" className="pt-3">
          Log Pattern Name
        </Title>
        <div className="flex">
          <Input
            placeholder="Untitled Log Pattern"
            className="w-80"
            value={name}
            onChange={(e) => setName(e.target.value)}
            warningMessage={warning.name}
          />
        </div>

        <Title as="h3" colorScheme="light" className="pt-3">
          Log Level
        </Title>
        <div className="flex">
          <Select
            colorScheme="charcoal"
            className="w-32"
            widthOption="fit-wrapper"
            header={
              <Text weight="bold" colorScheme="light">
                {logLevel}
              </Text>
            }
          >
            {Object.keys(LogLevel).map((_level) => {
              const level = _level as keyof typeof LogLevel

              return (
                <OptionItem
                  key={`add-log-pattern-modal-log-level-list-${level}`}
                  colorScheme="charcoal"
                  onClick={() => {
                    setLogLevel(level)
                  }}
                  isActive={level === logLevel}
                >
                  {level}
                </OptionItem>
              )
            })}
          </Select>
        </div>

        <Title as="h3" colorScheme="light" className="pt-3">
          Regular Expression
        </Title>
        <div className="grid grid-cols-1 grid-rows-[1fr_auto] gap-y-2">
          <CodeEditor code={regex} setCode={setRegex} />

          <div>
            <Button
              className="charcoal"
              onClick={() => {
                // TODO: 정규표현식 체크 필요.
                setIsValidRegex(true)
              }}
            >
              Check Validation
            </Button>
            <Text className="ml-7" colorScheme={warning.regex ? 'orange' : 'light'}>
              Is valid regular expression.
            </Text>
          </div>
        </div>

        <div>
          <Title as="h3" colorScheme="light">
            Color
          </Title>
        </div>
        <div className="flex items-center">
          <ColorPickerBox color={color} className="w-12 h-5" onChange={(color) => setColor(color)} />
        </div>

        <div className="col-span-2 flex justify-end items-center gap-x-3">
          <Button colorScheme="primary" onClick={onSubmit}>
            Save
          </Button>
          <Button colorScheme="grey">Cancel</Button>
        </div>
      </div>
    </Modal>
  )
}

export default AddLogPatternModal

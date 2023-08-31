/* eslint-disable @typescript-eslint/no-unsafe-call */
import React from 'react'
import AceEditor from 'react-ace'
import classnames from 'classnames/bind'
import 'ace-builds/src-noconflict/mode-xml'
import 'ace-builds/src-noconflict/theme-monokai'
import 'ace-builds/src-noconflict/ext-language_tools'
import * as ace from 'ace-builds/src-noconflict/ace'

import styles from './CodeEditor.module.scss'

// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
ace.config.set('basePath', '/node_modules/ace-builds/src-noconflict/')

const cx = classnames.bind(styles)

interface CodeEditorProps {
  code: string
  setCode: React.Dispatch<React.SetStateAction<string>>
}

const CodeEditor: React.FC<CodeEditorProps> = ({ code, setCode }) => {
  return (
    <div className={cx('editor')}>
      <AceEditor
        mode="xml"
        theme="monokai"
        onLoad={() => {
          //
        }}
        onChange={(value) => {
          setCode(value)
        }}
        value={code}
        width="100%"
        height="100%"
        setOptions={{
          enableBasicAutocompletion: true,
          enableLiveAutocompletion: true,
          enableSnippets: true,
          showLineNumbers: true,
          showPrintMargin: true,
          showGutter: true,
          highlightActiveLine: true,
          fontSize: 16,
          tabSize: 2,
        }}
      />
    </div>
  )
}

export default CodeEditor

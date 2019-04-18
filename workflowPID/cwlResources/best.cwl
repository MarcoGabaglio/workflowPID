cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ python ]


inputs:
    pythonscript:
        type: File
        inputBinding:
            position: 1

    filetoParse:
        type: File
        inputBinding:
            position: 2


outputs:
    bestids:
        type: stdout
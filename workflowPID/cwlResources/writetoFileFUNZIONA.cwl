cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ cat ]


inputs:
    ras:
        type: File
        inputBinding:
            position: 1

outputs:
    finalras:
        type: stdout
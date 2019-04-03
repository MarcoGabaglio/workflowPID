cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ cat ]
stdout: $(inputs.name.basename).RESULT


inputs:
    ras:
        type: File
        inputBinding:
            position: 1
    name:
        type: File

outputs:
    finalras:
        type: stdout
        
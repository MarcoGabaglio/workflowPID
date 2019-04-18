cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ python ]
arguments: [$(inputs.pythonscript.path), $(inputs.ras.path)]


inputs:

    pythonscript:
        type: File
        inputBinding:
            position: 1

    ras:
        type: File

    name:
        type: File



outputs: []
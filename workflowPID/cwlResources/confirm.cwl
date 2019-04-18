cwlVersion: v1.0
class: CommandLineTool
baseCommand: [sort]

arguments: ["-k1,1", "-k12,12nr", "-k11,11n"]

inputs:
    blastRes:
        type: File
        inputBinding:
            position: 1


outputs:
    res:
        type: stdout
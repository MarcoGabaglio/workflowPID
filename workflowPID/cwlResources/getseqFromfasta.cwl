cwlVersion: v1.0
class: CommandLineTool
baseCommand: [grep]
arguments: [-w, -A 1, -f]



inputs:
    ids:
        type: File
        inputBinding:
            position: 1

    data:
        type: File
        inputBinding:
            position: 2


outputs:
    bestseq:
       type: stdout
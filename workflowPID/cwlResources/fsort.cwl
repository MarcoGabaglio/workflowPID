cwlVersion: v1.0
class: CommandLineTool
baseCommand: [sort]

arguments: ["-u", "-k1,1", "--merge"]


inputs:
    firstsort:
        type: File
        inputBinding:
            position: 1


outputs:
   finalres:
       type: stdout
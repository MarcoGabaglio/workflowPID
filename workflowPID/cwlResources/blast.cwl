cwlVersion: v1.0
class: CommandLineTool
baseCommand: [blastp]
arguments: ["-outfmt", "6"]

inputs:
    db:
        type: File
        inputBinding:
            position: 1
            prefix: -db
        secondaryFiles:
            - .pin
            - .phr
            

    queries:
        type: File
        inputBinding:
            position: 2
            prefix: -query
outputs:
    blastresults:
        type: stdout
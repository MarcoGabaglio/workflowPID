cwlVersion: v1.0
class: Workflow


inputs:
    database:
        type: File
        secondaryFiles:
            - .pin
            - .phr
            - .psq



    randomDB:
        type: File
        secondaryFiles:
            - .pin
            - .phr
            - .psq

    queries: File

    script1: File

    #script2: File



outputs:
    outFile:
        type: File
        outputSource: [write/finalras]


steps:
   firstBlast:
       run: blast.cwl
       in:
          db: database
          queries: queries
          

       out: [blastresults]

   analyze:
       run: best.cwl
       in:
           pythonscript: script1
           filetoParse: firstBlast/blastresults

       out: [bestids]

   getseq:
       run: getseqFromfasta.cwl
       in:
           ids: analyze/bestids
           data: database

       out: [bestseq]



   finalBlast:
       run: blast.cwl
       in:
           db: randomDB
           queries: getseq/bestseq

       out: [blastresults]

   sort:
       run: confirm.cwl
       in:
           blastRes: finalBlast/blastresults

       out: [res]


   finalsort:
       run: fsort.cwl

       in:
           firstsort: sort/res

       out:
           [finalres]



   write:
        run: writetoFile.cwl

        in:
            ras: finalsort/finalres
            name: queries

        out: [finalras]
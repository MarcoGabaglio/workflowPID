{
    "cwlVersion": "v1.0", 
    "$graph": [
        {
            "id": "#best.cwl", 
            "inputs": {
                "filetoParse": {
                    "inputBinding": {
                        "position": 2
                    }, 
                    "type": "File"
                }, 
                "pythonscript": {
                    "inputBinding": {
                        "position": 1
                    }, 
                    "type": "File"
                }
            }, 
            "class": "CommandLineTool", 
            "outputs": {
                "bestids": {
                    "type": "stdout"
                }
            }, 
            "baseCommand": [
                "python"
            ]
        }, 
        {
            "inputs": {
                "db": {
                    "secondaryFiles": [
                        ".pin", 
                        ".phr"
                    ], 
                    "inputBinding": {
                        "position": 1, 
                        "prefix": "-db"
                    }, 
                    "type": "File"
                }, 
                "queries": {
                    "inputBinding": {
                        "position": 2, 
                        "prefix": "-query"
                    }, 
                    "type": "File"
                }
            }, 
            "outputs": {
                "blastresults": {
                    "type": "stdout"
                }
            }, 
            "baseCommand": [
                "blastp"
            ], 
            "class": "CommandLineTool", 
            "arguments": [
                "-outfmt", 
                "6"
            ], 
            "id": "#blast.cwl"
        }, 
        {
            "inputs": {
                "blastRes": {
                    "inputBinding": {
                        "position": 1
                    }, 
                    "type": "File"
                }
            }, 
            "outputs": {
                "res": {
                    "type": "stdout"
                }
            }, 
            "baseCommand": [
                "sort"
            ], 
            "class": "CommandLineTool", 
            "arguments": [
                "-k1,1", 
                "-k12,12nr", 
                "-k11,11n"
            ], 
            "id": "#confirm.cwl"
        }, 
        {
            "inputs": {
                "firstsort": {
                    "inputBinding": {
                        "position": 1
                    }, 
                    "type": "File"
                }
            }, 
            "outputs": {
                "finalres": {
                    "type": "stdout"
                }
            }, 
            "baseCommand": [
                "sort"
            ], 
            "class": "CommandLineTool", 
            "arguments": [
                "-u", 
                "-k1,1", 
                "--merge"
            ], 
            "id": "#fsort.cwl"
        }, 
        {
            "inputs": {
                "data": {
                    "inputBinding": {
                        "position": 2
                    }, 
                    "type": "File"
                }, 
                "ids": {
                    "inputBinding": {
                        "position": 1
                    }, 
                    "type": "File"
                }
            }, 
            "outputs": {
                "bestseq": {
                    "type": "stdout"
                }
            }, 
            "baseCommand": [
                "grep"
            ], 
            "class": "CommandLineTool", 
            "arguments": [
                "-w", 
                "-A 1", 
                "-f"
            ], 
            "id": "#getseqFromfasta.cwl"
        }, 
        {
            "id": "#main", 
            "inputs": [
                {
                    "secondaryFiles": [
                        ".pin", 
                        ".phr", 
                        ".psq"
                    ], 
                    "type": "File", 
                    "id": "#main/database"
                }, 
                {
                    "type": "File", 
                    "id": "#main/queries"
                }, 
                {
                    "secondaryFiles": [
                        ".pin", 
                        ".phr", 
                        ".psq"
                    ], 
                    "type": "File", 
                    "id": "#main/randomDB"
                }, 
                {
                    "type": "File", 
                    "id": "#main/script"
                }
            ], 
            "steps": [
                {
                    "out": [
                        "#main/analyze/bestids"
                    ], 
                    "run": "#best.cwl", 
                    "id": "#main/analyze", 
                    "in": [
                        {
                            "source": "#main/firstBlast/blastresults", 
                            "id": "#main/analyze/filetoParse"
                        }, 
                        {
                            "source": "#main/script", 
                            "id": "#main/analyze/pythonscript"
                        }
                    ]
                }, 
                {
                    "out": [
                        "#main/finalBlast/blastresults"
                    ], 
                    "run": "#blast.cwl", 
                    "id": "#main/finalBlast", 
                    "in": [
                        {
                            "source": "#main/randomDB", 
                            "id": "#main/finalBlast/db"
                        }, 
                        {
                            "source": "#main/getseq/bestseq", 
                            "id": "#main/finalBlast/queries"
                        }
                    ]
                }, 
                {
                    "out": [
                        "#main/finalsort/finalres"
                    ], 
                    "run": "#fsort.cwl", 
                    "id": "#main/finalsort", 
                    "in": [
                        {
                            "source": "#main/sort/res", 
                            "id": "#main/finalsort/firstsort"
                        }
                    ]
                }, 
                {
                    "out": [
                        "#main/firstBlast/blastresults"
                    ], 
                    "run": "#blast.cwl", 
                    "id": "#main/firstBlast", 
                    "in": [
                        {
                            "source": "#main/database", 
                            "id": "#main/firstBlast/db"
                        }, 
                        {
                            "source": "#main/queries", 
                            "id": "#main/firstBlast/queries"
                        }
                    ]
                }, 
                {
                    "out": [
                        "#main/getseq/bestseq"
                    ], 
                    "run": "#getseqFromfasta.cwl", 
                    "id": "#main/getseq", 
                    "in": [
                        {
                            "source": "#main/database", 
                            "id": "#main/getseq/data"
                        }, 
                        {
                            "source": "#main/analyze/bestids", 
                            "id": "#main/getseq/ids"
                        }
                    ]
                }, 
                {
                    "out": [
                        "#main/sort/res"
                    ], 
                    "run": "#confirm.cwl", 
                    "id": "#main/sort", 
                    "in": [
                        {
                            "source": "#main/finalBlast/blastresults", 
                            "id": "#main/sort/blastRes"
                        }
                    ]
                }, 
                {
                    "out": [
                        "#main/write/finalras"
                    ], 
                    "run": "#writetoFile.cwl", 
                    "id": "#main/write", 
                    "in": [
                        {
                            "source": "#main/finalsort/finalres", 
                            "id": "#main/write/ras"
                        }
                    ]
                }
            ], 
            "class": "Workflow", 
            "outputs": [
                {
                    "outputSource": "#main/write/finalras", 
                    "type": "File", 
                    "id": "#main/outFile"
                }
            ]
        }, 
        {
            "inputs": {
                "ras": {
                    "inputBinding": {
                        "position": 1
                    }, 
                    "type": "File"
                }
            }, 
            "stdout": "output.txt", 
            "outputs": {
                "finalras": {
                    "type": "stdout"
                }
            }, 
            "baseCommand": [
                "cat"
            ], 
            "class": "CommandLineTool", 
            "id": "#writetoFile.cwl"
        }
    ]
}
import csv
import itertools
import os

symbolAddrsLines = []
assetsYamlLines = []
CLines = []
HLines = []
fileCombined = []
fileC = []
fileH = []
projectDir = "/mnt/c/users/emily/afdecomp/af"
# If there's c_keyframe data we need to include c_keyframe.h
ckfDataExists: bool = False
ckfTypes = ["ckf_je", "ckf_bs", "ckf_ckcb", "ckf_kn", "ckf_c", "ckf_ds", "ckf_ba"]
# Same with evw_anime.h
evwDataExists: bool = False
evwTypes = ["evw_scroll", "evw_colprim", "evw_colenv", "evw_colreg", "evw_texanime", "evw_textable", "evw_animeptn", "evw_data"]
notArrayTypes = ["ckf_bs", "ckf_ba", "evw_colreg", "evw_texanime", "evw_textable"]

with open('input.csv', newline='') as csvfile:
    # Create two iterators so we can check both the current and next line
    # This is necessary to calculate the size of vertex segments
    reader, nextReader = itertools.tee(csv.reader(csvfile, skipinitialspace=True, delimiter=',', quotechar='|'))
    next(nextReader)
    firstRow = True

    for row, nextRow in itertools.zip_longest(reader, nextReader):
        if firstRow:
            firstRow = False

            if len(row) == 5:
                romStart, romEnd, segmentNum, segmentName, fileDir = row
                subFolder = None
            if len(row) == 6:
                romStart, romEnd, segmentNum, segmentName, fileDir, subFolder = row

            romStart: int = int(romStart[2:], 16)
            romEnd: int = int(romEnd[2:], 16)
            segmentNum: int = int(segmentNum, 16)
            continue
    
        vram, fileName, fileType = row
        # offset from the start is the vram address without the segment prefix
        rom: int = romStart + int(vram[4:], 16)
        vram: int = int(vram[2:],16)
        if fileType == "vtx":

            nextVram = nextRow[0]
            nextVram: int = int(nextVram[2:],16)
            size = nextVram - vram
            symbolAddrsLines.append(f"{fileName} = 0x{vram:X}; // segment:{segmentName} rom:0x{rom:X} size:0x{size:X}")
        else:
            symbolAddrsLines.append(f"{fileName} = 0x{vram:X}; // segment:{segmentName} rom:0x{rom:X}")
        
        if subFolder:
            assetsYamlLines.append(f"          - [0x{rom:X}, {fileType}, {subFolder}/{fileName}]")
        else:
            assetsYamlLines.append(f"          - [0x{rom:X}, {fileType}, {fileName}]")

        fileExtension: str = None
        if fileType == "vtx":
            fileExtension = ".vtx"
        if fileType == "af_gfx":
            fileExtension = ".gfx"
        if fileType == "af_palette":
            fileExtension = ".palette"
        if fileType == "af_ci4":
            fileExtension = ".ci4"
        if fileType == "af_i4":
            fileExtension = ".i4"
        if fileType == "af_i8":
            fileExtension = ".i8"
        if fileType == "af_ia8":
            fileExtension = ".ia8"
        if fileType == "ckf_je":
            fileExtension = ""
        if fileType == "ckf_bs":
            fileExtension = ""
        if fileType == "ckf_ckcb":
            fileExtension = ""
        if fileType == "ckf_kn":
            fileExtension = ""
        if fileType == "ckf_c":
            fileExtension = ""
        if fileType == "ckf_ds":
            fileExtension = ""
        if fileType == "ckf_ba":
            fileExtension = ""
        if fileType == "evw_scroll":
            fileExtension = ""
        if fileType == "evw_colprim":
            fileExtension = ""
        if fileType == "evw_colenv":
            fileExtension = ""
        if fileType == "evw_colreg":
            fileExtension = ""
        if fileType == "evw_texanime":
            fileExtension = ""
        if fileType == "evw_textable":
            fileExtension = ""
        if fileType == "evw_animeptn":
            fileExtension = ""
        if fileType == "evw_data":
            fileExtension = ""

        if subFolder:
            CLines.append(f'#include "assets/jp/{fileDir}/{subFolder}/{fileName}{fileExtension}.inc.c"')
        else:
            CLines.append(f'#include "assets/jp/{fileDir}/{fileName}{fileExtension}.inc.c"')

        dataType: str = None
        if fileType == "vtx":
            dataType = "Vtx"
        if fileType == "af_gfx":
            dataType = "Gfx"
        if fileType == "af_palette":
            dataType = "unsigned short"
        if fileType == "af_ci4":
            dataType = "unsigned char"
        if fileType == "af_i4":
            dataType = "unsigned char"
        if fileType == "af_i8":
            dataType = "unsigned char"
        if fileType == "af_ia8":
            dataType = "unsigned char"
        if fileType == "ckf_je":
            dataType = "JointElemR"
        if fileType == "ckf_bs":
            dataType = "BaseSkeletonR"
        if fileType == "ckf_ckcb":
            dataType = "u8"
        if fileType == "ckf_kn":
            dataType = "s16"
        if fileType == "ckf_c":
            dataType = "s16"
        if fileType == "ckf_ds":
            dataType = "Keyframe"
        if fileType == "ckf_ba":
            dataType = "BaseAnimationR"
        if fileType == "evw_scroll":
            dataType = "EvwAnimeScroll"
        if fileType == "evw_colprim":
            dataType = "EvwAnimeColPrim"
        if fileType == "evw_colenv":
            dataType = "EvwAnimeColEnv"
        if fileType == "evw_colreg":
            dataType = "EvwAnimeColReg"
        if fileType == "evw_texanime":
            dataType = "EvwAnimeTexAnime"
        if fileType == "evw_textable":
            dataType = "void*"
        if fileType == "evw_animeptn":
            dataType = "u8"
        if fileType == "evw_data":
            dataType = "EvwAnimeData"

        if not ckfDataExists and fileType in ckfTypes:
            ckfDataExists = True
        
        if not evwDataExists and fileType in evwTypes:
            evwDataExists = True

        if fileType in notArrayTypes:
            HLines.append(f"extern {dataType} {fileName};")
        else:
            HLines.append(f"extern {dataType} {fileName}[];")

    fileCombined.append("--------------------------------------------------------------------------------")
    fileCombined.append("symbol_addrs_assets.txt")
    fileCombined.append("--------------------------------------------------------------------------------")
    symbolAddrsLines = "\n".join(symbolAddrsLines)
    fileCombined.append(symbolAddrsLines)
    fileCombined.append("")

    fileCombined.append("--------------------------------------------------------------------------------")
    fileCombined.append("assets.yaml")
    fileCombined.append("--------------------------------------------------------------------------------")
    fileCombined.append(f"  - name: {segmentName}")
    fileCombined.append(f"    dir: {fileDir}")
    fileCombined.append(f"    type: code")
    fileCombined.append(f"    start: 0x{romStart:X}")
    fileCombined.append(f"    vram: 0x{segmentNum:02X}000000")
    fileCombined.append(f"    exclusive_ram_id: segment_{segmentNum:02X}")
    fileCombined.append(f"    compress: True")
    fileCombined.append(f"    align: 0x1000")
    fileCombined.append(f"    symbol_name_format: $VRAM_$ROM")
    fileCombined.append(f"    subsegments:")
    fileCombined.append(f"      - [auto, c, {segmentName}]")
    fileCombined.append(f"      - start: 0x{romStart:X}")
    fileCombined.append(f"        type: .data")
    fileCombined.append(f"        name: {segmentName}")
    fileCombined.append(f"        subsegments:")
    assetsYamlLines = "\n".join(assetsYamlLines)
    fileCombined.append(assetsYamlLines)
    fileCombined.append(f"  - [0x{romEnd:X}]")
    fileCombined.append("")

    if subFolder:
        fileC.append(f'#include "{subFolder}.h"')
    else:
        fileC.append(f'#include "{segmentName}.h"')
    fileC.append("")
    CLines = "\n".join(CLines)
    fileC.append(CLines)
    fileC.append("")

    if subFolder:
        fileH.append(f"#ifndef OBJECT_{subFolder.upper()}_H")
        fileH.append(f"#define OBJECT_{subFolder.upper()}_H")
    else:
        fileH.append(f"#ifndef OBJECT_{segmentName.upper()}_H")
        fileH.append(f"#define OBJECT_{segmentName.upper()}_H")
    fileH.append("")
    fileH.append('#include "gbi.h"')
    if ckfDataExists:
        fileH.append('#include "c_keyframe.h"')
    if evwDataExists:
        fileH.append('#include "evw_anime.h"')
    fileH.append("")
    HLines = "\n".join(HLines)
    fileH.append(HLines)
    fileH.append("")
    fileH.append("#endif")
    fileH.append("")
    

fileCombined = "\n".join(fileCombined)
with open("output.txt", "w") as outputFile:
    outputFile.write(fileCombined)

if subFolder:
    path = f"{projectDir}/src/{fileDir}/{subFolder}"
else:
    path = f"{projectDir}/src/{fileDir}"

try:
    os.mkdir(path)
except:
    pass

if subFolder:
    fileC = "\n".join(fileC)
    with open(f"{path}/{subFolder}.c", "w") as outputFile:
        outputFile.write(fileC)

    fileH = "\n".join(fileH)
    with open(f"{path}/{subFolder}.h", "w") as outputFile:
        outputFile.write(fileH)
else:
    fileC = "\n".join(fileC)
    with open(f"{path}/{segmentName}.c", "w") as outputFile:
        outputFile.write(fileC)

    fileH = "\n".join(fileH)
    with open(f"{path}/{segmentName}.h", "w") as outputFile:
        outputFile.write(fileH)

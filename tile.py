TMEM_WORD_SIZE: int = 0x8

objectRomStart: int = 0x15C8000

# usually the palette is placed before the textures, offsetting their address by 0x20
offset: int = 0x20

paletteName: str = "int_sum_hal_chest02_pal"

# texture start: this is in "TMEM words" which are 8 bytes. the tmem argument in gDPSetTile()
# texture width: the lrs argument in gDPSetTileSize() is displayed as (n<<2), this should be n+1
# texture height: the lrt argument in gDPSetTileSize() is displayed as (n<<2), this should be n+1
tileData: dict = [
    [0x00, 32, 32],
    [0x40, 16, 16],
    [0x50, 16, 16],
    [0x60, 32, 48],
    [0xC0, 16, 48],
    [0xF0, 16, 16],
    ]

rowCount:int = 1

for row in tileData:
    textureStart:int
    textureWidth: int
    textureHeight: int

    textureStart, textureWidth, textureHeight = row

    romAddress:int = objectRomStart + offset +  textureStart * TMEM_WORD_SIZE
    print(f"          - [0x{romAddress:X}, ci4, texture{rowCount}, {textureWidth}, {textureHeight}, {paletteName}]")

    rowCount += 1
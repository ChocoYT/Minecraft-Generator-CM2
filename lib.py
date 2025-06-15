from enum import Enum
from typing import Union

number = Union[int, float]

class BlockType(Enum):
    NOR           = 0, 1
    AND           = 1, 0
    OR            = 2, 0
    XOR           = 3, 0
    Button        = 4, 0
    FlipFlop_OFF  = 5, 0
    FlipFlop_ON   = 5, 1
    LED           = 6, 0
    Sound         = 7, 0
    Conductor     = 8, 0
    MysteriousOR  = 9, 0
    NAND          = 10, 1
    XNOR          = 11, 1
    Random        = 12, 1
    Text          = 13, 0
    Tile          = 14, 0
    Node          = 15, 0
    Delay         = 16, 0
    Antenna       = 17, 0
    ConductorV2   = 18, 0
    LEDMixer      = 19, 0

class SoundType(Enum):
    SINE     = 0
    SQUARE   = 1
    TRIANGLE = 2
    SAWTOOTH = 3
    
class Material(Enum):
    STUD   = 1
    SMOOTH = 2
    
class Properties(Enum):
    SNAP_TO_GRID = None
    TEXT         = 65
    COLOR        = 75, 75, 75
    MATERIAL     = 1
    COLLISION    = 0

class Block:
    def __init__(self, block: BlockType, position: tuple[number, number, number], properties: dict | None = {}):
        self.block      = block
        self.position   = position
        self.properties = properties
        
        self.encoded = self.encode()
 
    def encode(self) -> str:
        data = f"{self.block.value[0]},{self.block.value[1]},{self.position[0]},{self.position[1]},{self.position[2]},"
        
        text       = self.properties.get(Properties.TEXT        )
        color      = self.properties.get(Properties.COLOR       )
        material   = self.properties.get(Properties.MATERIAL    )
        collision  = self.properties.get(Properties.COLLISION   )
        snapToGrid = self.properties.get(Properties.SNAP_TO_GRID)
        
        if self.block == BlockType.Text:
            if text:  data += f"{ord(text)},"
            else:     data += f"{Properties.TEXT.value},"
            
        if self.block == BlockType.Tile:
            colorData: str
            if color:  colorData = f"{color[0]}+{color[1]}+{color[2]}"
            else:      colorData += f"{Properties.COLOR.value[0]},{Properties.COLOR.value[1]},{Properties.COLOR.value[2]},"
            
            materialData: str
            if material:  materialData = str(material.value)
            else:         materialData = str(Properties.MATERIAL.value)
            
            collisionData: str
            if collision:  collisionData = str(collision.value)
            else:          collisionData = str(Properties.COLLISION.value)
            
            # Combine All Properties
            data += f"{colorData}+{materialData}+{collisionData},"
        
        if snapToGrid:  data += f"snapToGrid=False,"
        
        return f"{data};"
    
    def getPosition(self) -> tuple[number, number, number]:  return tuple(map(float, self.position))
    def getColor(self) -> tuple[int, int, int] | None:
        color = self.properties.get(Properties.COLOR)
        return color if color else Properties.COLOR.value
    
class Connection:
    def __init__(self, A: int, B: int) -> None:
        self.A = A
        self.B = B
    
    def encode(self) -> str:
        return f"{self.A},{self.B},;"

class Object:
    def __init__(self, blocks: list[Block] | None = [], connections: list[Connection] | None = []):
        self.blocks = set(blocks)
        self.connections = set(connections)
        
        self.objects = self.blocks.union(self.connections)

    def encode(self) -> str:
        data = ""
        for obj in self.objects:
            data += obj.encode()
        
        return f"{data[:-1]}???"
    
    @property
    def encoded(self) -> str:  return self.encode()
    
    @property
    def positions(self) -> str:  return str({block.getPosition() for block in self.blocks}).replace("{", "").replace("}", "")
    @property
    def colors(self) -> str:  return str({block.getColor() for block in self.blocks}).replace("{", "").replace("}", "")
    
    @property
    def vertices(self) -> str:  return str({(*block.getPosition(), *block.getColor()) for block in self.blocks}).replace("{", "").replace("}", "")

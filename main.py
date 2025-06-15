from enum import Enum
from json import load as loadJSON

from pygame.image import load as loadImage
from pygame import Surface, Vector3

from pyperclip import copy as copyToClipboard
from os import getcwd

from lib import *

class Axis(Enum):
    POSITIVE_X =  1, 0, 0
    NEGATIVE_X = -1, 0, 0
    
    POSITIVE_Y = 0,  1, 0
    NEGATIVE_Y = 0, -1, 0
    
    POSITIVE_Z = 0, 0,  1
    NEGATIVE_Z = 0, 0, -1

def createModelFromJSON(
        modelDir: str,
        resolution: tuple[int, int, int] | None = None
    ) -> Object:
    
    with open(modelDir) as f:
        modelJSON = loadJSON(f)
        
        if resolution is not None:
            resolution = Vector3(resolution)
        else:
            resolution = Vector3(16, 16, 16)
        
        textures = modelJSON["textures"]
        
        texturesAll = textures.get("all")
        if texturesAll:
            imageAll = loadImage(f"{texturePath}\\{texturesAll.removeprefix("minecraft:")}.png")

            top    = createObjectFromImage(imageAll, (resolution.x - 1, resolution.y - 1, -resolution.z),  resolution.xz, forward=Axis.POSITIVE_Y,  up=Axis.POSITIVE_Z)
            bottom = createObjectFromImage(imageAll, (0, 0, -resolution.z), resolution.xz, forward=Axis.NEGATIVE_Y,  up=Axis.POSITIVE_Z)
            east   = createObjectFromImage(imageAll, (resolution.x - 1, 0, 0),  resolution.yz, forward=Axis.POSITIVE_X,  up=Axis.POSITIVE_Y)
            west   = createObjectFromImage(imageAll, (0, 0, -resolution.z), resolution.yz, forward=Axis.NEGATIVE_X,  up=Axis.POSITIVE_Y)
            north  = createObjectFromImage(imageAll, (0, 0, 0),             resolution.xy, forward=Axis.POSITIVE_Z,  up=Axis.POSITIVE_Y)
            south  = createObjectFromImage(imageAll, (resolution.x - 1, 0, -resolution.z), resolution.xy, forward=Axis.NEGATIVE_Z,  up=Axis.POSITIVE_Y)
            
            blocks = set()
            for block in top.blocks.union(bottom.blocks):
                if block.position.x == 0 or block.position.x == -resolution.x:  continue
                if block.position.z == 0 or block.position.z == -resolution.z:  continue
                
                blocks.add(block)
            
            blocks = blocks.union(east.blocks)
            blocks = blocks.union(west.blocks)
            blocks = blocks.union(north.blocks)
            blocks = blocks.union(south.blocks)
            
            return Object(blocks)

def createObjectFromImage(
        image:      Surface,
        offset:     tuple[number, number, number] | None = (0, 0, 0),
        resolution: tuple[int, int] | None = None,
        forward:    Axis            | None = Axis.NEGATIVE_Z,
        up:         Axis            | None = Axis.POSITIVE_Y
    ) -> Object:
    
    blocks = set()
    imageSize = image.get_size()
    offset = Vector3(offset)
    
    if resolution is None:  resolution = imageSize
    
    spacing = imageSize[0] / resolution[0], imageSize[1] / resolution[1]
    for x in range(int(resolution[0])):
        for y in range(int(resolution[1])):
            
            position = x, resolution[1] - (y + 1), 0
            color = image.get_at((round(x * spacing[0]), round(y * spacing[1])))
            
            blocks.add(Block(
                BlockType.Tile, rotateVector(position, forward, up) + offset, {
                    Properties.COLOR: (color.r, color.g, color.b),
                    Properties.MATERIAL: Material.SMOOTH
                    }
            ))
    
    return Object(blocks)

def rotateVector(vector: tuple[number, number, number], forward: Axis, up: Axis) -> Vector3:
    vector = Vector3(vector)
    
    f = Vector3(forward.value)
    u = Vector3(up.value)
    r = Vector3.cross(u, f)

    return Vector3(
        vector.x * r.x + vector.y * u.x + vector.z * f.x,
        vector.x * r.y + vector.y * u.y + vector.z * f.y,
        vector.x * r.z + vector.y * u.z + vector.z * f.z
    )
    
if __name__ == "__main__":

    assets = f"{getcwd()}\\Minecraft-Assets\\minecraft"

    modelPath   = f"{assets}\\models"
    texturePath = f"{assets}\\textures"
    
    model = f"{modelPath}\\block\\cracked_polished_blackstone_bricks.json"  # Change This

    obj = createModelFromJSON(model)
    
    print(f"Total blocks created: {len(obj.blocks)}")
    copyToClipboard(obj.encoded)
    print("Model object copied to clipboard!")

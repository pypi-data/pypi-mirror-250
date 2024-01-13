# BrainGenix-NES
# AGPLv3


def GetID(_Object):

    ShapeID = None
    if (type(_Object) == str):
        ShapeID = str(_Object)
    elif (type(_Object) == int):
        ShapeID = str(_Object)
    else:
        ShapeID = str(_Object.ID)

    return ShapeID
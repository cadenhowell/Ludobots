from pyrosim.commonFunctions import Save_Whitespace

class GEOMETRY_URDF: 

    def __init__(self,size, objectType):

        self.depth   = 3

        self.string1 = '<geometry>'

        if objectType == 'box':
            sizeString = str(size[0]) + " " + str(size[1]) + " " + str(size[2])
            self.string2 = ' <box size="' + sizeString + '" />'
        elif objectType == 'sphere':
            sizeString = str(size[0])
            self.string2 = ' <sphere radius="' + sizeString + '" />'
        elif objectType == 'cylinder':
            self.string2 = ' <cylinder length="' + str(size[0]) + '" radius="' + str(size[1]) + '" />'


        self.string3 = '</geometry>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )

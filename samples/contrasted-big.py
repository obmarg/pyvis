import hashlib
import os

word = 'Martin'

hash = hashlib.md5( word ).hexdigest()

chunks = [ hash[ i * 6 : (i+1) *6 ] for i in range(3) ]

svgHead = '''
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     version="1.1"
     baseProfile="full"
     width="840"
     height="315">
'''

svgFoot = '''
</svg>
'''

def YiqContrast( color ):
    '''
    Gets a contrast value
    @param: color.  Color string without # prefix
    @return: >= 0 is Close to black
    '''
    r = int( color[0:2], 16 )
    g = int( color[2:4], 16 )
    b = int( color[4:6], 16 )
    return ( ( r *299 ) + ( g * 587 ) + ( b * 114 ) ) /1000

def DrawRect( coords, width, height, color ):
    '''
    Draws a rectangle
    @param: coords  The coordinates of the upper left
    @param: width   The width
    @param: height  The height
    @param: color  The color
    '''
    rv = '<rect x="{}" y="{}" height="{}" width="{}"'.format(
            coords[0], coords[1], height, width
            )
    rv += ' style="fill:{}" />'.format( color )
    return rv

def DrawRightAngleTriangle( coords, len, color, upsideDown=False ):
    '''
    Draws a triangle
    @param: coords  The coordinates of the right angle
    @param: len Length of the side
    @param: color  The color to draw in hex
    @param: upsideDown  True if the triangle is upside down
    '''
    rv = '<polygon points="'
    if upsideDown:
        len = -len
    transform = [ ( 0, len ), ( len, len ), ( 0, 0 ) ]
    strList = []
    for i in range( 3 ):
        c = [ str( o + t ) for o, t in zip( coords, transform[ i ] ) ]
        strList.append( ','.join( c ) )
    rv += ' '.join( strList )
    rv += '" style="fill:' + color + '" />'
    return rv

content = ''

rectcolor = '#FFFFFF'
contrasts = [ YiqContrast( chunks[ i ] ) for i in range( 3 ) ]
print contrasts
avg = sum( contrasts ) / 3
if avg < 128:
    rectcolor = '#000000'

content += DrawRect( ( 0,0 ), 840, 315, rectcolor )

for x in range( 0, 840, 42 ):
    for y in range( 0, 318, 42 ):
        content += DrawRightAngleTriangle( 
            ( x, y ), 42, '#' + chunks[ ( (x/42) + (y/42) ) % 3 ]  
            )

output = svgHead + content + svgFoot

img = '1.svg'
if os.path.exists( img ):
    if os.path.exists( '2.svg' ):
        os.unlink( img )
    else:
        img = '2.svg'

with open( img, 'w' ) as f:
    f.write( output )

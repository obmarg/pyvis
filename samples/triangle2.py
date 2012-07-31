import hashlib
import os

word = 'Graeme Coupar'

hash = hashlib.md5( word ).hexdigest()

chunks = [ hash[ i * 6 : (i+1) *6 ] for i in range(3) ]

svgHead = '''
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     version="1.1"
     baseProfile="full"
     width="10"
     height="10">
'''

svgFoot = '''
</svg>
'''

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

for x in range( 10 ):
    for y in range( 10 ):
        content += DrawRightAngleTriangle( 
                ( x, y ), 1, '#' + chunks[ (x + y) % 3 ]
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

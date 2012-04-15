#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
import os
import logging
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QObject
from PyQt4 import QtCore, QtGui, Qsci, QtSvg
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase
from PyQt4.Qsci import QsciLexerPython

class Editor(QObject):
    def __init__( self ):
        super( Editor, self ).__init__()
        self._WriteModule()
        import temp
        self.module = temp

    def Setup( self, parentWidget ):
        editor = QsciScintilla( parentWidget )
        editor.resize( 512, 768 ) 
        
        # Set up the font
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setFixedPitch(True)
        font.setPointSize(13)
        fm = QtGui.QFontMetrics(font)

        editor.setFont( font )
        editor.setMarginsFont( font )

        # Add in line numbers
        editor.setMarginWidth( 0, fm.width("000") + 5 )
        editor.setMarginLineNumbers( 0, True )

        editor.setBraceMatching( QsciScintilla.SloppyBraceMatch )

        # Set up a python lexer
        lexer = QsciLexerPython()
        lexer.setDefaultFont( font )
        editor.setLexer( lexer )

        # Set up indentation
        editor.setAutoIndent( True )
        editor.setIndentationsUseTabs( False )
        editor.setTabWidth( 4 )

        self.editor = editor
        self.editor.linesChanged.connect( self.OnChange )

    changeImage = QtCore.pyqtSignal( 'QString' )

    @QtCore.pyqtSlot()
    def OnChange( self ):
        # TODO: Check syntax etc.
        s = self.editor.text()
        self._WriteModule( s )
        if self._ReloadModule():
            try:
                if self.module.img:
                    self.changeImage.emit( self.module.img )
            except AttributeError:
                # img probably just doesn't exist
                pass
                    
   
    def _WriteModule( self, code=None ):
        '''
        Writes code to the module
        @param: code    The code to write (optional)
        '''
        with open( 'temp.py', 'w' ) as t:
            if code:
                logging.debug( 'Writing code' )
                t.write( code )

    def _ReloadModule( self ):
        '''
        Reloads the module
        @return: True if succesfull, False otherwise
        '''
        try:
            logging.debug( "Reloading module" )
            reload( self.module )
            logging.debug( "Reloaded module" )
            return True
        except:
            return False

class PyVisWindow(QtGui.QMainWindow):
    def __init__( self ):
        super( PyVisWindow, self ).__init__()

        self._InitUi()

    @QtCore.pyqtSlot('QString')
    def SetImage( self, img ):
        self.image.load( img )

    def _InitUi( self ):
        exitAction = QtGui.QAction( QtGui.QIcon( 'exit.png' ), '&Exit', self )
        exitAction.setShortcut( 'Ctrl+Q' )
        exitAction.setStatusTip( 'Exit application' )
        exitAction.triggered.connect( QtGui.qApp.quit )

        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu( '&File' )
        fileMenu.addAction( exitAction )
        
        self.resize( 1024, 768 )
        self.setWindowTitle( 'PyVis' )

        self.editor = Editor()
        self.editor.Setup( self )
        self.editor.changeImage.connect( self.SetImage )

        self.image = QtSvg.QSvgWidget( 'Broom_icon.svg', self )
        self.image.move( 512, 0 )
        self.image.resize( self.image.sizeHint() )
        
        self.show()


if __name__ == "__main__":
    logging.basicConfig( level=logging.DEBUG )
    # Create Qt application and the QDeclarative view
    app = QApplication(sys.argv)

    w = PyVisWindow()

    # Enter Qt main loop
    sys.exit(app.exec_())

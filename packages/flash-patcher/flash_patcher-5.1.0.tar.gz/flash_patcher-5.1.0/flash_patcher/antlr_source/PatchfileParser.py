# Generated from ../flash_patcher/antlr_source/PatchfileParser.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,20,99,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,1,0,1,0,1,0,1,0,1,1,4,1,26,8,1,11,1,12,
        1,27,1,1,1,1,1,1,1,1,1,2,4,2,35,8,2,11,2,12,2,36,1,3,1,3,1,3,1,3,
        1,3,1,3,1,4,1,4,1,4,1,4,1,5,4,5,50,8,5,11,5,12,5,51,1,5,1,5,1,5,
        1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,7,4,7,71,8,
        7,11,7,12,7,72,1,8,1,8,1,8,1,8,5,8,79,8,8,10,8,12,8,82,9,8,1,9,3,
        9,85,8,9,1,9,1,9,1,9,3,9,90,8,9,1,9,3,9,93,8,9,1,9,1,9,3,9,97,8,
        9,1,9,0,0,10,0,2,4,6,8,10,12,14,16,18,0,0,101,0,20,1,0,0,0,2,25,
        1,0,0,0,4,34,1,0,0,0,6,38,1,0,0,0,8,44,1,0,0,0,10,49,1,0,0,0,12,
        60,1,0,0,0,14,70,1,0,0,0,16,80,1,0,0,0,18,96,1,0,0,0,20,21,5,1,0,
        0,21,22,5,5,0,0,22,23,3,18,9,0,23,1,1,0,0,0,24,26,3,0,0,0,25,24,
        1,0,0,0,26,27,1,0,0,0,27,25,1,0,0,0,27,28,1,0,0,0,28,29,1,0,0,0,
        29,30,5,6,0,0,30,31,3,4,2,0,31,32,5,17,0,0,32,3,1,0,0,0,33,35,5,
        18,0,0,34,33,1,0,0,0,35,36,1,0,0,0,36,34,1,0,0,0,36,37,1,0,0,0,37,
        5,1,0,0,0,38,39,5,2,0,0,39,40,5,5,0,0,40,41,3,18,9,0,41,42,5,13,
        0,0,42,43,3,18,9,0,43,7,1,0,0,0,44,45,5,3,0,0,45,46,5,5,0,0,46,47,
        3,18,9,0,47,9,1,0,0,0,48,50,3,8,4,0,49,48,1,0,0,0,50,51,1,0,0,0,
        51,49,1,0,0,0,51,52,1,0,0,0,52,53,1,0,0,0,53,54,5,7,0,0,54,55,3,
        14,7,0,55,56,5,19,0,0,56,57,5,6,0,0,57,58,3,4,2,0,58,59,5,17,0,0,
        59,11,1,0,0,0,60,61,5,4,0,0,61,62,5,5,0,0,62,63,5,7,0,0,63,64,3,
        14,7,0,64,65,5,19,0,0,65,66,5,6,0,0,66,67,3,4,2,0,67,68,5,17,0,0,
        68,13,1,0,0,0,69,71,5,20,0,0,70,69,1,0,0,0,71,72,1,0,0,0,72,70,1,
        0,0,0,72,73,1,0,0,0,73,15,1,0,0,0,74,79,3,2,1,0,75,79,3,6,3,0,76,
        79,3,10,5,0,77,79,3,12,6,0,78,74,1,0,0,0,78,75,1,0,0,0,78,76,1,0,
        0,0,78,77,1,0,0,0,79,82,1,0,0,0,80,78,1,0,0,0,80,81,1,0,0,0,81,17,
        1,0,0,0,82,80,1,0,0,0,83,85,5,10,0,0,84,83,1,0,0,0,84,85,1,0,0,0,
        85,86,1,0,0,0,86,87,5,8,0,0,87,89,5,14,0,0,88,90,5,12,0,0,89,88,
        1,0,0,0,89,90,1,0,0,0,90,92,1,0,0,0,91,93,5,11,0,0,92,91,1,0,0,0,
        92,93,1,0,0,0,93,97,1,0,0,0,94,97,5,12,0,0,95,97,5,9,0,0,96,84,1,
        0,0,0,96,94,1,0,0,0,96,95,1,0,0,0,97,19,1,0,0,0,10,27,36,51,72,78,
        80,84,89,92,96
    ]

class PatchfileParser ( Parser ):

    grammarFileName = "PatchfileParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'('", "')'", "<INVALID>", 
                     "'-'" ]

    symbolicNames = [ "<INVALID>", "ADD", "REMOVE", "REPLACE", "REPLACE_ALL", 
                      "FILENAME", "BEGIN_PATCH", "BEGIN_CONTENT", "FUNCTION", 
                      "END", "OPEN_BLOCK", "CLOSE_BLOCK", "INTEGER", "DASH", 
                      "FUNCTION_NAME", "WHITESPACE", "COMMENT", "END_PATCH", 
                      "AS_TEXT", "END_CONTENT", "CONTENT_TEXT" ]

    RULE_addBlockHeader = 0
    RULE_addBlock = 1
    RULE_addBlockText = 2
    RULE_removeBlock = 3
    RULE_replaceNthBlockHeader = 4
    RULE_replaceNthBlock = 5
    RULE_replaceAllBlock = 6
    RULE_replaceBlockText = 7
    RULE_root = 8
    RULE_locationToken = 9

    ruleNames =  [ "addBlockHeader", "addBlock", "addBlockText", "removeBlock", 
                   "replaceNthBlockHeader", "replaceNthBlock", "replaceAllBlock", 
                   "replaceBlockText", "root", "locationToken" ]

    EOF = Token.EOF
    ADD=1
    REMOVE=2
    REPLACE=3
    REPLACE_ALL=4
    FILENAME=5
    BEGIN_PATCH=6
    BEGIN_CONTENT=7
    FUNCTION=8
    END=9
    OPEN_BLOCK=10
    CLOSE_BLOCK=11
    INTEGER=12
    DASH=13
    FUNCTION_NAME=14
    WHITESPACE=15
    COMMENT=16
    END_PATCH=17
    AS_TEXT=18
    END_CONTENT=19
    CONTENT_TEXT=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class AddBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ADD(self):
            return self.getToken(PatchfileParser.ADD, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self):
            return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlockHeader" ):
                listener.enterAddBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlockHeader" ):
                listener.exitAddBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlockHeader" ):
                return visitor.visitAddBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def addBlockHeader(self):

        localctx = PatchfileParser.AddBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_addBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.match(PatchfileParser.ADD)
            self.state = 21
            self.match(PatchfileParser.FILENAME)
            self.state = 22
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def addBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlock" ):
                listener.enterAddBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlock" ):
                listener.exitAddBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlock" ):
                return visitor.visitAddBlock(self)
            else:
                return visitor.visitChildren(self)




    def addBlock(self):

        localctx = PatchfileParser.AddBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_addBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 24
                self.addBlockHeader()
                self.state = 27 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 29
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 30
            self.addBlockText()
            self.state = 31
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AddBlockTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AS_TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(PatchfileParser.AS_TEXT)
            else:
                return self.getToken(PatchfileParser.AS_TEXT, i)

        def getRuleIndex(self):
            return PatchfileParser.RULE_addBlockText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddBlockText" ):
                listener.enterAddBlockText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddBlockText" ):
                listener.exitAddBlockText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddBlockText" ):
                return visitor.visitAddBlockText(self)
            else:
                return visitor.visitChildren(self)




    def addBlockText(self):

        localctx = PatchfileParser.AddBlockTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_addBlockText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 33
                self.match(PatchfileParser.AS_TEXT)
                self.state = 36 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==18):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RemoveBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REMOVE(self):
            return self.getToken(PatchfileParser.REMOVE, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.LocationTokenContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,i)


        def DASH(self):
            return self.getToken(PatchfileParser.DASH, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_removeBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRemoveBlock" ):
                listener.enterRemoveBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRemoveBlock" ):
                listener.exitRemoveBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRemoveBlock" ):
                return visitor.visitRemoveBlock(self)
            else:
                return visitor.visitChildren(self)




    def removeBlock(self):

        localctx = PatchfileParser.RemoveBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_removeBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(PatchfileParser.REMOVE)
            self.state = 39
            self.match(PatchfileParser.FILENAME)
            self.state = 40
            self.locationToken()
            self.state = 41
            self.match(PatchfileParser.DASH)
            self.state = 42
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceNthBlockHeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPLACE(self):
            return self.getToken(PatchfileParser.REPLACE, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def locationToken(self):
            return self.getTypedRuleContext(PatchfileParser.LocationTokenContext,0)


        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceNthBlockHeader

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceNthBlockHeader" ):
                listener.enterReplaceNthBlockHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceNthBlockHeader" ):
                listener.exitReplaceNthBlockHeader(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceNthBlockHeader" ):
                return visitor.visitReplaceNthBlockHeader(self)
            else:
                return visitor.visitChildren(self)




    def replaceNthBlockHeader(self):

        localctx = PatchfileParser.ReplaceNthBlockHeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_replaceNthBlockHeader)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(PatchfileParser.REPLACE)
            self.state = 45
            self.match(PatchfileParser.FILENAME)
            self.state = 46
            self.locationToken()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceNthBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_CONTENT(self):
            return self.getToken(PatchfileParser.BEGIN_CONTENT, 0)

        def replaceBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.ReplaceBlockTextContext,0)


        def END_CONTENT(self):
            return self.getToken(PatchfileParser.END_CONTENT, 0)

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def replaceNthBlockHeader(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceNthBlockHeaderContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceNthBlockHeaderContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceNthBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceNthBlock" ):
                listener.enterReplaceNthBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceNthBlock" ):
                listener.exitReplaceNthBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceNthBlock" ):
                return visitor.visitReplaceNthBlock(self)
            else:
                return visitor.visitChildren(self)




    def replaceNthBlock(self):

        localctx = PatchfileParser.ReplaceNthBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_replaceNthBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 48
                self.replaceNthBlockHeader()
                self.state = 51 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==3):
                    break

            self.state = 53
            self.match(PatchfileParser.BEGIN_CONTENT)
            self.state = 54
            self.replaceBlockText()
            self.state = 55
            self.match(PatchfileParser.END_CONTENT)
            self.state = 56
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 57
            self.addBlockText()
            self.state = 58
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceAllBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPLACE_ALL(self):
            return self.getToken(PatchfileParser.REPLACE_ALL, 0)

        def FILENAME(self):
            return self.getToken(PatchfileParser.FILENAME, 0)

        def BEGIN_CONTENT(self):
            return self.getToken(PatchfileParser.BEGIN_CONTENT, 0)

        def replaceBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.ReplaceBlockTextContext,0)


        def END_CONTENT(self):
            return self.getToken(PatchfileParser.END_CONTENT, 0)

        def BEGIN_PATCH(self):
            return self.getToken(PatchfileParser.BEGIN_PATCH, 0)

        def addBlockText(self):
            return self.getTypedRuleContext(PatchfileParser.AddBlockTextContext,0)


        def END_PATCH(self):
            return self.getToken(PatchfileParser.END_PATCH, 0)

        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceAllBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceAllBlock" ):
                listener.enterReplaceAllBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceAllBlock" ):
                listener.exitReplaceAllBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceAllBlock" ):
                return visitor.visitReplaceAllBlock(self)
            else:
                return visitor.visitChildren(self)




    def replaceAllBlock(self):

        localctx = PatchfileParser.ReplaceAllBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_replaceAllBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(PatchfileParser.REPLACE_ALL)
            self.state = 61
            self.match(PatchfileParser.FILENAME)
            self.state = 62
            self.match(PatchfileParser.BEGIN_CONTENT)
            self.state = 63
            self.replaceBlockText()
            self.state = 64
            self.match(PatchfileParser.END_CONTENT)
            self.state = 65
            self.match(PatchfileParser.BEGIN_PATCH)
            self.state = 66
            self.addBlockText()
            self.state = 67
            self.match(PatchfileParser.END_PATCH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReplaceBlockTextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTENT_TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(PatchfileParser.CONTENT_TEXT)
            else:
                return self.getToken(PatchfileParser.CONTENT_TEXT, i)

        def getRuleIndex(self):
            return PatchfileParser.RULE_replaceBlockText

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReplaceBlockText" ):
                listener.enterReplaceBlockText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReplaceBlockText" ):
                listener.exitReplaceBlockText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReplaceBlockText" ):
                return visitor.visitReplaceBlockText(self)
            else:
                return visitor.visitChildren(self)




    def replaceBlockText(self):

        localctx = PatchfileParser.ReplaceBlockTextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_replaceBlockText)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 69
                self.match(PatchfileParser.CONTENT_TEXT)
                self.state = 72 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==20):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.AddBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.AddBlockContext,i)


        def removeBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.RemoveBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.RemoveBlockContext,i)


        def replaceNthBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceNthBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceNthBlockContext,i)


        def replaceAllBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PatchfileParser.ReplaceAllBlockContext)
            else:
                return self.getTypedRuleContext(PatchfileParser.ReplaceAllBlockContext,i)


        def getRuleIndex(self):
            return PatchfileParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = PatchfileParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0):
                self.state = 78
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1]:
                    self.state = 74
                    self.addBlock()
                    pass
                elif token in [2]:
                    self.state = 75
                    self.removeBlock()
                    pass
                elif token in [3]:
                    self.state = 76
                    self.replaceNthBlock()
                    pass
                elif token in [4]:
                    self.state = 77
                    self.replaceAllBlock()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 82
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocationTokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PatchfileParser.RULE_locationToken

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class FunctionContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FUNCTION(self):
            return self.getToken(PatchfileParser.FUNCTION, 0)
        def FUNCTION_NAME(self):
            return self.getToken(PatchfileParser.FUNCTION_NAME, 0)
        def OPEN_BLOCK(self):
            return self.getToken(PatchfileParser.OPEN_BLOCK, 0)
        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)
        def CLOSE_BLOCK(self):
            return self.getToken(PatchfileParser.CLOSE_BLOCK, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)


    class EndContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def END(self):
            return self.getToken(PatchfileParser.END, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnd" ):
                listener.enterEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnd" ):
                listener.exitEnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnd" ):
                return visitor.visitEnd(self)
            else:
                return visitor.visitChildren(self)


    class LineNumberContext(LocationTokenContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a PatchfileParser.LocationTokenContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INTEGER(self):
            return self.getToken(PatchfileParser.INTEGER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineNumber" ):
                listener.enterLineNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineNumber" ):
                listener.exitLineNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLineNumber" ):
                return visitor.visitLineNumber(self)
            else:
                return visitor.visitChildren(self)



    def locationToken(self):

        localctx = PatchfileParser.LocationTokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_locationToken)
        self._la = 0 # Token type
        try:
            self.state = 96
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8, 10]:
                localctx = PatchfileParser.FunctionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==10:
                    self.state = 83
                    self.match(PatchfileParser.OPEN_BLOCK)


                self.state = 86
                self.match(PatchfileParser.FUNCTION)
                self.state = 87
                self.match(PatchfileParser.FUNCTION_NAME)
                self.state = 89
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 88
                    self.match(PatchfileParser.INTEGER)


                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==11:
                    self.state = 91
                    self.match(PatchfileParser.CLOSE_BLOCK)


                pass
            elif token in [12]:
                localctx = PatchfileParser.LineNumberContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 94
                self.match(PatchfileParser.INTEGER)
                pass
            elif token in [9]:
                localctx = PatchfileParser.EndContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 95
                self.match(PatchfileParser.END)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






# Generated from ../flash_patcher/antlr_source/PatchfileParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .PatchfileParser import PatchfileParser
else:
    from PatchfileParser import PatchfileParser

# This class defines a complete generic visitor for a parse tree produced by PatchfileParser.

class PatchfileParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PatchfileParser#addBlockHeader.
    def visitAddBlockHeader(self, ctx:PatchfileParser.AddBlockHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#addBlock.
    def visitAddBlock(self, ctx:PatchfileParser.AddBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#addBlockText.
    def visitAddBlockText(self, ctx:PatchfileParser.AddBlockTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#removeBlock.
    def visitRemoveBlock(self, ctx:PatchfileParser.RemoveBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#replaceNthBlockHeader.
    def visitReplaceNthBlockHeader(self, ctx:PatchfileParser.ReplaceNthBlockHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#replaceNthBlock.
    def visitReplaceNthBlock(self, ctx:PatchfileParser.ReplaceNthBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#replaceAllBlock.
    def visitReplaceAllBlock(self, ctx:PatchfileParser.ReplaceAllBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#replaceBlockText.
    def visitReplaceBlockText(self, ctx:PatchfileParser.ReplaceBlockTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#root.
    def visitRoot(self, ctx:PatchfileParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#function.
    def visitFunction(self, ctx:PatchfileParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#lineNumber.
    def visitLineNumber(self, ctx:PatchfileParser.LineNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PatchfileParser#end.
    def visitEnd(self, ctx:PatchfileParser.EndContext):
        return self.visitChildren(ctx)



del PatchfileParser
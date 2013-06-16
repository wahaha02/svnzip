#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
# Purpose: collect files which you changed and base vision in svn for
#          code compare and code review.
# Dependency: need install subversion version 1.6.5 or above.
# Usage: svnzip.py (folder which you checkout from svn)
# Initial Version by Alex
######################################################################


import os
import sys

DEBUG = 0


class svnzip:
    def __init__(self, folder=''):
        self.target_folder = folder
        self.MFolder = 'MODI' 
        self.BFolder = 'BASE'
        self.temp = 'DIFF'
        self.codingtype = sys.getfilesystemencoding()
        
        if os.path.isdir( self.MFolder ):
            os.system('rm -rf %s' %(self.MFolder))

        if os.path.isdir( self.BFolder ):
            os.system('rm -rf %s' %(self.BFolder))
        
        if os.path.isfile( self.MFolder+'.zip' ):
            os.system('rm -f %s.zip' %(self.MFolder))

        if os.path.isfile( self.BFolder+'.zip' ):
            os.system('rm -f %s.zip' %(self.BFolder))
            
        os.system('mkdir %s' %(self.MFolder))
        os.system('mkdir %s' %(self.BFolder))
    
    def echo_exec(self, s):
        # print 'CMD: ', s, '\n'
        os.system( s ) 
        return s
                            
    def do(self, ):
        
        s = 'svn diff %s' %(self.target_folder)
        for diff_line in os.popen(s).readlines():
            diff = diff_line.replace('\n', '').split(": ")
            if diff[0] == 'Index':
            	name = diff[1]
            	Rev = ''
            	URL = ''
            	Note = ''

                for info_line in os.popen('svn info %s' %(name) ).readlines():
                    i = info_line.replace('\n', '').split(": ")
                    if len(i) == 2:
                        if i[0]=='Revision' or i[0]=='版本'.decode('UTF-8').encode(self.codingtype):
                            Rev = i[1] 
                        if i[0]=='URL':   
                            URL = i[1]
                        if i[0]=='Schedule' or i[0]=='调度'.decode('UTF-8').encode(self.codingtype):
                            Note = i[1]

                
                print 'MODIFIED FILE[%6s]: %s' %(Note, name)
                self.echo_exec( 'mkdir -p %s/%s'  %(self.MFolder, os.path.dirname(name)) )
                self.echo_exec( 'mkdir -p %s/%s'  %(self.BFolder, os.path.dirname(name)) )
                
                if Note != 'delete' and Note != '删除'.decode('UTF-8').encode(self.codingtype):
                	self.echo_exec( 'cp %s %s/%s'  %(diff[1], self.MFolder, name) )
                	
                if Note != 'add' and Note != '添加'.decode('UTF-8').encode(self.codingtype):
                	self.echo_exec( 'svn export -q %s@%s --force %s/%s' %(URL, Rev, self.BFolder, name) )
        
        self.echo_exec( 'mv %s %s'  %(self.MFolder, self.temp) )   
        self.echo_exec( 'zip -qr %s.zip %s'  %(self.MFolder, self.temp) )    
        self.echo_exec( 'rm -rf %s' %(self.temp) )
   
        self.echo_exec( 'mv %s %s'  %(self.BFolder, self.temp) )
        self.echo_exec( 'zip -qr %s.zip %s'  %(self.BFolder, self.temp) )
        self.echo_exec( 'rm -rf %s' %(self.temp) )

app = svnzip( sys.argv[1] )
app.do()





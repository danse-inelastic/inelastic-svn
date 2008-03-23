# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.components.Component import Component
class Clerk(Component):

    def __init__(self, *args, **kwds):
        Component.__init__(self, *args, **kwds)
        self.getHierarchy = HierarchyRetriever(self)
        return
    

    def indexUsers(self, where=None):
        """create an index of all users that meet the specified criteria"""
        from vnf.dom.User import User
        index = {}
        users = self.db.fetchall(User, where=where)
        for user in users:
            index[user.username] = user
            continue
        return index
    

    def indexActiveUsers(self):
        """create an index of all active users"""
        return self.indexUsers()
        return self.indexUsers(where="status='a'")


    def indexJobs(self, where = None):
        '''create and index of all jobs'''
        from vnf.dom.Job import Job
        return self._index( Job, where )


    def indexSampleAssemblies(self, where = None):
        """create an index of all sample assemblies
        that meet the specified criteria"""
        from vnf.dom.SampleAssembly import SampleAssembly
        return self._index( SampleAssembly, where )


    def indexScatterers(self, where = None):
        '''create and index of all scatterers
        that meet the specified criteria'''
        from vnf.dom.Scatterer import Scatterer
        return self._index( Scatterer, where )


    def indexServers(self, where = None):
        '''create and index of all servers
        that meet the specified criteria'''

        from vnf.dom.Scatterer import Scatterer
        return self._index( Scatterer, where )


    def updateRecord(self, record):
        id = record.id
        where = "id='%s'" % id
        
        assignments = []
        
        for column in record.getColumnNames():
            value = getattr( record, column )
            assignments.append( (column, value) )
            continue
        
        self.db.updateRow(record, assignments, where)
        return


    def getRecordByID(self, tablename, id):
        exec 'from vnf.dom.%s import %s as Table' % (tablename, tablename) \
             in locals()
        return self._getRecordByID( Table, id )
        

    def getCrystal(self, id):
        '''retrieve crystal of given id'''
        from vnf.dom.Crystal import Crystal
        return self._getRecordByID( Crystal, id )

    
    def getJob(self, id):
        '''retrieve job of given id'''
        from vnf.dom.Job import Job
        return self._getRecordByID( Job, id )


    def getRealScatterer(self, id):
        '''given id in the scatter table, retrieve the real
        scatterer's record.
        The scatter table contains type and reference_id
        info of the scatterer.
        To look up the real scatterer, we have to
        go to the table of the given scatterer type
        and find the record of given id.
        '''
        from vnf.dom.Scatterer import Scatterer
        record = self.getScatterer( id )
        type = record.type
        id1 = record.reference
        exec "from vnf.dom.%s import %s as Table" % (type, type)
        scatterer = self._getRecordByID( Table, id1 )
        return scatterer


    def getSample(self, id):
        '''retrieve sample of given id'''
        from vnf.dom.Sample import Sample
        return self._getRecordByID( Sample, id )


    def getSampleAssembly(self, id):
        '''retrieve sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        return self._getRecordByID( SampleAssembly, id )


    def getScatterer(self, id):
        '''retrieve scatterer of given id'''
        from vnf.dom.Scatterer import Scatterer
        return self._getRecordByID( Scatterer, id )

    
    def getScattererIDs(self, id):
        '''retrieve ids of scatterers in the sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        records = self.db.fetchall(
            SampleAssembly.Scatterers, where = "localkey='%s'" % id )
        scattererIDs = [
            record.remotekey for record in records]
        return scattererIDs

    
    def getScatterers(self, id):
        '''retrieve scatterers in the sample assembly of given id'''
        ids = self.getScattererIDs( id )
        from vnf.dom.Scatterer import Scatterer
        ret = []
        for id in ids:
            record = self._getRecordByID( Scatterer, id )
            ret.append( record )
            continue
        return ret    


    def getServer(self, id):
        '''retrieve server of given id'''
        from vnf.dom.Server import Server
        return self._getRecordByID( Server, id )


    def getShape(self, id):
        '''retrieve shape of given id'''
        from vnf.dom.Shape import Shape
        return self._getRecordByID( Shape, id )


    def getRealShape(self, id):
        '''given id in the shape table, retrieve the real
        shape's record.
        The shape table contains type and reference_id
        info of the shape.
        To look up the real shape, we have to
        go to the table of the given shape type
        and find the record of given id.
        '''
        from vnf.dom.Shape import Shape
        record = self.getShape( id )
        
        type = record.type
        id1 = record.reference
        
        exec "from vnf.dom.%s import %s as Table" % (type, type)
        shape = self._getRecordByID( Table, id1 )
        
        return shape


    def getCrystal(self, id):
        '''retrieve crystal of given id'''
        from vnf.dom.Crystal import Crystal
        return self._getRecordByID( Crystal, id )


    def _index(self, table, where = None):
        index = {}
        all = self.db.fetchall(table, where=where)
        for item in all:
            index[item.id] = item
            continue
        return index

    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        return all[0]

    pass # end of Clerk




class HierarchyRetriever:

    def __init__(self, clerk):
        self.clerk = clerk
        return
    

    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onSampleAssembly(self, sampleassembly):
        scatterers = self.clerk.getScatterers( sampleassembly.id )
        scatterers = [ self( scatterer ) for scatterer in scatterers ]
        sampleassembly.scatterers = scatterers
        return sampleassembly


    def onScatterer(self, scatterer):
        realscatterer = self.clerk.getRealScatterer( scatterer.id )
        scatterer.realscatterer = self(realscatterer)
        return scatterer


    def onPolyXtalScatterer(self, scatterer):
        shape_id = scatterer.shape_id
        shape = self.clerk.getShape( shape_id )
        shape = self(shape)
        scatterer.shape = shape

        crystal_id = scatterer.crystal_id
        crystal = self.clerk.getCrystal( crystal_id )
        crystal = self(crystal)
        scatterer.crystal = crystal
        
        return scatterer


    def onCrystal(self, crystal):
        return crystal


    def onShape(self, shape):
        realshape = self.clerk.getRealShape( shape.id )
        shape.realshape = self(realshape)
        return shape


    def onBlock(self, block):
        return block
        

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Fri Mar 14 22:18:28 2008

# End of file 

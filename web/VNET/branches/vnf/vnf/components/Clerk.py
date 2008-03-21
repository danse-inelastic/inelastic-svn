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


    def indexUsers(self, where=None):
        """create an index of all users that meet the specified criteria"""
    
        from vnf.dom.User import User
        index = {}
        users = self.db.fetchall(User, where=where)
        for user in users:
            index[user.username] = user

        return index


    def indexActiveUsers(self):
        """create an index of all active users"""
        return self.indexUsers()
        return self.indexUsers(where="status='a'")


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


    def getSampleAssembly(self, id):
        '''retrieve sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        return self._getRecordByID( SampleAssembly, id )


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


    def getScatterer(self, id):
        '''retrieve scatterer of given id'''
        from vnf.dom.Scatterer import Scatterer
        return self._getRecordByID( Scatterer, id )


    def getShape(self, id):
        '''retrieve shape of given id'''
        from vnf.dom.Shape import Shape
        return self._getRecordByID( Shape, id )


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



# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Fri Mar 14 22:18:28 2008

# End of file 

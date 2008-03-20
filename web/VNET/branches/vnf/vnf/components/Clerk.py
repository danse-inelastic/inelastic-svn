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
        index = {}
        all = self.db.fetchall(SampleAssembly, where=where)
        for item in all:
            index[item.id] = item
            continue
        
        return index


    def getSampleAssembly(self, id):
        '''retrieve sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        all = self.db.fetchall( SampleAssembly, where = "id='%s'" % id )
        return all[0]


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
            record = self.db.fetchall(
                Scatterer, where = "id='%s'" % id )[0]
            
            type = record.type
            id1 = record.reference

            exec "from vnf.dom.%s import %s as Table" % (type, type)
            scatterer = self.db.fetchall(
                Table, where = "id='%s'" % id1 )[0]

            ret.append( scatterer )

            continue
            
        return ret


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Fri Mar 14 22:18:28 2008

# End of file 

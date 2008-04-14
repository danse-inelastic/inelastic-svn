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
        '''create and index all jobs'''
        from vnf.dom.Job import Job
        return self._index( Job, where )

    def indexInstruments(self, where = None):
        """create an index of all instruments
        that meet the specified criteria"""
        from vnf.dom.Instrument import Instrument
        return self._index( Instrument, where )

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


    def indexNeutronExperiments(self, where = None):
        from vnf.dom.NeutronExperiment import NeutronExperiment
        return self._index( NeutronExperiment, where )


    def updateRecord(self, record):
        id = record.id
        where = "id='%s'" % id
        
        assignments = []
        
        for column in record.getColumnNames():
            value = getattr( record, column )
            value = _tostr( value )
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
    
    
    def getJobs(self, where = None):
        '''retrieve all jobs'''
        from vnf.dom.Job import Job
        return self._getAll( Job, where )


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
        return self._getRealObject( id, Scatterer )


    def getRealComponent(self, id):
        '''given id in the component table, retrieve the real
        component's record.
        The component table contains type and reference_id
        info of the component.
        To look up the real component, we have to
        go to the table of the given component type
        and find the record of given id.
        '''
        from vnf.dom.Component import Component
        return self._getRealObject( id, Component )


    def getSample(self, id):
        '''retrieve sample of given id'''
        from vnf.dom.Sample import Sample
        return self._getRecordByID( Sample, id )
    
    def getSamples(self, where = None):
        '''retrieve all samples'''
        from vnf.dom.Sample import Sample
        return self._getAll( Sample, where )

    def getSampleAssembly(self, id):
        '''retrieve sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        return self._getRecordByID( SampleAssembly, id )
    
    def getScatteringKernels(self, where = None):
        '''retrieve all scattering kernels'''
        from vnf.dom.ScatteringKernel2 import ScatteringKernel2
        return self._getAll( ScatteringKernel2, where )

    def getInstrument(self, id):
        '''retrieve instrument of given id'''
        from vnf.dom.Instrument import Instrument
        return self._getRecordByID( Instrument, id )

    def getComponent(self, id):
        '''retrieve component of given id'''
        from vnf.dom.Component import Component
        return self._getRecordByID( Component, id )
    
    def getScatterer(self, id):
        '''retrieve scatterer of given id'''
        from vnf.dom.Scatterer import Scatterer
        return self._getRecordByID( Scatterer, id )
    
    def getScatterers(self, id):
        '''retrieve scatterers in the sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        from vnf.dom.Scatterer import Scatterer
        return self._getElements(
            id, SampleAssembly.Scatterers, Scatterer)

    def getComponents(self, id):
        '''retrieve components in the instrument of given id'''
        from vnf.dom.Instrument import Instrument
        referencetable = Instrument.Components
        
        records = self.db.fetchall(
            referencetable, where = "localkey='%s'" % id )

        from vnf.dom.Component import Component
        ret = []
        
        for record in records:
            componentID = record.remotekey
            componentrecord = self._getRecordByID( Component, componentID )
            componentrecord.label = record.label
            ret.append( componentrecord )
            continue

        return ret

    def getInstrumentGeometer(self, instrument):
        id = instrument.id
        from vnf.dom.Instrument import Instrument
        records = self.db.fetchall(
            Instrument.Geometer, where = 'container_id=%r' % id )
        geometer = {}
        for record in records:
            geometer[ record.element_label ] = record
            continue
        return geometer

    def getPolyXtalKernels(self, id):
        '''retrieve kernels in the scatterer of given id'''
        from vnf.dom.PolyXtalScatterer import PolyXtalScatterer
        from vnf.dom.ScatteringKernel import ScatteringKernel
        return self._getElements(
            id, PolyXtalScatterer.Kernels, ScatteringKernel)


    def getServer(self, id):
        '''retrieve server of given id'''
        from vnf.dom.Server import Server
        return self._getRecordByID( Server, id )
    
    def getServers(self, where = None):
        '''retrieve all servers'''
        from vnf.dom.Server import Server
        return self._getAll( Server, where )


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
        return self._getRealObject( id, Shape )


    def getRealScatteringKernel(self, id):
        from vnf.dom.ScatteringKernel import ScatteringKernel
        return self._getRealObject( id, ScatteringKernel)

    
    def getCrystal(self, id):
        '''retrieve crystal of given id'''
        from vnf.dom.Crystal import Crystal
        return self._getRecordByID( Crystal, id )


    def getPhononDispersion(self, id):
        from vnf.dom.PhononDispersion import PhononDispersion
        return self._getRecordByID( PhononDispersion, id )


    def getRealPhononDispersion(self, id):
        from vnf.dom.PhononDispersion import PhononDispersion
        return self._getRealObject( id, PhononDispersion )


    def getNeutronExperiment(self, id):
        from vnf.dom.NeutronExperiment import NeutronExperiment
        return self._getRecordByID( NeutronExperiment, id )


    def newJob(self, job):
        self.db.insertRow(job)
        return


    def _getElementIDs(self, id, referencetable):
        '''retrieve ids of elements in the container of the given id'''
        records = self.db.fetchall(
            referencetable, where = "localkey='%s'" % id )
        elementIDs = [
            record.remotekey for record in records]
        return elementIDs

    
    def _getElements(self, id, referencetable, elementtable):
        '''retrieve elements in the container of given id'''
        ids = self._getElementIDs( id, referencetable )
        records = [
            self._getRecordByID( elementtable, id )
            for id in ids]
        return records


    def _getRealObject(self, id, table):
        '''given id in a virtual table, retrieve the real
        object's record.
        A virtual table contains type and reference_id
        info of the real object.
        To look up the real object, we have to
        go to the table of the given object type
        and find the record of given id.
        '''
        record = self._getRecordByID( table, id )
        type = record.type
        id1 = record.reference
        exec "from vnf.dom.%s import %s as RealObj" % (type, type)
        obj = self._getRecordByID( RealObj, id1 )
        return obj


    def _index(self, table, where = None):
        index = {}
        all = self.db.fetchall(table, where=where)
        for item in all:
            index[item.id] = item
        return index
    
    def _getAll(self, table, where = None):
        index = {}
        all = self.db.fetchall(table, where=where)
        return all

    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        if len(all) == 1:
            return all[0]
        raise RuntimeError, "Cannot find record of id=%s in table %s" % (
            id, table.__name__)




class HierarchyRetriever:

    def __init__(self, clerk):
        self.clerk = clerk
        return
    

    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onNeutronExperiment(self, experiment):
        instrument_id = experiment.instrument_id
        instrument = self.clerk.getInstrument( instrument_id )
        instrument = self(instrument)
        experiment.instrument = instrument

        sampleassembly_id = experiment.sampleassembly_id
        if sampleassembly_id == '' or sampleassembly_id == 'None':
            experiment.sampleassembly = None
            return
        
        sampleassembly = self.clerk.getSampleAssembly( sampleassembly_id )
        sampleassembly = self(sampleassembly)
        experiment.sampleassembly = sampleassembly
        return experiment


    def onInstrument(self, instrument):
        components = self.clerk.getComponents( instrument.id )
        components = [ self( component ) for component in components ]
        instrument.components = components
        geometer = self.clerk.getInstrumentGeometer( instrument )
        instrument.geometer = geometer
        return instrument


    def onComponent(self, component):
        realcomponent = self.clerk.getRealComponent( component.id )
        component.realcomponent = self(realcomponent)
        return component


    def onMonochromaticSource(self, source):
        return source


    def onIQEMonitor(self, iqem):
        return iqem


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

        kernels = self.clerk.getPolyXtalKernels( scatterer.id )
        kernels = [ self(kernel) for kernel in kernels ]
        scatterer.kernels = kernels

        return scatterer


    def onScatteringKernel(self, kernel):
        realkernel = self.clerk.getRealScatteringKernel( kernel.id )
        kernel.realscatteringkernel = self(realkernel)
        return kernel
    

    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        dispersion_id = kernel.dispersion_id
        dispersion = self.clerk.getPhononDispersion( dispersion_id )
        dispersion = self(dispersion)
        kernel.dispersion = dispersion
        return kernel


    def onPhononDispersion(self, dispersion):
        realdispersion = self.clerk.getRealPhononDispersion( dispersion.id )
        dispersion.realdispersion = realdispersion
        return dispersion


    def onIDFPhononDispersion(self, dispersion):
        return dispersion


    def onCrystal(self, crystal):
        return crystal


    def onShape(self, shape):
        realshape = self.clerk.getRealShape( shape.id )
        shape.realshape = self(realshape)
        return shape


    def onBlock(self, block):
        return block

    pass # end of Clerk



def _tostr( value ):
    if isinstance( value, list ) or isinstance(value, tuple):
        ret =  '{%s}' % ','.join( [ str(item) for item in value ] )
        return ret
    return str(value)
        

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Fri Mar 14 22:18:28 2008

# End of file 

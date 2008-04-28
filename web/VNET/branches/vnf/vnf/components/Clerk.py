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
        return record


    def getRecordByID(self, tablename, id):
        exec 'from vnf.dom.%s import %s as Table' % (tablename, tablename) \
             in locals()
        return self._getRecordByID( Table, id )


    def findParentSampleAssembly(self, scatterer_id ):
        from vnf.dom.SampleAssembly import SampleAssembly
        table = SampleAssembly.Scatterers
        all = self.db.fetchall( table, where = "remotekey='%s'" % scatterer_id )
        if len(all) != 1:
            raise RuntimeError, "Every scatterer should have only one parent sample assembly"
        record = all[0]
        id = record.localkey
        return self.getSampleAssembly( id )
        

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

    def getUser(self, username):
        '''retrieve user of given username'''
        from vnf.dom.User import User
        all = self.db.fetchall( User, where = "username='%s'" % username )
        assert len(all) == 1
        return all[0]
        
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


    def getAbstractScatterer(self, impltablename, id ):
        '''obtain record in the abstract scatterer table given the
        implementation table and id'''
        
        from vnf.dom.Scatterer import Scatterer
        all = self.db.fetchall(
            Scatterer, where = "type='%s' and reference='%s'" % (
            impltablename, id) )
        assert len(all) == 1
        return all[0]


    def deleteScattererFromSampleAssembly(self, scatterer_id, sampleassembly_id ):
        # mark scatterer as deleted
        record = self.getScatterer( scatterer_id )
        assignments = [ ('status', 'd'), ]
        self.db.updateRow(
            record, assignments, where = "id='%s'" % scatterer_id)

        # detach scatterer from sampleassembly
        from vnf.dom.SampleAssembly import SampleAssembly
        table = SampleAssembly.Scatterers
        records = self.db.fetchall(
            table,
            where = "localkey='%s' and remotekey='%s'" % (
            sampleassembly_id, scatterer_id )
            )
        assert len(records) == 1
        reference = records[0]

        self.db.deleteRow(table, where="id='%s'" % reference.id)
        return


    def deleteRecord(self, record):
        table = record.__class__
        self.db.deleteRow( table, where="id='%s'" % record.id )
        return
    

    def newJob(self, job):
        self.db.insertRow(job)
        return


    def newReference(self, table, localkey, remotekey):
        '''create a new reference record.

        The new record will not be inserted to the db.
        So you have to do that some time in the future.
        '''
        record = table()
        id = new_id( self.director )
        record.id = id
        record.localkey = localkey
        record.remotekey = remotekey
        return record
    

    def new_ownedobject(self, table):
        '''create a new record for the given table.

        The given table is assumed to have following fields:
          - id
          - creator
          - date
        '''
        director = self.director
        
        record = table()
        
        id = new_id( director )
        record.id = id

        record.creator = director.sentry.username
        
        self.newRecord( record )
        return record


    def newRecord(self, record):
        'insert a new record into db'
        self.db.insertRow( record )
        return record


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


    def _init(self):
        Component._init(self)
        self.deepcopy = DeepCopier( self )
        return



class DeepCopier:

    def __init__(self, clerk):
        self.clerk = clerk
        self.director = clerk.director
        return


    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onInstrument(self, instrument):
        components = instrument.components
        component_copies = [ self( component ) for component in components ]
        from vnf.dom.Instrument import Instrument
        instrument_copy = self.clerk.new_ownedobject( Instrument )

        for prop in ['short_description', 'componentsequence', 'category']:
            setattr( instrument_copy, prop,
                     getattr( instrument, prop ) )
            continue
        
        from vnf.dom.Instrument import Instrument
        for component in component_copies:
            label = component.label
            ref = self.clerk.newReference(
                Instrument.Components,
                instrument_copy.id, component.id )
            ref.label = component.label
            self.clerk.newRecord( ref )
            continue
        
        instrument_copy.components = component_copies

        geometer = instrument.geometer
        #geometer is a dictionary of label: record
        geometer_copy = {}
        for name, record in geometer.iteritems():
            recordcopy = self.onInstrumentGeometer( record )
            recordcopy.container_id = instrument_copy.id
            self.clerk.updateRecord( recordcopy )
            geometer_copy[ name ] = recordcopy
            continue
        instrument_copy.geometer = geometer_copy

        self.clerk.updateRecord( instrument_copy )
        
        return instrument_copy


    def onInstrumentGeometer(self, record):
        from vnf.dom.Instrument import Instrument
        new = self.clerk.new_ownedobject( Instrument.Geometer )
        attrs = ['element_label', 'position', 'orientation', 'reference_label']
        for attr in attrs:
            setattr(new, attr, getattr(record, attr) )
            continue
        self.clerk.updateRecord( new )
        return new
    

    def onComponent(self, component):
        realcomponent = component.realcomponent
        realcomponent_copy = self(realcomponent)

        from vnf.dom.Component import Component
        component_copy = self.clerk.new_ownedobject( Component )
        component_copy.type = realcomponent.__class__.__name__
        component_copy.reference = realcomponent_copy.id
        self.clerk.updateRecord( component_copy )

        #remember my label in my instrument
        component_copy.label = component.label
        return component_copy


    def onMonochromaticSource(self, source):
        from vnf.dom.MonochromaticSource import MonochromaticSource
        copy = self.clerk.new_ownedobject( MonochromaticSource )
        copy.energy = source.energy
        self.clerk.updateRecord(copy)
        return copy


    def onIQEMonitor(self, iqem):
        from vnf.dom.IQEMonitor import IQEMonitor
        copy = self.clerk.new_ownedobject( IQEMonitor )
        attrs = [
            'Emin', 'Emax', 'nE',
            'Qmin', 'Qmax', 'nQ',
            'max_angle_in_plane', 'min_angle_in_plane',
            'max_angle_out_of_plane', 'min_angle_out_of_plane',
            'short_description',
            ]
        for attr in attrs:
            setattr( copy, attr, getattr( iqem, attr) )
            continue
        self.clerk.updateRecord(copy)
        return copy


    def onDetectorSystem_fromXML(self, record):
        from vnf.dom.DetectorSystem_fromXML import DetectorSystem_fromXML \
             as table
        copy = self.clerk.new_ownedobject( table )
        attrs = [
            'tofmin', 'tofmax', 'ntofbins',
            ]
        for attr in attrs:
            setattr( copy, attr, getattr( record, attr) )
            continue
        self.clerk.updateRecord(copy)
        return copy

    pass # end of DeepCopier


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


    def onDetectorSystem_fromXML(self, ds):
        return ds


    def onSampleAssembly(self, sampleassembly):
        scatterers = self.clerk.getScatterers( sampleassembly.id )
        scatterers = [ self( scatterer ) for scatterer in scatterers ]
        sampleassembly.scatterers = scatterers
        return sampleassembly


    def onScatterer(self, scatterer):
        try:
            realscatterer = self.clerk.getRealScatterer( scatterer.id )
        except Exception, error:
            import traceback
            self.clerk._debug.log(traceback.format_exc() )
            return scatterer
        scatterer.realscatterer = self(realscatterer)
        return scatterer
    
    
    def onPolyXtalScatterer(self, scatterer):
        shape_id = scatterer.shape_id
        shape = self.clerk.getShape( shape_id )
        shape = self(shape)
        scatterer.shape = shape
        
        crystal_id = scatterer.crystal_id
        try:
            crystal = self.clerk.getCrystal( crystal_id )
            crystal = self(crystal)
        except:
            crystal = None
            pass
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
        realdispersion = self(realdispersion)
        dispersion.realphonondispersion = realdispersion
        return dispersion


    def onIDFPhononDispersion(self, dispersion):
        return dispersion


    def onCrystal(self, crystal):
        return crystal


    def onShape(self, shape):
        try:
            realshape = self.clerk.getRealShape( shape.id )
        except Exception, error:
            import traceback
            self.clerk._debug.log(traceback.format_exc() )
            return shape
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


from misc import new_id

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Fri Mar 14 22:18:28 2008

# End of file 

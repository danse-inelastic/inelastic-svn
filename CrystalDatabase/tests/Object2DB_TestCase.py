#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest

class TestCase(unittest.TestCase):


    def test1(self):
        'simple object with just string'
        # create a simple data object type
        class Dummy:

            def __init__(self, a):
                self.a = a


        # add inventory
        from dsaw.model.Inventory import Inventory as base
        class Inventory(base):

            a = base.descriptors.str(name='a')

        Dummy.Inventory = Inventory
        

        # create a data object instance
        dummy = Dummy('hello')

        # convert dummy to a db record
        from dsaw.model.visitors.Object2DBRecord import Object2DBRecord
        o2r = Object2DBRecord()
        record = o2r(dummy)

        self.assertEqual(record.a, dummy.a)
        self.assertEqual(record.name, 'dummy')
        return
    
    
    def test1a(self):
        'str type: max_length'
        # create a simple data object type
        class Dummy:

            a = ''

        # add inventory
        from dsaw.model.Inventory import Inventory as base
        class Inventory(base):

            a = base.descriptors.str(name='a', max_length=99)

        Dummy.Inventory = Inventory
        
        # convert Dummy class to a db table
        from dsaw.model.visitors.Object2DBTable import Object2DBTable
        o2t = Object2DBTable()
        Table = o2t(Dummy)

        self.assertEqual(Table.a.length, Inventory.a.max_length)
        return
    
    
    def test2(self):
        'object with reference'

        from dsaw.model.Inventory import Inventory as InventoryBase
        
        # create data object types
        class Computation:

            def __init__(self, about):
                self.about = about
                return

            class Inventory(InventoryBase):

                about = InventoryBase.descriptors.str(name='about')

                
        class Job:

            def __init__(self, server, computation):
                self.server = server
                self.computation = computation

            class Inventory(InventoryBase):

                server = InventoryBase.descriptors.str(name='server')
                computation = InventoryBase.descriptors.reference(name='computation', targettype=Computation)
                

        # create data objects
        computation = Computation('what?')
        job = Job('a.b.c', computation)

        # convert to a db record
        from dsaw.model.visitors.Object2DBRecord import Object2DBRecord
        o2r = Object2DBRecord()
        record = o2r(job)

        self.assertEqual(job.server, record.server)
        self.assertEqual(record.name, 'job')
        print record.computation
        return
    
    
    def test3(self):
        'object for which Inventory is created on the fly'
        import dataobjects
        Computation = dataobjects.Computation
        Job = dataobjects.Job
        
        # create data objects
        computation = Computation('what?')
        job = Job('a.b.c', computation)

        # convert to a db record
        from dsaw.model.visitors.Object2DBRecord import Object2DBRecord
        o2r = Object2DBRecord()
        record = o2r(job)

        self.assertEqual(job.server, record.server)
        self.assertEqual(record.name, 'job')
        print record.computation
        return
    
    
    def test4(self):
        'referenceset'
        import dataobjects as do
        structure = do.Structure(do.Cylinder(r=3, h=10), [do.Atom(symbol='C')])

        # convert to a db record
        from dsaw.model.visitors.Object2DBRecord import Object2DBRecord
        o2r = Object2DBRecord()
        record = o2r(structure)

        self.assert_(o2r.registry.getRecord(structure.shape))
        return
    
    
    pass # end of TestCase


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 

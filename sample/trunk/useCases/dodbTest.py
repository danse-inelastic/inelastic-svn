from sample.SampleX import Sample

species='V'
VAlloy = Sample(species) 

# VAlloy gets db LOCATION of all available information, checking both local and global db's ***
# This includes but is not limited to crystal structure db's, all scattering data db's, any other pertinent 
#experimental data db's or files, calculated data db's, etc. ***

print VAlloy.getAvailableData()


#crystal structure
#atomic weight, atomic electronegativies, melting point...
#neutron scattering data, both raw and post-reduction
#simulated data
#others?
#***note the *type* of data is displayed rather than the data itself, which must be retreived first ***

print VAlloy.getCrystalStructures()

#assign scattering data

VAlloy.assignScatteringData()

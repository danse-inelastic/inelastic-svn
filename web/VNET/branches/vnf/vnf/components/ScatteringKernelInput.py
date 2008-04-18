#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, action, actionRequireAuthentication, AuthenticationError

from FormActor import FormActor as base

class ScatteringKernelInput(base):

    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of a scattering kernel"
        

    def default(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, err:
            return err.page
    
        formcomponent = self.retrieveFormToShow( 'selectkernel')
        formcomponent.director = director
        
        # build the SKChoice form
        SKChoice = document.form(name='scatteringKernelInput', action=director.cgihome)
        
        # specify action
        action = actionRequireAuthentication(          
            actor = 'scatteringKernelInput', 
            sentry = director.sentry,
            routine = 'onSelect',
            label = '',
            arguments = {'form-received': formcomponent.name },
            )
            
        from vnf.weaver import action_formfields
        action_formfields( action, SKChoice )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( SKChoice )
        
        submit = SKChoice.control(name='submit',type="submit", value="next")
    
        return page 
    
    
    def onSelect(self, director):
        selected = self.processFormInputs(director)
        method = getattr(self, selected )
        return method( director )


    def gulpHarmonic(self, director):
        from GulpHarmonic import GulpHarmonic
        gh=GulpHarmonic(director)
        return gh.getPage()
    
    def gulpNE(self, director):
        try:
            page = director.retrievePage( 'gulpNE' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        
        document = main.document(title="Newton's equations from Gulp")
        document.byline = '<a href="http://danse.us">DANSE</a>'
            
        # build the form
        form = document.form(name='gulpHarmonic', action=director.cgihome)
        
        p = form.paragraph()
        p.text = ['''<script src="/vnfBK/javascripts/SpryAssets/SpryAccordion.js" 
type="text/javascript"></script>

<script type="text/javascript">
<!--
var Accordion1 = new Spry.Widget.Accordion("themoEnsemble");
//-->
</script>''',
"<h1>Newton's equations from Gulp</h1>",
'<h2>Thermodynamic Ensemble</h2>',
'''<br />
  <br />
  </label>
  <div id="themoEnsemble" class="Accordion"
 tabindex="0">
  <div class="AccordionPanel">
  <div class="AccordionPanelTab"> <label> <input
 name="radio" id="nve" value="nve" type="radio" />Constant
Number, Volume, Energy Ensemble (NVE)</label>
  </div>
  <div class="AccordionPanelContent">
  <div class="AccordionPanelContent"> <label>Energy
(K) <input name="temp2" id="temp2" value="0"
 type="text" /> </label>
  <p>&nbsp;</p>
  </div>
  </div>
  </div>
  <div class="AccordionPanel">
  <div class="AccordionPanelTab"> <label> <input
 name="radio" id="nve2" value="nve" type="radio" />
Constant Number, Volume, Temperature Ensemble (NVT)</label> </div>
  <div class="AccordionPanelContent"> <label>Temperature
(K) <input name="temp" id="temp" value="0"
 type="text" /> </label>
  <p> <label>Thermostat Parameter <input name="temp4"
 id="temp4" value="0.05" type="text" /> </label>
  </p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  </div>
  </div>
  <div class="AccordionPanel">
  <div class="AccordionPanelTab"> <label> <input
 name="radio" id="radio" value="radio" type="radio" />
Constant Number, Pressure, Temperature</label> </div>
  <div class="AccordionPanelContent"> <label>Pressure
(atm) <input name="temp3" id="temp3" value="0"
 type="text" /> </label>
  <p> <label>Barostat Parameter <input name="temp7"
 id="temp7" value="0.05" type="text" /> </label>
  </p>
  <p> <label>Temperature (K) <input name="temp5"
 id="temp5" value="0" type="text" /> </label>
  </p>
  <p> <label>Thermostat Parameter <input name="temp6"
 id="temp6" value="0.005" type="text" /> </label>
  </p>
  </div>
  </div>
  </div>'''
]
        p = form.paragraph()
        p.text = ['<h2>Settings</h2>',
'''<p><label>Time Step (fs) <input name="timeStep"
 id="timeStep" value="1.0" type="text" /> </label>
  </p>
  <p> <label>Equilibrium Time (ps) <input
 name="equilibriumTime" id="equilibriumTime" value="0"
 type="text" /> </label>
  </p>
  <p> <label>Production Time (ps) <input
 name="equilibriumTime2" id="equilibriumTime2" value="1.0"
 type="text" /> </label>
  </p>
  <p> <label>Properties Calculation Frequency (fs) <input
 name="frequencyPropertyCalc" id="frequencyPropertyCalc"
 value="5.0" type="text" /> </label>
  </p>
  <p> <label>Trajectory Output Types
  <select name="trajectoryOutput" id="trajectoryOutput">
  <option>xyz and history</option>
  <option>xyz</option>
  <option>history</option>
  </select>
  </label></p>
  <p> <label>Save Progress Frequency (ps) <input
 name="restartFileOutputFrequency"
 id="restartFileOutputFrequency" value="0.25" type="text" />
  </label>
  ''']
        
        submit = form.control(name='submit',type="submit", value="next")
            
        return page        
#        from GulpNE import GulpNE
#        gh=GulpNE(director)
#        return gh.getPage()



    def __init__(self, name=None):
        if name is None:
            name = "scatteringKernelInput"
        super(ScatteringKernelInput, self).__init__(name)
        return
    
    
    def _head(self, director):
        page = director.retrieveSecurePage( 'scatteringKernelInput' )
        
        main = page._body._content._main

        # the record we are working on
        id = None # eventually get the id from idd
        
        document = main.document(title='Energetics / Dynamics Selection' )
        document.byline = '<a href="http://danse.us">DANSE</a>'

        return page, document


# version
__id__ = "$Id$"

# End of file 

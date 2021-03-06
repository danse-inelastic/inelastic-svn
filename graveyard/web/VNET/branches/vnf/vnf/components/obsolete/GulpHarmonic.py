#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, actionRequireAuthentication, AuthenticationError


class GulpHarmonic(Actor):


    def __init__(self, name=None):
        if name is None:
            name = "gulpHarmonic"
        super(GulpHarmonic, self).__init__(name)
    
    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'gulpHarmonic' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        
        document = main.document(title='Hamonic dynamics from Gulp' )
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



# version
__id__ = "$Id$"

# End of file 

<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!
! {LicenseText}
!
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-->


<!DOCTYPE inventory>

<inventory>

  <component name='main'>
    <property name='actor'>scatteringKernelInput</property>
    <property name='submit'>next</property>
    <component name='scatteringKernelInput'>
    	<property name='form-recieved'>selectkernel</property>
        <component name='selectkernel'>
    	     <property name='kernel'>gulpNE</property>
        </component> 
    </component>    
    <property name='routine'>onSelect</property>   
    <component name='sentry'>
    	<property name='username'>demo</property>
    	<property name='passwd'>demo</property>
    </component>
  </component>
</inventory>


<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by XMLMill on Fri Apr  4 10:17:11 2008-->

<!-- End of file -->

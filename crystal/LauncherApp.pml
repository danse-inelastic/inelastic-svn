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

    <component name="LauncherApp">
        <property name="typos">strict</property>
        <property name="help-persistence">False</property>
        <property name="help">False</property>
        <property name="launcher">serial_launcher</property>
        <property name="help-properties">False</property>
        <property name="help-components">False</property>

        <component name="serial_launcher">
            <property name="help-persistence">False</property>
            <property name="remote">False</property>
            <property name="help">False</property>
            <property name="dry_run">False</property>
            <property name="search_path">True</property>
            <property name="errlogfile"></property>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
            <property name="env">None</property>
            <property name="rsh">rsh -. </property>
            <property name="logfile">run.log</property>
            <property name="remote_server"></property>
        </component>


        <component name="weaver">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="copyright"></property>
            <property name="creator"></property>
            <property name="timestamp">True</property>
            <property name="author"></property>
            <property name="bannerCharacter">~</property>
            <property name="help-properties">False</property>
            <property name="versionId"> $Id$</property>
            <property name="timestampLine"> Generated automatically by %s on %s</property>
            <property name="help-components">False</property>
            <property name="lastLine"> End of file </property>
            <property name="licenseText">['{LicenseText}']</property>
            <property name="copyrightLine">(C) %s  All Rights Reserved</property>
            <property name="organization"></property>
            <property name="bannerWidth">78</property>
        </component>

    </component>

</inventory>

<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by Renderer on Mon Dec  1 15:09:14 2008-->

<!-- End of file -->

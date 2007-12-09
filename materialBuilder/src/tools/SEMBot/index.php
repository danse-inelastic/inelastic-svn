<?php

require_once("util.inc");

page_head("");

?>
<body>
<table class="navbar" border="0" width="100%" cellpadding="0"
       bgcolor="#a0c0ff" cellspacing="0">

  <tr valign="middle">
      <th bgcolor="#70b0f0" class="navbar-select"
          >&nbsp;&nbsp;&nbsp;Home&nbsp;&nbsp;&nbsp;</th>

      <th nowrap>&nbsp;&nbsp;&nbsp;<a
        href="NE1_Documentation">NE1 API Docs</a>&nbsp;&nbsp;&nbsp;</th>

      <th>&nbsp;&nbsp;&nbsp;<a
        href="#">QA</a>&nbsp;&nbsp;&nbsp;</th>

      <th>&nbsp;&nbsp;&nbsp;<a
        href="#">Builds</a>&nbsp;&nbsp;&nbsp;</th>

      <th class="navbar" align="right" width="100%">
        <table border="0" cellpadding="0" cellspacing="0">
          <tr><th class="navbar" align="center">materialBuilder Software-Engineering Mechanisms Robot (SEMBot)&nbsp;&nbsp;&nbsp;<a href="http://www.nanoengineer-1.net/" target="_top">NE1 Wiki</a>&nbsp;&nbsp;&nbsp;</th>
          </tr></table></th>
  </tr>
</table>

<p>
<img align="right" src="Engineer-X-Man-Logo.png">
Welcome to the materialBuilder Software-Engineering Mechanisms Robot (SEMBot).
<p>
SEMBot files are checked in under /cad/src/tools/SEMBot/ and are updated before each run.
<table class="summary" border="1" cellpadding="3"
       cellspacing="0" width="500" bgcolor="white">
  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">Log</span></td>
    <td class="summary">
      <span class="summary-name"><a href="http://www.nanohive-1.org/Engineering/SEMBot.log">SEMBot.log</a></span></td>
  </tr>
</table>
<pre>

</pre>

<a name="epydoc"></a>
<table class="summary" border="1" cellpadding="3"
       cellspacing="0" width="500" bgcolor="white">
  <tr bgcolor="#70b0f0" class="table-header">
    <td colspan="2" class="table-header">
    <span class="table-header">Epydoc API Documentation Generation</span></td>
  </tr>

  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">Summary</span></td>
    <td class="summary">This mechanism updates a local copy of the NE1 codebase, then runs <a href="http://epydoc.sourceforge.net/">Epydoc</a> on it to generate formatted <a href="NE1_Documentation">NE1 API documentation</a>.</td>
  </tr>

  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">Last run</span></td>
    <td class="summary">
      <span class="summary-name"><?php include 'NE1_Docs.timestamp'; ?></span> (Updated every night.)</td>
  </tr>

  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">Last result</span></td>
    <td class="summary">
      <span class="summary-name"><?php include 'NE1_Docs.result'; ?></span></td>
  </tr>

  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">Log</span></td>
    <td class="summary">
      <span class="summary-name"><a href="http://www.nanohive-1.org/Engineering/NE1_Docs.log">NE1_Docs.log</a></span></td>
  </tr>

<!--
  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">
        <input type="submit" value="Re-Generate"></span></td>
    <td class="summary">
      This will re-run Epydoc to re-generate the API documentation. (Password required.)
  </tr>
-->

  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">Notes</span></td>
    <td class="summary">
      The Epydoc configuration file is checked in as /cad/src/epydoc.config and is updated before each Epydoc run.
      <p>
      To add images to your Epydoc documentation, use the following format: <tt>IMAGE(<i>URL</i>)</tt> which gets transcribed as <tt>&lt;img src="<i>URL</i>"&gt;</tt>
      <p>
      Epydoc chokes on <tt>__author__ = ['Mark', 'Bruce']</tt> so please use <tt>__author__ = "Mark, Bruce"</tt> instead.</td>
  </tr>
</table>

<p>

<a name="qa"></a>
<table class="summary" border="1" cellpadding="3"
       cellspacing="0" width="500" bgcolor="white">
  <tr bgcolor="#70b0f0" class="table-header">
    <td colspan="2" class="table-header">
    <span class="table-header">QA</span></td>
  </tr>

  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">Summary</span></td>
    <td class="summary">pyUnit, pyChecker, etc.</td>
  </tr>
</table>

<p>

<a name="builds"></a>
<table class="summary" border="1" cellpadding="3"
       cellspacing="0" width="500" bgcolor="white">
  <tr bgcolor="#70b0f0" class="table-header">
    <td colspan="2" class="table-header">
    <span class="table-header">Builds</span></td>
  </tr>

  <tr>
    <td width="15%" align="right" valign="top" class="summary">
      <span class="summary-type">Summary</span></td>
    <td class="summary">Nightly builds, etc.</td>
  </tr>
</table>

</body>
</html>

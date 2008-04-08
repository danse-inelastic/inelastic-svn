<?xml version="1.0" encoding="ISO-8859-1"?>
<!--####################################################################
 |  $Id: db2latex-mw-itemizedlist.xsl,v 1.1 2004/01/18 12:19:59 miwie Exp $
 |  $Author: miwie $
 + ################################################################# -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:doc="http://nwalsh.com/xsl/documentation/1.0"
                exclude-result-prefixes="doc" version="1.0">

  <!-- DOCUMENTATION                                                   -->
  <doc:reference id="itemizedlists" xmlns="">
    <referenceinfo>
      <releaseinfo role="meta">
	$Id: db2latex-mw-itemizedlist.xsl,v 1.1 2004/01/18 12:19:59 miwie Exp $
      </releaseinfo>
      <authorgroup>
	<author><firstname>Michael</firstname> <surname>Wiedmann</surname></author>
      </authorgroup>
      <copyright>
	<year>2004</year>
	<holder>Michael Wiedmann</holder>
      </copyright>
    </referenceinfo>

    <title>Lists <filename>db2latex-mw-itemizedlist.xsl</filename></title>
    <partintro>
      <section>
	<title>Introduction</title>
	<para>Especially for itemizedlist which contain only short lines
	  of text LaTeX's default vertical space between items is IMHO
	  too excessive. <filename>mdwlist.sty</filename> provides 
	  "compacted itemize environments" with less vertical space 
	  between items.
	</para>
	<para>
	  If the "spacing" attribute of the "itemizedlist" element
	  contains "db2latex:compact" we use these modified itemize 
	  environments instead of the standard LaTeX ones.
	</para>
	<para>Ensure that "\usepackage{mdwlist}" is output
	  somewhere in your stylesheets.
	</para>
      </section>
    </partintro>
  </doc:reference>

  <xsl:output method="text" encoding="ISO-8859-1" indent="yes"/>

  <xsl:template match="itemizedlist">
    <xsl:if test="title"><xsl:apply-templates select="title"/></xsl:if>
    <xsl:choose>
      <xsl:when test="@spacing='db2latex:compact'">
        <xsl:text>&#10;\begin{itemize*}</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#10;\begin{itemize}</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="listitem"/>
    <xsl:choose>
      <xsl:when test="@spacing='db2latex:compact'">
        <xsl:text>&#10;\end{itemize*}</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#10;\end{itemize}</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>

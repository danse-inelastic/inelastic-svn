<?xml version="1.0" encoding="ISO-8859-1"?>
<!--####################################################################
 |  $Id: db2latex-mw-variablelist.xsl,v 1.1 2004/01/18 12:19:59 miwie Exp $
 |  $Author: miwie $
 + ################################################################# -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:doc="http://nwalsh.com/xsl/documentation/1.0"
                exclude-result-prefixes="doc" version="1.0">

  <!-- DOCUMENTATION                                                   -->
  <doc:reference id="variablelists" xmlns="">
    <referenceinfo>
      <releaseinfo role="meta">
	$Id: db2latex-mw-variablelist.xsl,v 1.1 2004/01/18 12:19:59 miwie Exp $
      </releaseinfo>
      <authorgroup>
	<author><firstname>Michael</firstname> <surname>Wiedmann</surname></author>
      </authorgroup>
      <copyright>
	<year>2004</year>
	<holder>Michael Wiedmann</holder>
      </copyright>
    </referenceinfo>

    <title>Lists <filename>db2latex-mw-variablelist.xsl</filename></title>
    <partintro>
      <section>
	<title>Introduction</title>
	<para>This customization of "variablelist" depends on the usage
	  of one of KOMA document classes (scrbook, scrartcl, etc.). 
	  You have to ensure that your stylesheets outputs a
          corresponding line, like "\documentclass{scrXXXX}".
	</para>
        <itemizedlist>
	  <listitem>
	    <simpara>If the attribute 'role' contains 
	      'db2latex:multiterm' we use a 'parbox' for every 
	      'item'. Otherwise the item's could be too long to 
	      fit on one line. 
	      Use this if your list contains many 'term's.
	    </simpara>
	  </listitem>
	  <listitem>
	    <simpara>If the attribute 'role' contains 
	      'db2latex:nonoindent' we don't output '\noindent' 
	      before the environment.
	    </simpara>
	  </listitem>
	  <listitem>
	    <simpara>If the 'role' attribute contains 
	      'db2latex:labeling' as value we use KOMA's 
	      'labeling' environment.
	    </simpara>
	  </listitem>
	  <listitem>
	    <simpara>If the attribute 'termlength' is 
	      non-empty we use this numeric value as a hint 
	      for 'labeling' for the width of the 'item's 
	      (defaults to 5).
	    </simpara>
	  </listitem>
	</itemizedlist>
      </section>
    </partintro>
  </doc:reference>

  <xsl:output method="text" encoding="ISO-8859-1" indent="yes"/>

  <xsl:template match="variablelist">
    <xsl:variable name="helpstring">123456789012345</xsl:variable>
    <xsl:if test="title"> 
      <xsl:apply-templates select="title"/>
    </xsl:if>
    <xsl:text>&#10;</xsl:text> 
    <xsl:choose>
      <xsl:when test="contains(@role,'db2latex:nonoindent')">
	<!-- noop -->
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>\noindent&#10;</xsl:text> 
      </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test="contains(@role,'db2latex:labeling')">
	<xsl:text>\begin{labeling}{</xsl:text>
	<xsl:choose>
	  <xsl:when test="@termlength!=''">
	    <xsl:value-of select="substring($helpstring,1,number(@termlength))"/>
	  </xsl:when>
	  <xsl:otherwise>
	    <xsl:text>12345</xsl:text>
	  </xsl:otherwise>
	</xsl:choose>
	<xsl:text>}&#10;</xsl:text> 
	<xsl:apply-templates select="varlistentry"/>
	<xsl:text>\end{labeling}&#10;</xsl:text> 
      </xsl:when>
      <xsl:when test="contains(@role,'db2latex:compact')">
        <xsl:text>\begin{description*}</xsl:text>
	<xsl:apply-templates select="varlistentry"/>
	<xsl:text>\end{description*}&#10;</xsl:text> 
      </xsl:when>
      <xsl:when test="contains(@role,'db2latex:multiterm')">
        <xsl:text>\begin{description}</xsl:text>
	<xsl:apply-templates select="varlistentry">
          <xsl:with-param name="multiterm" select="1"/>
        </xsl:apply-templates>
	<xsl:text>\end{description}&#10;</xsl:text> 
      </xsl:when>
      <xsl:otherwise>
	<xsl:text>\begin{description}&#10;</xsl:text> 
	<xsl:apply-templates select="varlistentry"/>
	<xsl:text>\end{description}&#10;</xsl:text> 
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="varlistentry">
    <xsl:param name="multiterm" select="0"/>
    <xsl:variable name="id"> 
      <xsl:call-template name="label.id"/>
    </xsl:variable>
    <xsl:text>% \null is a trick&#10;</xsl:text>
    <!-- changed MW, 040105 -->
    <xsl:choose>
      <xsl:when test="$multiterm > 0">
	<!-- FIXME: let user specify the width of the parbox -->
        <xsl:text>\item[{\parbox[b]{0.5\linewidth}{</xsl:text>
        <xsl:for-each select="term">
          <xsl:apply-templates/>
          <xsl:if test="position()!=last()">
            <xsl:text>, </xsl:text>
          </xsl:if>
        </xsl:for-each>
        <xsl:text>}}]\null{}</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>\item[{</xsl:text>
        <xsl:for-each select="term">
          <xsl:apply-templates/>
          <xsl:if test="position()!=last()">
            <xsl:text>, </xsl:text>
          </xsl:if>
        </xsl:for-each>
        <xsl:text>}]\null{}</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="listitem"/>
  </xsl:template>

</xsl:stylesheet>

<?xml version='1.0'?>
<!--############################################################################
|	$Id: db2latex-mw-revhistory.xsl,v 1.1 2004/01/26 10:56:02 j-devenish Exp $
+ ############################################################################## -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version='1.0'>

  <!-- use a more pleasant (IMHO) table layout for the 'revhistory' -->
  <xsl:template match="revhistory/revision">
    <xsl:variable name="revnumber" select=".//revnumber"/>
    <xsl:variable name="revdate"   select=".//date"/>
    <xsl:variable name="revauthor" select=".//authorinitials"/>
    <xsl:variable name="revremark" select=".//revremark|.//revdescription"/>

    <xsl:if test="$revnumber">
      <xsl:call-template name="gentext.element.name"/>
      <xsl:text> </xsl:text>
      <xsl:apply-templates select="$revnumber"/>
    </xsl:if>
    <xsl:text> &amp; </xsl:text>
    <xsl:apply-templates select="$revdate"/>
    <xsl:text> &amp; </xsl:text>
    <xsl:choose>
      <xsl:when test="count($revauthor)=0">
        <xsl:call-template name="dingbat">
          <xsl:with-param name="dingbat">nbsp</xsl:with-param>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="$revauthor"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text> \\&#10;</xsl:text>
    <xsl:if test="$revremark"> 
      <!-- we can't simply use "X" as column format -->
      <xsl:text>\multicolumn{3}{@{}p{\linewidth}@{}}{</xsl:text>
      <xsl:apply-templates select="$revremark"/> 
      <xsl:text>} \\ [1em]&#10;</xsl:text>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>

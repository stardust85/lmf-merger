<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        </head>
    <body>
    <xsl:for-each select="LexicalResource/Lexicon/LexicalEntry">
        <p>
            <b><xsl:value-of select="Lemma/feat[@att='writtenForm']/@val"/></b> /<xsl:value-of select="Lemma/feat[@att='phoneticForm']/@val"/>/<br/>
          <ol>
            <xsl:for-each select="Sense">
              <li>
                  <ul>
                   <xsl:for-each select="Equivalent">
                      <li>
                          <xsl:value-of select="feat[@att='writtenForm']/@val"/>
                      </li>
                   </xsl:for-each>
                  </ul>
              </li>
            </xsl:for-each>
          </ol>
        </p>
    </xsl:for-each>
    </body>
    </html>
</xsl:template>

</xsl:stylesheet>

# fred-OpenAPI-Specification

**OpenAPI specification for the Federal Reserve Economic Data (FRED) API (JSON and YAML)**



**FRED API Summary**

The Federal Reserve Bank of St. Louis' Economic Research Division offers enhanced economic data services through the FRED API. This API enables programmatic access to the Federal Reserve Economic Data (FRED)


**Data Retrieval**

Users can query specific economic data by specifying source, release, category, and series among other preferences.


**Compatibility**

Supports any programming language capable of parsing XML or JSON. Communication with servers is facilitated via HTTPS, based on the REST web service architecture.


**Service Features**

Uses HTTPS for secure data requests and responses.
Utilizes URLs for specifying data requests.
Delivers data in XML or JSON formats, offering structured, flexible data handling compared to HTML's visual and less strictly formatted structure.



**FRED API API Endpoints**


**Categories**

fred/category - Get a category.

fred/category/children - Get the child categories for a specified parent category.

fred/category/related - Get the related categories for a category.

fred/category/series - Get the series in a category.

fred/category/tags - Get the tags for a category.

fred/category/related_tags - Get the related tags for a category.



**Releases**

fred/releases - Get all releases of economic data.

fred/releases/dates - Get release dates for all releases of economic data.

fred/release - Get a release of economic data.

fred/release/dates - Get release dates for a release of economic data.

fred/release/series - Get the series on a release of economic data.

fred/release/sources - Get the sources for a release of economic data.

fred/release/tags - Get the tags for a release.

fred/release/related_tags - Get the related tags for a release.

fred/release/tables - Get the release tables for a given release.


**Series**

fred/series - Get an economic data series.

fred/series/categories - Get the categories for an economic data series.

fred/series/observations - Get the observations or data values for an economic data series.

fred/series/release - Get the release for an economic data series.

fred/series/search - Get economic data series that match keywords.

fred/series/search/tags - Get the tags for a series search.

fred/series/search/related_tags - Get the related tags for a series search.

fred/series/tags - Get the tags for an economic data series.

fred/series/updates - Get economic data series sorted by when observations were updated on the FRED®
server.
fred/series/vintagedates - Get the dates in history when a series' data values were revised or new data values were released.



**Sources**

fred/sources - Get all sources of economic data.

fred/source - Get a source of economic data.

fred/source/releases - Get the releases for a source.



**Tags**

fred/tags - Get all tags, search for tags, or get tags by name.

fred/related_tags - Get the related tags for one or more tags.

fred/tags/series - Get the series matching tags.




For geting **API Kye** visit https://fredaccount.stlouisfed.org/apikeys

Fore more info visit https://research.stlouisfed.org/

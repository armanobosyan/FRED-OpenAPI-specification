# fred-OpenAPI-specification
YAML OpenAPI specification for the Federal Reserve Economic Data (FRED) API

# About
This OpenAPI specification serves as a contract for developers, detailing how to programmatically access economic data from the Federal Reserve Economic Data (FRED) API database.

It covers operations for querying categories, their hierarchies, related tags, and detailed series data within categories or releases. By following this specification, developers can integrate FRED's rich economic datasets into their applications, enabling analysis, visualization, and dissemination of economic indicators and trends.

This YAML snippet is an OpenAPI (formerly known as Swagger) specification for the Federal Reserve Economic Data (FRED) API. It outlines how to interact with the API, detailing available endpoints, their operations, parameters, and expected responses. 
Here's a breakdown of its components and their functionalities:

# Overview
openapi: 3.0.0: Specifies the OpenAPI Specification version used.
info: Provides metadata about the API such as its title, description, and version.
servers: Lists the base URL(s) for the API endpoints.
Paths and Operations
Defines the available paths (endpoints) and operations (HTTP methods) that can be used to interact with the API.

## /category
get: Fetches a specific category by its ID.
parameters: Include api_key, file_type, and category_id.
responses: Returns details of the specified category.

## /category/children
get: Retrieves child categories for a given parent category ID.
parameters: Similar to /category, with additional parameters for time filtering (realtime_start, realtime_end).
responses: Lists child categories of the specified parent category.

## /category/related
get: Fetches categories related to a specified category.
parameters: Includes api_key, file_type, category_id, and time filtering options.
responses: Provides related categories.

## /category/series
get: Retrieves series within a specified category.
parameters: Extends the common parameters with options to limit, offset, order, and filter the results.
responses: Returns series data within the category.

## /category/tags
get: Fetches tags associated with a specific category.
parameters: Standard parameters with options for pagination and ordering.
responses: Lists tags for the category.

## /category/related_tags
get: Retrieves tags related to specific tags within a category.
parameters: Includes tag_names to specify which tags to find relations for.
responses: Provides related tags based on the specified tags.

## /releases and Subpaths
get: Various operations related to economic data releases, including fetching all releases, release dates, series within a release, sources, tags, related tags, tables, etc.
parameters: Common parameters are used across these endpoints, with specific ones like release_id, tag_names, and element_id tailored to each operation's needs.
responses: Depending on the endpoint, responses include lists of releases, series, tags, tables, and more, often with options to filter, sort, and paginate results.

Additianl path will be added...




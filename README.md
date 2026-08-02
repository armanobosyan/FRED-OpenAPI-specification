# FRED OpenAPI Specification

[![Validate spec](https://github.com/armanobosyan/FRED-OpenAPI-specification/actions/workflows/validate-spec.yml/badge.svg)](https://github.com/armanobosyan/FRED-OpenAPI-specification/actions/workflows/validate-spec.yml)

An OpenAPI 3.0 description of the [Federal Reserve Economic Data (FRED)
API](https://fred.stlouisfed.org/docs/api/fred/), in YAML and JSON, covering
all 35 endpoints including the GeoFRED map endpoints.

FRED publishes its API as HTML documentation only. This repository turns that
into a machine-readable contract you can load into Postman, Insomnia, Swagger
UI, an OpenAPI code generator or an LLM tool definition.

## Files

| File | Purpose |
| --- | --- |
| `fred-schema.yaml` | the specification — **edit this one** |
| `fred-schema.json` | generated from the YAML by `sync-spec.py` |
| `sync-spec.py` | validates the YAML and regenerates the JSON |
| `fred-ID-parentID-Names.csv` | every FRED category as `id,name,parent_id` |
| `requirements.txt` | what `sync-spec.py` needs |

## Using it

Point your tool at either file; they describe the same API. Requests need a
free API key from <https://fredaccount.stlouisfed.org/apikeys>.

The key is modelled as an `apiKey` security scheme rather than as a query
parameter on each operation:

```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: query
      name: api_key
```

Most tools will prompt for it once and append `?api_key=...` to every request.

Responses are XML unless you pass `file_type=json`. Response bodies are not
modelled field by field — operations declare a JSON object or an XML string,
and the documented `400` error shape (`error_code`, `error_message`).

Parameters carry their documented constraints, so a generated client or tool
definition is usable without the docs open alongside it. Enumerated values are
spelled out rather than left as codes, and 141 parameters carry an example,
mostly the values FRED uses in its own documentation:

```yaml
- name: units
  in: query
  description: A key that indicates a data value transformation. Values: lin = Levels
    (No transformation); chg = Change; ch1 = Change from Year Ago; pch = Percent Change;
    pc1 = Percent Change from Year Ago; pca = Compounded Annual Rate of Change; ...
  schema:
    type: string
    enum: [lin, chg, ch1, pch, pc1, pca, cch, cca, log]
    default: lin
```

## Endpoints

| Group | Endpoints |
| --- | --- |
| Categories | `category`, `category/children`, `category/related`, `category/series`, `category/tags`, `category/related_tags` |
| Releases | `releases`, `releases/dates`, `release`, `release/dates`, `release/series`, `release/sources`, `release/tags`, `release/related_tags`, `release/tables` |
| Series | `series`, `series/categories`, `series/observations`, `series/release`, `series/search`, `series/search/tags`, `series/search/related_tags`, `series/tags`, `series/updates`, `series/vintagedates` |
| Sources | `sources`, `source`, `source/releases` |
| Tags | `tags`, `related_tags`, `tags/series` |
| Maps | `geofred/shapes/file`, `geofred/series/group`, `geofred/series/data`, `geofred/regional/data` |

The map endpoints live under `/geofred/`, not `/fred/maps/`.

## Editing

`fred-schema.yaml` is the source of truth. After changing it:

```sh
pip install -r requirements.txt
python sync-spec.py
```

That validates the document against the OpenAPI 3.0 schema, checks that every
`operationId` is unique, and rewrites `fred-schema.json`.

The same script runs as `python sync-spec.py --check` on every push and pull
request (`.github/workflows/validate-spec.yml`) and fails the build on invalid
YAML, an invalid or duplicate-id document, or a `fred-schema.json` that no
longer matches the YAML. The two files drifting apart is the failure mode this
repository is most prone to: an API key was once removed from the JSON copy and
left behind in the YAML.

## Two places the spec differs from FRED's documentation

Both were confirmed against the live API, which is stricter than the docs:

- `geofred/shapes/file` — `shape` is documented without a required marker, but
  the API answers `Bad Request. Shape variable must be set.` without it.
- `geofred/regional/data` — `frequency` is documented as an optional value
  list, but the API answers `Bad Request. Must have frequency set.` without it.

Both are marked `required: true` here.

## Category list

`fred-ID-parentID-Names.csv` holds every FRED category with its parent, sorted
by `parent_id` then `id`:

```csv
id,name,parent_id
1,Production & Business Activity,0
10,"Population, Employment, & Labor Markets",0
```

FRED has no endpoint that returns the category tree in one call, so this file
is assembled by walking `fred/category/children` from the root. Regenerate it
with [FRED-API-ID-Fetcher](https://github.com/armanobosyan/FRED-API-ID-Fetcher),
which also fetches the metadata of every series filed under those categories —
title, frequency, units, seasonality and coverage — which FRED likewise offers
no endpoint to list.

## Version 2.0.0

The specification was rebuilt from FRED's documentation. Changes that affect
generated clients:

- `operationId`s are now derived from the path and unique
  (`getCategoryChildren`, `getGeoFredRegionalData`). Version 1.0.2 mixed
  `getCategory` with `GetSeriesObservations` and used `getReleaseDates` for two
  different endpoints.
- `api_key` moved from a per-operation parameter to the security scheme above.
- The four `geofred` endpoints were added.
- Every operation now declares `responses`; 16 of 31 previously had none, which
  made the document invalid OpenAPI.
- A scraping artefact that appeared as a query parameter named `Description`
  on 14 operations, and similar `The` and `Description:` parameters, were
  removed.
- Parameter names, types, defaults, allowed values and required flags were
  regenerated from the documentation; `include_observations` on
  `release/tables` is now `include_observation_values`, and
  `releases/dates` gained `order_by`, `sort_order` and
  `include_release_dates_with_no_data`.
- Every parameter now has a description, 141 have an example, and the meaning
  of each enumerated value is spelled out. Operations are grouped under tags,
  and the document declares `externalDocs` pointing back at FRED.

## License

MIT — see [LICENSE](LICENSE).

# Changelog

## [Unreleased] - TBD

## [0.3.0] - 2026-03-01

**Added**

- Python 3.13 and 3.14 support
- v3 `requestBody` generation with `application/json`, `multipart/form-data`, and `application/x-www-form-urlencoded` content types
- v3 parameter `style` (`form`, `simple`, `label`, `matrix`, `spaceDelimited`, `pipeDelimited`, `deepObject`)
- v3 richer parameter schemas: string, array, and object
- v3 operation `security` and `deprecated`
- v3 `securitySchemes` in `components`
- v2 `securityDefinitions` with apiKey schemes
- v2 operation `security` and `deprecated`
- v2 `collectionFormat` for array query and form-data parameters
- v2 `items` injection for array-typed parameters

## [0.2.1] - 2024-07-10

**Fixed**

- Value for the `openapi` field.
- Non-uniqueness in generated parameter.
- Missing referenced values for Open API 3.0.

## [0.2.0] - 2024-07-10

**Added**

- Generating response references inside operations in Open API 2.0
- Generating basic Open API 3.0 documents

**Fixed**

- Allow generating parameters with the same name but different locations

## [0.1.0] - 2024-05-15

- Initial public release

[Unreleased]: https://github.com/Stranger6667/hypothesis-openapi/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/Stranger6667/hypothesis-openapi/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/Stranger6667/hypothesis-openapi/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/Stranger6667/hypothesis-openapi/compare/v0.1.0...v0.2.0

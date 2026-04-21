---
name: api-docs-generator
description: Reads API routes and generates OpenAPI 3.0 documentation with request/response examples, error codes, authentication requirements, and schema definitions. Use when an API exists but has no docs, when onboarding external consumers, or before publishing a public API surface.
---

# API Documentation Generator

Read existing API routes and produce complete, accurate OpenAPI 3.0 documentation. The output should be good enough to drop into Swagger UI or Redoc with no edits.

## Hard Rules

- Document what the code DOES, not what it should do. Read the implementation, not just the route signatures.
- Never invent error codes or response shapes. If you can't confirm it from the code, mark it as `# TODO: verify`.
- Auth requirements must come from middleware/decorators in the code — not assumed.

## Process

### 1. Discover Routes

Scan the codebase for all API route definitions. Common patterns by framework:

- **Flask**: `@app.route`, `@blueprint.route`, `add_url_rule`
- **FastAPI**: `@app.get`, `@app.post`, `@router.{method}`
- **Express**: `app.get`, `app.post`, `router.{method}`
- **Django**: `urlpatterns`, `path()`, `re_path()`

List every route found: method, path, handler function name.

### 2. Read Each Handler

For each route, read the handler function and extract:

- **Request**: path params, query params, request body shape, required vs optional fields, data types
- **Response**: all return paths (success AND error), status codes, response body shapes
- **Auth**: any auth decorators, middleware, token checks, session requirements
- **Side effects**: DB writes, external API calls, file operations (relevant for docs consumers)

Do NOT skim. Read every branch of the handler — the error paths are what external consumers hit most.

### 3. Infer Schemas

Build JSON Schema definitions for all request bodies and response objects:

- Use `$ref` to `#/components/schemas/` for any type used more than once
- Mark fields `required` only if the code enforces it (validation, null checks)
- Use `example` values pulled from the code (test fixtures, seed data, inline defaults)
- If a field's type is ambiguous, use `oneOf` or note it with a comment

### 4. Document Auth

Identify the auth pattern and document it in `components/securitySchemes`:

- **API key**: header name, query param name, or cookie name
- **Bearer token**: JWT or opaque — note where it's validated
- **Session cookie**: cookie name and scope
- **No auth**: mark explicitly so consumers know it's intentional

Apply `security` blocks to each operation that requires it.

### 5. Write the OpenAPI Document

Produce a valid OpenAPI 3.0.3 YAML document:

```yaml
openapi: 3.0.3
info:
  title: <inferred from project name>
  version: <from package.json / pyproject.toml / setup.py, or "1.0.0">
  description: <1-2 sentence summary of what this API does>

servers:
  - url: http://localhost:<port>
    description: Local development
  # Add staging/prod if base URLs are found in config

paths:
  /example/{id}:
    get:
      summary: <short imperative phrase, e.g. "Get location by ID">
      description: <longer description if behavior is non-obvious>
      operationId: getLocationById
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          example: "loc_abc123"
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Location"
              example:
                id: "loc_abc123"
                name: "Grand Canyon South Rim"
        "404":
          description: Location not found
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
      security:
        - BearerAuth: []

components:
  schemas:
    Error:
      type: object
      required: [error]
      properties:
        error:
          type: string
          example: "Not found"
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
```

### 6. Output and Placement

Write the document to `docs/openapi.yaml` (or `openapi.yaml` at the project root if no `docs/` dir exists).

Also write a brief `docs/API.md` index:
- Link to the OpenAPI file
- Note how to run Swagger UI locally: `npx @redocly/cli preview-docs docs/openapi.yaml`
- List any auth requirements at a glance
- Call out any `# TODO: verify` items that need human review

### 7. Validate

Run a quick self-check before presenting:

- [ ] Every route in the codebase has a corresponding path entry
- [ ] Every response branch (success + error) is documented
- [ ] No invented fields — everything traceable to the code
- [ ] Auth correctly applied (routes with auth checks have `security`, routes without don't)
- [ ] All `$ref` targets exist in `components/schemas`
- [ ] Examples are realistic, not `"string"` or `0` placeholders

Report the self-check result and flag any `# TODO: verify` items for the user to confirm.

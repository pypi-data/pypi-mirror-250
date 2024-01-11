# Beef: Generate methods for calling REST APIs using type hints

Beef is a Python metaprogramming library which eliminates need for boilerplate code when integrating with REST APIs.
The library provides a powerful class descriptor which generates code for calling a REST API based on method signatures
annotated with type hints. The library takes care of building urls, deserialization of Pydantic models, and with
minimal customization offers rate limiting, retries, and caching. Beef is built on top of aiohttp, minimum
supported Python version is 3.9, it works with Pydantic V1 and V2.

- test without pydantic
- wheel
- Readme
- GithubAction with Pip upload, code cover, configuration matrix tests for python versions

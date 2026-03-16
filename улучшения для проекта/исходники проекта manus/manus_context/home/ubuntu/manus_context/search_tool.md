```python
import dataclasses
from typing import Literal

def search(
    brief: str,
    type: Literal["info", "image", "api", "news", "tool", "data", "research"],
    queries: list[str],
    time: Literal["all", "past_day", "past_week", "past_month", "past_year"] | None = None,
) -> dict:
  """Search for information across various sources.

  <supported_types>
  - `info`: General web information, articles, and factual answers
  - `image`: Images relevant to the topic; automatically downloaded and locally saved
  - `api`: APIs that can be invoked programmatically, including documentation and sample code
  - `news`: Time-sensitive news content from trusted media sources
  - `tool`: External tools, services, platforms, or web applications that may help achieve the task
  - `data`: Public datasets, downloadable tables, dashboards, or structured data sources
  - `research`: Academic publications, papers, whitepapers, or government/industry reports
  </supported_types>

  <instructions>
  - MUST use this tool to access up-to-date or external information when needed; DO NOT rely solely on internal knowledge
  - MUST use this tool to collect assets before creating documents, presentations, or websites
  - DO NOT use browser-based search result page parsing unless strictly necessary; prefer this tool instead
  - DO NOT rely solely on search result snippets as they are often incomplete; MUST follow up by navigating to the source URLs using browser tools
  - Each search may contain up to 3 `queries`, which MUST be variants of the same intent (i.e., query expansions), NOT different goals
  - For non-English queries, MUST include at least one English query as the final variant to expand coverage
  - For complex searches, MUST break down into step-by-step searches instead of using a single complex query
  - Access multiple URLs from search results for comprehensive information or cross-validation
  - For image results, use the attached thumbnail catalog to evaluate and select images based on the `Position` field in the result list
  - This tool automatically downloads all result images in full resolution and provides local file paths; no manual download needed
  - When using the downloaded images, MUST copy them into the target working directory, as the default save path may be cleared
  - For API results, follow the returned documentation and examples to call APIs via Python
  - MUST prioritize using APIs for bulk data access scenarios such as retrieving stock prices
  - DO NOT use advanced search syntax (quotes, filters, operators) in queries as they are not supported
  - Only use `time` parameter when explicitly required by task, otherwise leave time range unrestricted
  </instructions>

  <recommended_usage>
  - Use `info` to validate facts, discover relevant articles, or cross-check content
  - Use `image` for visual references, illustration sources, or user-requested image retrieval
  - Use `api` to find callable APIs and integrate them into code or workflows
  - Use `news` for breaking updates, current events, or recent announcements
  - Use `tool` to find apps, SaaS platforms, or plugins that can perform specific operations
  - Use `data` to locate reliable datasets or statistical information from sources like SimilarWeb or Yahoo Finance
  - Use `research` to support academic, technical, or policy-related tasks with credible publications
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    type: The category of search to perform. Determines the source and format of expected results.
    queries: Up to 3 query variants that express the same search intent
    time: Optional time filter to limit results to a recent time range
  """
```

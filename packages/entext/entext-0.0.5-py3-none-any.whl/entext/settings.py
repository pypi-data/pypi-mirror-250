from pathlib import Path


SYSTEM_PROMPT: str = (
    "In the provided string, please tell me which part is the "
    "department/school and which part the university or institution name. Reply"
    " in JSON with no explanation. The JSON should have two fields, one called"
    "department and one called university. For example, if the string was "
    "'Department of Computer Science, University of Oxford', the JSON "
    'would be {"department": "Department of Computer Science", '
    '"university": "University of Oxford"}. Make sure that all your '
    'responses use double quotes (") and not single quotes. Not all '
    "institutions are universities. They might, for example, be hospitals. "
    'Nonetheless, please always use the word "university" in your response. '
    "Finally, if a country is present, please extract that as well. This should"
    " be a separate field called country with a two-character country code. "
    "For example, if the country was 'China' then the JSON would have a country"
    " field with the value 'CN'. If the country was 'United States' then the "
    "JSON would have a country field with the value 'US'. If there is no "
    "country, then include an empty country field."
)

OPENAI_KEY: str = (Path.home() / ".openai").read_text().strip()

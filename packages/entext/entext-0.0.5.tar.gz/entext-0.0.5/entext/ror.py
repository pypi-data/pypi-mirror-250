import requests


class RORMatcher:
    def __init__(self):
        ...

    @staticmethod
    def match(institution: str) -> dict | None:
        # setup the JSON endpoint
        endpoint = (
            f"https://api.ror.org/organizations?affiliation={institution}"
        )

        # fetch the JSON
        try:
            response = requests.get(endpoint)
            json = response.json()

            # if there are no results, return None
            if len(json["items"]) == 0:
                return None

            # otherwise, return the first result if it's a perfect match with
            # chosen=true
            if json["items"][0]["chosen"]:
                return json["items"][0]

            # otherwise, return None
            return None
        except Exception as e:
            return None

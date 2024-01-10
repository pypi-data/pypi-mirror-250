import json

import typer
from rich import print


class Resolver:
    def __init__(self, llm_callable, ror_callable):
        self.llm_callable = llm_callable
        self.ror_callable = ror_callable

    def resolve(self, affiliation: str) -> dict:
        """
        Resolve an affiliation string into a department and ROR ID
        :param affiliation: the affiliation string
        :return: None
        """
        llm_json = self.llm_callable(affiliation)
        ror_json = self.ror_callable(affiliation)

        try:
            llm_json = json.loads(llm_json)

            if ror_json is None:
                ror_json = self.ror_callable(llm_json["university"])

            result = {"llm": llm_json, "ror": ror_json}
        except json.JSONDecodeError as e:
            result = {
                "llm": {"university": "", "department": "", "error": e.msg},
                "ror": ror_json,
            }

        return result


def main(affiliation: str):
    """
    Resolve an affiliation string into a department and ROR ID
    :param affiliation: the affiliation string
    :return: None
    """
    try:
        from entext.entext import open_ai, ror
    except ImportError:
        try:
            from entext import open_ai
            from entext import ror
        except ImportError:
            import open_ai
            import ror

    print(
        Resolver(
            llm_callable=open_ai.OpenAI.parse, ror_callable=ror.RORMatcher.match
        ).resolve(affiliation)
    )


if __name__ == "__main__":
    typer.run(main)

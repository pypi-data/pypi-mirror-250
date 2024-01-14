import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


class ChiselAI:
    def __init__(
        self, output_folder: str, model: str = "gpt-3.5-turbo", api_key: str = None
    ):
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "Please set the OPENAI_API_KEY environment variable or pass it in as an argument."
                )

        self.output_folder = Path(output_folder)
        print(self.output_folder)
        self.client = OpenAI()
        print("self.client")
        self.model = model

    def request(self, messages: list):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message


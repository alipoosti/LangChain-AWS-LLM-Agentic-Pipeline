import json
from langchain_aws import ChatBedrockConverse

class BaseAgent:
    def __init__(self, model_id="meta.llama3-70b-instruct-v1:0", region_name="ca-central-1"):
        self.llm = ChatBedrockConverse(
            model_id=model_id,
            region_name=region_name,
        )

    def call_llm(self, system_message: str, human_message: str) -> str:
        messages = [
            ("system", system_message),
            ("human", human_message),
        ]
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            raise RuntimeError(f"Error calling Bedrock service: {e}")

class AuthorExtractorAgent(BaseAgent):
    def extract_authors(self, page_text_md: str):
        system_msg = "You are an assistant that extracts author names from academic paper text."
        human_msg = (
            "Extract the list of author names from the following markdown text of one page of an academic paper. "
            "Return the result as a JSON array of strings, e.g. [\"John Doe\", \"Jane Doe\"].\n\n"
            f"Text:\n{page_text_md}"
        )
        response = self.call_llm(system_msg, human_msg)
        try:
            authors = json.loads(response)
            if isinstance(authors, list) and all(isinstance(a, str) for a in authors):
                return authors
            else:
                raise ValueError("Response JSON is not a list of strings")
        except Exception:
            # fallback: try to parse as plain text list separated by commas or newlines
            authors = [a.strip() for a in response.strip("[] \n").replace('"', '').split(",")]
            return [a for a in authors if a]

class AbstractExtractorAgent(BaseAgent):
    def extract_abstract(self, page_text_md: str):
        system_msg = "You are an assistant that extracts the abstract from academic paper text."
        human_msg = (
            "Extract the abstract from the following markdown text of one page of an academic paper. "
            "Return the abstract as a JSON object with a single key \"abstract\" and string value.\n\n"
            f"Text:\n{page_text_md}"
        )
        response = self.call_llm(system_msg, human_msg)
        try:
            data = json.loads(response)
            abstract = data.get("abstract", "")
            if isinstance(abstract, str):
                return abstract.strip()
            else:
                raise ValueError("Abstract is not a string")
        except Exception:
            # fallback: return raw response stripped
            return response.strip()

class TitleExtractorAgent(BaseAgent):
    def extract_title(self, page_text_md: str):
        system_msg = "You are an assistant that extracts the title from academic paper text."
        human_msg = (
            "Extract the title from the following markdown text of one page of an academic paper. "
            "Return the title as a plain string.\n\n"
            f"Text:\n{page_text_md}"
        )
        response = self.call_llm(system_msg, human_msg)
        return response.strip()

class IntroExtractorAgent(BaseAgent):
    def extract_intro_summary(self, first_5_pages_md: str):
        system_msg = "You are an assistant that summarizes the introduction of an academic paper."
        human_msg = (
            "Summarize the paper's focus, pain points, importance, and author contributions from the following markdown text "
            "of the first 5 pages of an academic paper. Return the summary as a plain string.\n\n"
            f"Text:\n{first_5_pages_md}"
        )
        response = self.call_llm(system_msg, human_msg)
        return response.strip()

class ConclusionExtractorAgent(BaseAgent):
    def extract_conclusion_summary(self, last_5_pages_md: str):
        system_msg = "You are an assistant that summarizes the conclusion of an academic paper."
        human_msg = (
            "Summarize the concluding remarks, remaining open problems, and interesting future research areas from the following markdown text "
            "of the last 5 pages of an academic paper. Return the summary as a plain string.\n\n"
            f"Text:\n{last_5_pages_md}"
        )
        response = self.call_llm(system_msg, human_msg)
        return response.strip()

class PaperSummaryWriterAgent(BaseAgent):
    def compile_summary(self, authors, abstract, title, intro_summary, conclusion_summary):
        system_msg = "You are an assistant that compiles a comprehensive summary of an academic paper."
        human_msg = (
            "Using the following extracted information, write a comprehensive summary of the academic paper.\n\n"
            f"Title: {title}\n"
            f"Authors: {', '.join(authors)}\n"
            f"Abstract: {abstract}\n"
            f"Introduction Summary: {intro_summary}\n"
            f"Conclusion Summary: {conclusion_summary}\n\n"
            "Write the summary in markdown format."
        )
        response = self.call_llm(system_msg, human_msg)
        return response.strip()
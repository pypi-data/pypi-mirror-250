from typing import List, Optional, Tuple
import traceback
from translator import LanguageDetect
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI

class GPTTranslator(LanguageDetect):
    retry_times = 3
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_base=(os.environ.get("OPENAI_PROXY") or "https://api.openai.com/v1")) # type: ignore
    input_variables = ["text", "context"]
    simple_prompt = PromptTemplate(
        input_variables=input_variables,
        template="""
CONTEXT:
{context}
############
INSTRUCTION:
- Technical terms, company names and person names should still be English
- No outmost quotation mark
- When translating, if certain parts sound awkward in Chinese, make some adjustments
############

TRANSLATE THIS COMMENT INTO CHINESE:
{text}
""")

    explain_prompt = PromptTemplate(
            input_variables=input_variables,
            template="""
TEXT CONTEXT AND BACKGROUND INFO:
{context}
############
EXPLAIN THIS TEXT IN CHINESE BASED ON THE CONTEXT
{text}
""")
    free_trans_prompt = PromptTemplate(
            input_variables=["text", "explain"],
            template="""
TEXT EXPLAINATION:
{explain}
############
COMBINED WITH THE EXPLAINATION GIVEN, TRANSLATE THE FOLLOWING TEXT INTO CHINESE:
{text}
""")
    def __init__(self, two_steps: bool) -> None:
        super().__init__()
        self.two_steps = two_steps

    @property
    def simple_chain(self) -> LLMChain:
        return LLMChain(llm=self.llm, prompt=self.simple_prompt)

    @property
    def explain_chain(self) -> LLMChain:
        return LLMChain(llm=self.llm, prompt=self.explain_prompt)

    @property
    def free_tran_chain(self) -> LLMChain:
        return LLMChain(llm=self.llm, prompt=self.free_trans_prompt)

    def trim_context(self, context: str) -> str:
        return "\n".join(context.split("\n")[:20])

    def call(self, texts: List[str], context: Optional[str] = None) -> List[str]:
        context = context or ""
        context = self.trim_context(context)
        texts = [t for t in texts]
        translate_index, translate_texts = self.filter_texts(texts)

        if self.two_steps:
            explain_chain = self.explain_chain
            free_tran_chain = self.free_tran_chain
            for idx, text in zip(translate_index, translate_texts):
                for i in range(self.retry_times):
                    try:
                        translated = free_tran_chain.run({"explain": explain_chain.run({"context": context, "text": text}), "text": text})
                        texts[idx] = translated
                    except Exception as e:
                        traceback.print_exception(e)
                        if i < self.retry_times - 1:
                            continue
                    break
        else:
            simple_chain = self.simple_chain
            for idx, text in zip(translate_index, translate_texts):
                for i in range(self.retry_times):
                    try:
                        translated = simple_chain.run({'text': text, 'context': context})
                        texts[idx] = translated
                    except Exception as e:
                        traceback.print_exception(e)
                        if i < self.retry_times - 1:
                            continue
                    break
        return texts



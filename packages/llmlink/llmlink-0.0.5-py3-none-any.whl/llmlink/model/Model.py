from typing import Any
from langchain.agents import initialize_agent, ZeroShotAgent, AgentExecutor
from langchain import OpenAI, LLMChain, HuggingFacePipeline, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from transformers import Pipeline
from .BaseModel import BaseModel


class Model(BaseModel):
    """
    A Model class to be used with applications in LLMLink

    Parameters
    ----------
    model : str or huggingface pipeline (default 'gpt-4')
        The name of the model or the pipeline itself to be used
    model_type : str (default 'chat_openai')
        The type of model to be used. Currently supports 'chat_openai', 'openai', or 'huggingface'
    memory : bool (default False)
        Whether to support memory when chatting with the model
    tools : list or None (default None)
        List of tools to give the model access to, thus creating an agent
    temperature : int (default 0)
        Temperature value to use with OpenAI models
    huggingface_task : str or None (default None)
        The task to use for the huggingface pipeline
    huggingface_model_kwargs : dict or None (default None)
        Any keyword arguments to use to load the huggingface model
    huggingface_pipeline_kwargs : dict or None (default None)
        Any keyword arguments to use to load the huggingface pipeline
    openai_api_key : str or None (default None)
        Your OpenAI API key
    """

    def __init__(
            self,
            model='gpt-4',
            model_type='chat_openai',
            memory=False,
            tools=None,
            temperature=0,
            huggingface_task=None,
            huggingface_model_kwargs=None,
            huggingface_pipeline_kwargs=None,
            openai_api_key=None
    ):
        self.model = model
        self.model_type = model_type
        self.memory = memory
        self.tools = tools
        self.temperature = temperature
        self.huggingface_task = huggingface_task
        self.huggingface_model_kwargs = huggingface_model_kwargs
        self.huggingface_pipeline_kwargs = huggingface_pipeline_kwargs
        self.openai_api_key = openai_api_key

        self._agent = self._initialize_model()

    def __call__(self, text):
        return self.run(text)

    def _initialize_model(self):
        """
        Initialize the model

        NOTE: THIS FUNCTION IS NOT INTENDED TO BE CALLED BY THE USER
        """
        if self.model_type == 'openai':
            llm = OpenAI(
                model=self.model,
                openai_api_key=self.openai_api_key,
                temperature=self.temperature
            )
        elif self.model_type == 'chat_openai':
            llm = ChatOpenAI(
                model=self.model,
                openai_api_key=self.openai_api_key,
                temperature=self.temperature
            )
        elif self.model_type == 'huggingface':
            if isinstance(self.model, Pipeline):
                llm = HuggingFacePipeline(
                    pipeline=self.model
                )
            else:
                llm = HuggingFacePipeline.from_model_id(
                    model_id=self.model,
                    task=self.huggingface_task,
                    model_kwargs=self.huggingface_model_kwargs,
                    pipeline_kwargs=self.huggingface_pipeline_kwargs
                )

        if self.tools:
            if self.memory:
                prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
                suffix = """Begin!"

                {chat_history}
                Question: {input}
                {agent_scratchpad}"""

                prompt = ZeroShotAgent.create_prompt(
                    self.tools,
                    prefix=prefix,
                    suffix=suffix,
                    input_variables=[
                        "input", "chat_history", "agent_scratchpad"],
                )
                memory = ConversationBufferMemory(memory_key="chat_history")
                llm_chain = LLMChain(llm=llm, prompt=prompt)
                agent = ZeroShotAgent(
                    llm_chain=llm_chain, tools=self.tools, verbose=True)
                return AgentExecutor.from_agent_and_tools(
                    agent=agent, tools=self.tools, verbose=True, memory=memory
                )
            else:
                return initialize_agent(
                    tools=self.tools,
                    llm=llm,
                    verbose=True
                )

        else:
            if self.memory:
                prompt = PromptTemplate(
                    template="""Have a conversation with a human, answering the following questions as best you can.
                    Begin!

                    {chat_history}
                    Question: {input}
                    """,
                    input_variables=['input', 'chat_history']
                )
                memory = ConversationBufferMemory(memory_key='chat_history')
                return LLMChain(llm=llm, prompt=prompt, memory=memory)
            else:
                return LLMChain(llm=llm, prompt=PromptTemplate(template='{input}', input_variables=['input']))

    def run(self, text):
        """
        Run the model on some text

        Parameters
        ----------
        text : str
            The user prompt to run

        Returns
        -------
        response : str
            The response from the model
        """
        response = self._agent.run(text)
        if response.startswith('AI: '):
            response = response[4:]
        return response

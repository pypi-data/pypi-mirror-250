from langchain.tools import Tool
from .BaseModel import BaseModel

PREFIX = 'Answer the following question as best you can. You have access to the following tools:'
SUFFIX = 'Begin\n\nQuestion: {question}\n'
INSTRUCTIONS = 'Use the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do next\nAction: the action to take, should be one of {tool_names}\nAction Input: The input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question'

THOUGHT = 'thought'
ACTION = 'action'
INPUT = 'input'
ANSWER = 'answer'
QUESTION = 'question'
TOOL = 'tool'
OBSERVATION = 'observation'

RESPONSE_TYPES = {
    'Thought': THOUGHT,
    'Action': ACTION,
    'Action Input': INPUT,
    'Final Answer': ANSWER,
    'Question': QUESTION,
    'Observation': OBSERVATION
}


class Agent(BaseModel):
    """
    Custom agent which implements the ReAct framework using an LLM

    Parameters
    ----------
    llm : Any
        Any LLM-like object that runs in a functional manner. i.e. llm('How are you today?') returns
        a suitable response
    tools : langchain Tool or list of Tools
        Tools for the Agent to have access to
    verbose : bool (default False)
        Whether to print intermediate outputs
    """

    def __init__(
            self,
            llm,
            tools,
            verbose=False,
            return_full_text=False
    ):
        super().__init__()
        self.llm = llm
        self.tools = tools
        self.verbose = verbose
        self.return_full_text = return_full_text

    @property
    def llm(self):
        return self._llm

    @llm.setter
    def llm(self, value):
        self._llm = value

    @property
    def tools(self):
        return self._tools

    @tools.setter
    def tools(self, value):

        if isinstance(value, list):
            if not all([isinstance(v, Tool) for v in value]):
                raise TypeError('All tools must be langchain Tool objects')

        elif isinstance(value, Tool):
            value = [value]

        else:
            raise TypeError(
                f'tools must be langchain Tool or list of Tools, got {type(value)}')

        self._tools = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):

        if not isinstance(value, bool):
            raise TypeError(f'verbose must be bool, got {type(value)}')

        self._verbose = value

    @property
    def return_full_text(self):
        return self._return_full_text

    @return_full_text.setter
    def return_full_text(self, value):
        if not isinstance(value, bool):
            raise TypeError(
                f'return_full_text must be bool, got {type(value)}')
        self._return_full_text = value

    @property
    def tool_descriptions(self):
        return '\n\n'.join([f'{tool.name}: {tool.description}' for tool in self.tools])

    @property
    def tool_dict(self):
        return {
            tool.name: tool for tool in self.tools
        }

    @property
    def tool_names(self):
        return [tool.name for tool in self.tools]

    def create_prompt(
            self,
            question,
            prefix=PREFIX,
            suffix=SUFFIX,
            instructions=INSTRUCTIONS
    ):
        """
        Format the initial prompt for the LLM
        """
        return f'{prefix}\n\n{self.tool_descriptions}\n\n{instructions}\n\n{suffix}'.format(
            question=question,
            tool_names=self.tool_names
        )

    def run_tool(
            self,
            tool_name,
            tool_input
    ):
        """
        Run the specified tool
        """

        the_tool = self.tool_dict.get(tool_name)

        if the_tool:
            try:
                return the_tool(tool_input).strip()
            except Exception as e:
                return (f'Tool encountered an error: {e}')
        else:
            return f'No tool with the name {tool_name} found'

    def parse_output(
            self,
            output
    ):
        """
        Parse the output from the model
        """

        lines = output.splitlines()
        response = {}
        current_type = None

        for idx in range(len(lines)):

            if lines[idx].strip() == '':
                continue

            type_of_response = RESPONSE_TYPES.get(
                lines[idx].split(':')[0].strip())

            if type_of_response == THOUGHT:
                current_type == THOUGHT
                response[THOUGHT] = ':'.join(lines[idx].split(':')[1:]).strip()
            elif type_of_response == ACTION:
                current_type = ACTION
                response[ACTION] = TOOL
                response[TOOL] = ':'.join(lines[idx].split(':')[1:]).strip()
            elif type_of_response == INPUT:
                current_type = INPUT
                response[INPUT] = ':'.join(lines[idx].split(':')[1:]).strip()
            elif type_of_response == ANSWER:
                current_type = ANSWER
                response[ACTION] = ANSWER
                response[ANSWER] = ':'.join(lines[idx].split(':')[1:]).strip()
            elif type_of_response is None:
                if current_type:
                    response[current_type] += '\n' + lines[idx]
                else:
                    type_of_response = THOUGHT
                    response[THOUGHT] = lines[idx].strip()
            elif type_of_response in [QUESTION, OBSERVATION]:
                return response

        return response

    def run(
            self,
            question,
            return_full_text=None
    ):
        """
        Run the Agent for a question

        Parameters
        ----------
        question : str
            The input question for the Agent

        Returns
        -------
        response : dict
            Dictionary with the keys 'response' and 'full_text', containing
            the final response from the model and the full text generated by the model
            and the tools, respectively
        """

        if not return_full_text:
            return_full_text = self.return_full_text

        prompt = self.create_prompt(question)

        if self.verbose:
            print('INITIAL PROMPT:')
            print('\n')
            print(prompt)
            print('\n\n')

        while True:
            response = self.llm(prompt).strip()

            if self.verbose:
                print('MODEL RESPONSE:')
                print('\n')
                print(response)
                print('\n\n')

            action = self.parse_output(response)

            if self.verbose:
                print('PARSED ACTION:')
                print('\n')
                print(action)
                print('\n\n')

            if action.get(ACTION) == TOOL:
                tool_response = self.run_tool(
                    action[TOOL],
                    action[INPUT]
                )

                if tool_response == '':
                    tool_response = 'Tool returned no results'
                if action.get(THOUGHT):
                    prompt += f'Thought: {action[THOUGHT]}\nAction: {action[TOOL]}\nAction Input: {action[INPUT]}\nObservation: {tool_response}\n'
                else:
                    prompt += f'Action: {action[TOOL]}\nAction Input: {action[INPUT]}\nObservation: {tool_response}\n'

                if self.verbose:
                    print('NEW PROMPT:')
                    print('\n')
                    print(prompt)
                    print('\n\n')

            elif action.get(ACTION) == ANSWER:
                if action.get(THOUGHT):
                    prompt += f'Thought: {action[THOUGHT]}\nFinal Answer: {action[ANSWER]}'
                else:
                    prompt += f'Final Answer: {action[ANSWER]}'

                if self.verbose:
                    print('FINAL TEXT:')
                    print('\n')
                    print(prompt)

                if return_full_text:
                    return {
                        'response': action[ANSWER],
                        'full_text': prompt
                    }
                else:
                    return action[ANSWER]

            elif action.get(ACTION) is None:
                prompt += f'{response}\n\nWARNING: No parsable action detected - be sure to utilize the format provided'

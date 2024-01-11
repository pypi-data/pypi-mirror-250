from .utils import binary_feedback_handler, correction_feedback_handler, print_feedback, feedback, save_feedback_to_csv
from llmlink.model import BaseModel
import gradio as gr


class App:
    """
    An App class that wraps a model to be used in a Gradio chat interface

    Parameters
    ----------
    model : chainlink Model or custom class that extends the BaseModel class
        The model to be used with the application
    feedback : bool (default False)
        Whether to collect feedback within the app
    theme : str or None
        The gradio theme to use
    feedback_callback : function (default print_feedback)
        Function to use when feedback is submitted
    """

    def __init__(
            self,
            model,
            feedback=False,
            theme=None,
            feedback_callback=print_feedback
    ):
        self.model = model
        self.feedback = feedback
        self.theme = theme
        self.feedback_callback = feedback_callback

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if not isinstance(value, BaseModel):
            raise TypeError('model must inherit from BaseModel class')
        self._model = value

    @property
    def feedback(self):
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        if not isinstance(value, bool):
            raise TypeError('feedback must be bool')
        self._feedback = value

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('theme must be str')
        self._theme = value

    def deploy(self, *args, **kwargs):
        """
        Deploy the application

        Parameters
        ----------
        *args : various arguments
            Arguments to send to gradio.Blocks().launch()
        **kwargs : various keyword arguments
            Keyword arguments to send to gradio.Blocks().launch()

        Returns
        -------
        deploy_results
            The results of running the gradio deploy function
        """
        if not self.feedback:
            with gr.Blocks(theme=self.theme) as demo:
                chatbot = gr.Chatbot(label='ChainLink App')
                msg = gr.Textbox(
                    lines=1,
                    max_lines=20,
                    placeholder='Input your text here.'
                )
                clear = gr.ClearButton([msg, chatbot])
                gr.Blocks()

                def respond(message, chat_history):
                    try:
                        bot_message = self.model.run(message)
                        chat_history.append((message, bot_message))
                        return "", chat_history
                    except Exception as e:
                        print(e)
                        chat_history.append(
                            (message, '**There was an error communicating with the bot**'))
                        return "", chat_history

                msg.submit(respond, [msg, chatbot], [msg, chatbot])

            return demo.launch(*args, **kwargs)

        else:
            with gr.Blocks(theme=self.theme) as demo:
                chatbot = gr.Chatbot(label='ChainLink App', elem_id='chatbot')

                with gr.Row():
                    with gr.Column(scale=100):
                        msg = gr.Textbox(
                            lines=1,
                            max_lines=20,
                            show_label=False,
                            placeholder='Input your text here.',
                            elem_id='user_msg_input'
                        )
                with gr.Row():
                    clear = gr.ClearButton([msg, chatbot])

                with gr.Row():
                    with gr.Column():
                        binary = gr.Radio(
                            ['Good Response', 'Bad Response'],
                            label='Was this a good response?',
                            value=None,
                            elem_id='binary_feedback_selector'
                        )

                with gr.Row():
                    with gr.Column(scale=100):
                        correction = gr.Textbox(
                            show_label=True,
                            label='Correction (optional)',
                            placeholder='Enter your correction here',
                            elem_id='user_correction_input'
                        )

                with gr.Row():
                    with gr.Column(scale=100):
                        submit_button = gr.Button(
                            value='Submit Feedback', elem_id='submit_feedback_button')

                def respond(message, chat_history):
                    try:
                        bot_message = self.model.run(message)
                        chat_history.append((message, bot_message))
                        feedback['user_msg'] = message
                        feedback['bot_msg'] = bot_message
                        return "", chat_history
                    except Exception as e:
                        print(e)
                        chat_history.append(
                            (message, '**There was an error communicating with the bot**'))
                        return "", chat_history

                msg.submit(respond, [msg, chatbot], [msg, chatbot])
                binary.change(fn=lambda choice: binary_feedback_handler(
                    choice), inputs=[binary])
                correction.change(fn=lambda correction: correction_feedback_handler(
                    correction), inputs=[correction])
                submit_button.click(fn=self.feedback_callback)

            return demo.launch(*args, **kwargs)

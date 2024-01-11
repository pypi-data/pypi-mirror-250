import csv
import os

feedback = {
    'user_msg': None,
    'bot_msg': None,
    'binary_feedback': None,
    'correction': None
}


def binary_feedback_handler(choice):
    feedback['binary_feedback'] = 1 if choice == 'Good Response' else -1


def correction_feedback_handler(correction):
    feedback['correction'] = correction


def print_feedback():
    """
    Default function to submit feedback - simply prints the feedback to the console
    """
    if feedback['user_msg'] is not None and feedback['bot_msg'] is not None:
        print(f'User Messsage: {feedback["user_msg"]}')
        print(f'Bot Message: {feedback["bot_msg"]}')
        print(f'Binary Feedback: {feedback["binary_feedback"]}')
        print(f'Correction: {feedback["correction"]}')

    feedback['user_msg'] = None
    feedback['bot_msg'] = None
    feedback['binary_feedback'] = None
    feedback['correction'] = None


def save_feedback_to_csv(path='./feedback.csv'):
    if feedback['user_msg'] is not None and feedback['bot_msg'] is not None:
        csv_exists = os.path.isfile(path)
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not csv_exists:
                writer.writerow(['user_prompt', 'bot_response',
                                'binary_feedback', 'correction'])
            writer.writerow([feedback['user_msg'], feedback['bot_msg'],
                            feedback['binary_feedback'], feedback['correction']])

    feedback['user_msg'] = None
    feedback['bot_msg'] = None
    feedback['binary_feedback'] = None
    feedback['correction'] = None

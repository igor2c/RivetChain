import chainlit as cl
from chainlit.types import ThreadDict
import json
from rivet_py.rivet_client import setup_rivet, call_rivet

# Ensure the Rivet Node.js server is running
setup_rivet(rivet_project_filepath=r'.\rivet_py\projects\chat.rivet-project',
            rivet_server_filepath=r'.\rivet_py\rivet_server.js')


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    """ Displays button to resume chat """
    # https://github.com/Chainlit/cookbook/blob/main/resume-chat/app.py
    pass


@cl.on_message
async def main(user_message: cl.Message):

    # Get `message_history` variable from current `user_session`
    message_history = cl.user_session.get("message_history")  # type : list of lists, example: [["user", "Hello?"], ["assistant", "Hi!"]]
    if message_history is None:
        message_history = []

    # Call Rivet
    response_dict = call_rivet(inputs={'message_history': json.dumps(message_history),
                                       'user_message': user_message.content},
                               graph="Main Folder/Main Graph")

    # Parse Rivet response
    content = response_dict.get('output', {}).get('value', None)
    if content is None:
        content = response_dict.get('error', 'Unknown error.')
    assistant_message = cl.Message(content=content)

    # Set new `message_history` variable in current `user_session`
    message_history.append({"type": "user", "message": user_message.content})
    message_history.append({"type": "assistant", "message": assistant_message.content})
    cl.user_session.set("message_history", message_history)

    # Send response
    await assistant_message.send()


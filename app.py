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
async def main(message: cl.Message):

    response = cl.Message(content="")

    # Get memory variable from Chainlit thread
    memory = cl.user_session.get("memory")  # type : list of lists, example: [["user", "Hello?"], ["assistant", "Hi!"]]
    if memory is None:
        memory = []

    # Generate response
    response_dict = call_rivet(inputs={'previous_messages': json.dumps(memory), 'user_message': message.content},
                               graph="Main Folder/Main Graph")
    response.content = response_dict.get('output', {}).get('value', None)
    if not response.content:
        response.content = response_dict.get('error', '???')

    # Set new memory variable in Chainlit thread
    memory.append(["user", message.content])
    memory.append(["assistant", response.content])
    cl.user_session.set("memory", memory)

    # Send response
    await response.send()


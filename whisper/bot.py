# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        # Check if bot was tagged to a message and respond accordingly
        # Get message current user text was tagged to
        message = turn_context.activity.text
        bot_name = "whisper_to_text"
        # Check if bot was tagged to message
        if f"@{bot_name}" in message:
            # If bot was tagged, respond with a message
            await turn_context.send_activity(f"You tagged me in a message! You said '{ turn_context.activity.text }'")

        elif "/transcribe" in message:
            await turn_context.send_activity(f"You tagged me in a message! You said '{ turn_context.activity.text }'")

        elif "/translate" in message:
            await turn_context.send_activity(f"You tagged me in a message! You said '{ turn_context.activity.text }'")

        elif "/summarize" in message:
            await turn_context.send_activity(f"You tagged me in a message! You said '{ turn_context.activity.text }'")

        else:
            # If bot was not tagged, respond with a message

        # await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

        

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

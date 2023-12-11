from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from time import time
from os import environ
from openai import OpenAI
import json
import logging

if not (access_token := environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
    raise Exception("access token is not set as an environment variable")

if not (channel_secret := environ.get("LINE_CHANNEL_SECRET")):
    raise Exception("channel secret is not set as an environment variable")

if not (api_key := environ.get("OPENAI_API_KEY")):
    raise Exception("openai api key is not set as an environment variable")

client = OpenAI(api_key=api_key)
configuration = Configuration(access_token = access_token)
handler = WebhookHandler(channel_secret)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # TODO implement
    # logger.info(event)
    signature = event['headers']['x-line-signature']
    body = event['body']
      # handle webhook body
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)  # エラーをログに記録
        return {'statusCode': 500, 'body': 'Error'}

    return {'statusCode': 200, 'body': 'OK'}

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": event.message.text,
            }
        ],
        model="gpt-4-1106-preview",
        )
        logger.info(chat_completion)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=chat_completion.choices[0].message.content)]
            )
        )

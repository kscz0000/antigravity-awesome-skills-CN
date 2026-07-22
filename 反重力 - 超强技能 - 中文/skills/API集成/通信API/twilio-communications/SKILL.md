---
name: twilio-communications
description: "使用 Twilio 构建通信功能：短信、语音通话、WhatsApp Business API 和用户验证（双因素认证）。覆盖从简单通知到复杂 IVR 系统和多渠道认证的完整场景。"
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Twilio 通信

使用 Twilio 构建通信功能：短信、语音通话、WhatsApp Business API 和用户验证（双因素认证）。覆盖从简单通知到复杂 IVR 系统和多渠道认证的完整场景。重点关注合规性、速率限制和错误处理。

## 模式

### 短信发送模式

使用 Twilio 发送短信的基础模式。处理核心功能：电话号码格式化、消息传递和传递状态回调。

关键注意事项：
- 电话号码必须采用 E.164 格式（+1234567890）
- 默认速率限制：每秒 80 条消息（MPS）
- 超过 160 字符的消息会被拆分（成本更高）
- 运营商过滤可能阻止消息（特别是发送到美国号码）

**适用场景**：向用户发送通知、交易消息（订单确认、发货）、警报和提醒

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
import re

class TwilioSMS:
    """
    SMS sending with proper error handling and validation.
    """

    def __init__(self):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )
        self.from_number = os.environ["TWILIO_PHONE_NUMBER"]

    def validate_e164(self, phone: str) -> bool:
        """Validate phone number is in E.164 format."""
        pattern = r'^\+[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))

    def send_sms(
        self,
        to: str,
        body: str,
        status_callback: str = None
    ) -> dict:
        """
        Send an SMS message.

        Args:
            to: Recipient phone number in E.164 format
            body: Message text (160 chars = 1 segment)
            status_callback: URL for delivery status webhooks

        Returns:
            Message SID and status
        """
        # Validate phone number format
        if not self.validate_e164(to):
            return {
                "success": False,
                "error": "Phone number must be in E.164 format (+1234567890)"
            }

        # Check message length (warn about segmentation)
        segment_count = (len(body) + 159) // 160
        if segment_count > 1:
            print(f"Warning: Message will be sent as {segment_count} segments")

        try:
            message = self.client.messages.create(
                to=to,
                from_=self.from_number,
                body=body,
                status_callback=status_callback
            )

            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status,
                "segments": segment_count
            }

        except TwilioRestException as e:
            return self._handle_error(e)

    def _handle_error(self, error: TwilioRestException) -> dict:
        """Handle Twilio-specific errors."""
        error_handlers = {
            21610: "Recipient has opted out. They must reply START.",
            21614: "Invalid 'To' phone number format.",
            21211: "'From' phone number is not valid.",
            30003: "Phone is unreachable (off, airplane mode, no signal).",
            30005: "Unknown destination (invalid number or landline).",
            30006: "Landline or unreachable carrier.",
            30429: "Rate limit exceeded. Implement exponential backoff.",
        }

        return {
            "success": False,
            "error_code": error.code,
            "error": error_handlers.get(error.code, error.msg),
            "details": str(error)
        }

# Usage
sms = TwilioSMS()
result = sms.send_sms(
    to="+14155551234",
    body="Your order #1234 has shipped!",
    status_callback="https://your-app.com/webhooks/twilio/status"
)

### 反模式

- 发送前未验证 E.164 格式
- 在代码中硬编码 Twilio 凭据
- 忽略传递状态回调
- 未处理用户退订（21610）错误

### Twilio Verify 模式（双因素认证/一次性密码）

使用 Twilio Verify 进行电话号码验证和双因素认证。处理代码生成、传递、速率限制和欺诈预防。

相比自建一次性密码的关键优势：
- Twilio 管理代码生成和过期
- 内置欺诈预防（已为客户节省 8200 万美元以上，阻止了 7.47 亿次尝试）
- 自动处理速率限制
- 多渠道支持：短信、语音、电子邮件、推送、WhatsApp

Google 发现短信双因素认证可阻止"100% 的自动化机器人、96% 的批量钓鱼攻击和 76% 的定向攻击"。

**适用场景**：注册时用户电话号码验证、双因素认证（2FA）、密码重置验证、高价值交易确认

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from enum import Enum
from typing import Optional

class VerifyChannel(Enum):
    SMS = "sms"
    CALL = "call"
    EMAIL = "email"
    WHATSAPP = "whatsapp"

class TwilioVerify:
    """
    Phone verification with Twilio Verify.
    Never store OTP codes - Twilio handles it.
    """

    def __init__(self, verify_service_sid: str = None):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )
        # Create a Verify Service in Twilio Console first
        self.service_sid = verify_service_sid or os.environ["TWILIO_VERIFY_SID"]

    def send_verification(
        self,
        to: str,
        channel: VerifyChannel = VerifyChannel.SMS,
        locale: str = "en"
    ) -> dict:
        """
        Send verification code to phone/email.

        Args:
            to: Phone number (E.164) or email
            channel: SMS, call, email, or whatsapp
            locale: Language code for message

        Returns:
            Verification status
        """
        try:
            verification = self.client.verify \
                .v2 \
                .services(self.service_sid) \
                .verifications \
                .create(
                    to=to,
                    channel=channel.value,
                    locale=locale
                )

            return {
                "success": True,
                "status": verification.status,  # "pending"
                "channel": channel.value,
                "valid": verification.valid
            }

        except TwilioRestException as e:
            return self._handle_verify_error(e)

    def check_verification(self, to: str, code: str) -> dict:
        """
        Check if verification code is correct.

        Args:
            to: Phone number or email that received code
            code: The code entered by user

        Returns:
            Verification result
        """
        try:
            check = self.client.verify \
                .v2 \
                .services(self.service_sid) \
                .verification_checks \
                .create(
                    to=to,
                    code=code
                )

            return {
                "success": True,
                "valid": check.status == "approved",
                "status": check.status  # "approved" or "pending"
            }

        except TwilioRestException as e:
            # Code was wrong or expired
            return {
                "success": False,
                "valid": False,
                "error": str(e)
            }

    def _handle_verify_error(self, error: TwilioRestException) -> dict:
        """Handle Verify-specific errors."""
        error_handlers = {
            60200: "Invalid phone number format",
            60203: "Max send attempts reached for this number",
            60205: "Service not found - check VERIFY_SID",
            60223: "Failed to create verification - carrier rejected",
        }

        return {
            "success": False,
            "error_code": error.code,
            "error": error_handlers.get(error.code, error.msg)
        }

# Usage Example - Signup Flow
verify = TwilioVerify()

# Step 1: User enters phone number
result = verify.send_verification("+14155551234", VerifyChannel.SMS)
if result["success"]:
    print("Code sent! Check your phone.")

# Step 2: User enters the code they received
code = "123456"  # From user input
check = verify.check_verification("+14155551234", code)

if check["valid"]:
    print("Phone verified! Create account.")
else:
    print("Invalid code. Try again.")

# Best Practice: Offer voice fallback
async def verify_with_fallback(phone: str, max_attempts: int = 3):
    """Verify with voice fallback if SMS fails."""
    for attempt in range(max_attempts):
        channel = VerifyChannel.SMS if attempt == 0 else VerifyChannel.CALL
        result = verify.send_verification(phone, channel)

        if result["success"]:
            return result

        # If SMS failed, wait and try voice
        if channel == VerifyChannel.SMS:
            await asyncio.sleep(30)
            continue

    return {"success": False, "error": "All verification attempts failed"}

### 反模式

- 在数据库中存储一次性密码（Twilio 会处理）
- 未在验证端点实施速率限制
- 使用相同代码重试（让 Verify 生成新代码）
- 短信失败时无备用渠道

### TwiML IVR 模式

使用 TwiML 构建交互式语音应答（IVR）系统。TwiML（Twilio 标记语言）是 XML，告诉 Twilio 接收来电时该做什么。

核心 TwiML 动词：
- <Say>：文本转语音
- <Play>：播放音频文件
- <Gather>：收集按键/语音输入
- <Dial>：连接到另一个号码
- <Record>：录制来电者语音
- <Redirect>：移动到另一个 TwiML 端点

关键洞察：Twilio 向您的 webhook 发送 HTTP 请求，您返回 TwiML，Twilio 执行它。无状态，因此使用 URL 参数或会话。

**适用场景**：电话菜单系统（按 1 转销售...）、自动化客户支持、带确认的预约提醒、语音信箱系统

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.request_validator import RequestValidator
import os

app = Flask(__name__)

def validate_twilio_request(f):
    """Decorator to validate requests are from Twilio."""
    def wrapper(*args, **kwargs):
        validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

        # Get request details
        url = request.url
        params = request.form.to_dict()
        signature = request.headers.get("X-Twilio-Signature", "")

        if not validator.validate(url, params, signature):
            return "Invalid request", 403

        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/voice/incoming", methods=["POST"])
@validate_twilio_request
def incoming_call():
    """Handle incoming call with IVR menu."""
    response = VoiceResponse()

    # Gather digits with timeout
    gather = Gather(
        num_digits=1,
        action="/voice/menu-selection",
        method="POST",
        timeout=5
    )
    gather.say(
        "Welcome to Acme Corp. "
        "Press 1 for sales. "
        "Press 2 for support. "
        "Press 3 to leave a message."
    )
    response.append(gather)

    # If no input, repeat
    response.redirect("/voice/incoming")

    return Response(str(response), mimetype="text/xml")

@app.route("/voice/menu-selection", methods=["POST"])
@validate_twilio_request
def menu_selection():
    """Route based on menu selection."""
    response = VoiceResponse()
    digit = request.form.get("Digits", "")

    if digit == "1":
        # Transfer to sales
        response.say("Connecting you to sales.")
        response.dial(os.environ["SALES_PHONE"])

    elif digit == "2":
        # Transfer to support
        response.say("Connecting you to support.")
        response.dial(os.environ["SUPPORT_PHONE"])

    elif digit == "3":
        # Voicemail
        response.say("Please leave a message after the beep.")
        response.record(
            action="/voice/voicemail-saved",
            max_length=120,
            transcribe=True,
            transcribe_callback="/voice/transcription"
        )

    else:
        response.say("Invalid selection.")
        response.redirect("/voice/incoming")

    return Response(str(response), mimetype="text/xml")

@app.route("/voice/voicemail-saved", methods=["POST"])
@validate_twilio_request
def voicemail_saved():
    """Handle saved voicemail."""
    response = VoiceResponse()

    recording_url = request.form.get("RecordingUrl")
    recording_sid = request.form.get("RecordingSid")

    # Save to database, notify team, etc.
    print(f"Voicemail saved: {recording_url}")

    response.say("Thank you. Goodbye.")
    response.hangup()

    return Response(str(response), mimetype="text/xml")

@app.route("/voice/transcription", methods=["POST"])
@validate_twilio_request
def transcription_callback():
    """Handle voicemail transcription."""
    transcription = request.form.get("TranscriptionText")
    recording_sid = request.form.get("RecordingSid")

    # Save transcription, send to Slack, etc.
    print(f"Transcription: {transcription}")

    return "", 200

# Outbound call example
from twilio.rest import Client

def make_outbound_call(to: str, message: str):
    """Make outbound call with custom TwiML."""
    client = Client(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"]
    )

    # TwiML Bin URL or your endpoint
    call = client.calls.create(
        to=to,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        url="https://your-app.com/voice/outbound-message",
        status_callback="https://your-app.com/voice/status"
    )

    return call.sid

if __name__ == "__main__":
    app.run(debug=True)

### 反模式

- 未验证 X-Twilio-Signature（安全风险）
- 向 Twilio 返回非 XML 响应
- 未处理超时/无输入情况
- 在 TwiML 中硬编码电话号码

### WhatsApp Business API 模式

通过 Twilio API 发送和接收 WhatsApp 消息。使用与短信相同的 Twilio Messages API，只需少量更改。

关键 WhatsApp 规则：
- 24 小时会话窗口：只能在用户消息后 24 小时内回复
- 模板消息：用于会话窗口外的预批准模板
- 需要用户明确同意接收消息
- 速率限制：默认 80 MPS（经批准可达 400）
- 字符限制：非模板 1024 字符，模板约 550 字符

**适用场景**：富媒体客户支持、带按钮的订单通知、营销消息（使用模板）、交互式流程（预订、调查）

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from datetime import datetime, timedelta
from typing import Optional

class TwilioWhatsApp:
    """
    WhatsApp Business API via Twilio.
    Handles session windows and template messages.
    """

    def __init__(self):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )
        # WhatsApp number format: whatsapp:+14155551234
        self.from_number = os.environ["TWILIO_WHATSAPP_NUMBER"]

    def send_message(
        self,
        to: str,
        body: str,
        media_url: Optional[str] = None
    ) -> dict:
        """
        Send WhatsApp message within 24-hour session.

        Args:
            to: Recipient number (E.164, without whatsapp: prefix)
            body: Message text (max 1024 chars for non-template)
            media_url: Optional image/document URL

        Returns:
            Message result
        """
        # Format for WhatsApp
        to_whatsapp = f"whatsapp:{to}"
        from_whatsapp = f"whatsapp:{self.from_number}"

        try:
            message_params = {
                "to": to_whatsapp,
                "from_": from_whatsapp,
                "body": body
            }

            if media_url:
                message_params["media_url"] = [media_url]

            message = self.client.messages.create(**message_params)

            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }

        except TwilioRestException as e:
            return self._handle_whatsapp_error(e)

    def send_template_message(
        self,
        to: str,
        content_sid: str,
        content_variables: dict
    ) -> dict:
        """
        Send pre-approved template message.
        Use this for messages outside 24-hour window.

        Content templates must be approved by WhatsApp first.
        Create them in Twilio Console > Content Template Builder.
        """
        to_whatsapp = f"whatsapp:{to}"
        from_whatsapp = f"whatsapp:{self.from_number}"

        try:
            message = self.client.messages.create(
                to=to_whatsapp,
                from_=from_whatsapp,
                content_sid=content_sid,
                content_variables=content_variables
            )

            return {
                "success": True,
                "message_sid": message.sid,
                "template": True
            }

        except TwilioRestException as e:
            return self._handle_whatsapp_error(e)

    def _handle_whatsapp_error(self, error: TwilioRestException) -> dict:
        """Handle WhatsApp-specific errors."""
        error_handlers = {
            63016: "Outside 24-hour window. Use template message.",
            63018: "Template not approved or doesn't exist.",
            63025: "Too many template messages sent to this user.",
            63038: "Rate limit exceeded for WhatsApp.",
        }

        return {
            "success": False,
            "error_code": error.code,
            "error": error_handlers.get(error.code, error.msg)
        }

# Flask webhook for incoming WhatsApp messages
from flask import Flask, request

app = Flask(__name__)

@app.route("/webhooks/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages."""
    from_number = request.form.get("From", "").replace("whatsapp:", "")
    body = request.form.get("Body", "")
    media_url = request.form.get("MediaUrl0")  # First attachment

    # Track session start (24-hour window begins now)
    session_start = datetime.now()
    session_expires = session_start + timedelta(hours=24)

    # Store in database for session tracking
    # user_sessions[from_number] = session_expires

    # Process message and respond
    response = process_whatsapp_message(from_number, body, media_url)

    # Reply within session
    whatsapp = TwilioWhatsApp()
    whatsapp.send_message(from_number, response)

    return "", 200

def process_whatsapp_message(phone: str, text: str, media: str) -> str:
    """Process incoming message and generate response."""
    text_lower = text.lower()

    if "order status" in text_lower:
        return "Your order #1234 is out for delivery!"
    elif "support" in text_lower:
        return "A support agent will contact you shortly."
    else:
        return "Thanks for your message! Reply with 'order status' or 'support'."

# Send typing indicator (2025 feature)
def send_typing_indicator(to: str):
    """Let user know you're typing."""
    # Requires Senders API setup
    pass

### 反模式

- 在 24 小时窗口外发送非模板消息
- 未按用户跟踪会话窗口
- 超过会话消息 1024 字符限制
- 未处理模板拒绝错误

### Webhook 处理模式

处理 Twilio webhooks 以获取传递状态、来电消息和通话事件。关键：始终验证 X-Twilio-Signature。

Twilio 发送 webhooks 用于：
- 消息状态更新（排队 → 发送 → 已传递/失败）
- 来电短信/WhatsApp 消息
- 通话事件（发起、响铃、接听、完成）
- 录音/转录就绪

**适用场景**：跟踪消息传递状态、接收来电消息、通话分析和日志记录、语音信箱转录处理

from flask import Flask, request, abort
from twilio.request_validator import RequestValidator
from functools import wraps
import os
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

def validate_twilio_signature(f):
    """
    Validate that request came from Twilio.
    CRITICAL: Always use this for webhook endpoints.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

        # Build full URL (including query params)
        url = request.url

        # Get POST body as dict
        params = request.form.to_dict()

        # Get signature from header
        signature = request.headers.get("X-Twilio-Signature", "")

        if not validator.validate(url, params, signature):
            logger.warning(f"Invalid Twilio signature from {request.remote_addr}")
            abort(403)

        return f(*args, **kwargs)
    return wrapper

@app.route("/webhooks/twilio/sms/status", methods=["POST"])
@validate_twilio_signature
def sms_status_callback():
    """
    Handle SMS delivery status updates.

    Status progression: queued → sending → sent → delivered
    Or: queued → sending → undelivered/failed
    """
    message_sid = request.form.get("MessageSid")
    status = request.form.get("MessageStatus")
    error_code = request.form.get("ErrorCode")
    error_message = request.form.get("ErrorMessage")

    logger.info(f"SMS {message_sid}: {status}")

    if status == "delivered":
        # Message successfully delivered
        update_message_status(message_sid, "delivered")

    elif status == "undelivered":
        # Carrier rejected or other failure
        logger.error(f"SMS failed: {error_code} - {error_message}")
        handle_failed_message(message_sid, error_code, error_message)

    elif status == "failed":
        # Twilio couldn't send
        logger.error(f"SMS send failed: {error_code}")
        handle_failed_message(message_sid, error_code, error_message)

    return "", 200

@app.route("/webhooks/twilio/sms/incoming", methods=["POST"])
@validate_twilio_signature
def incoming_sms():
    """
    Handle incoming SMS messages.
    """
    from_number = request.form.get("From")
    to_number = request.form.get("To")
    body = request.form.get("Body")
    num_media = int(request.form.get("NumMedia", 0))

    # Handle media attachments
    media_urls = []
    for i in range(num_media):
        media_urls.append(request.form.get(f"MediaUrl{i}"))

    # Check for opt-out keywords
    if body.strip().upper() in ["STOP", "UNSUBSCRIBE", "CANCEL"]:
        handle_opt_out(from_number)
        return "", 200

    # Check for opt-in keywords
    if body.strip().upper() in ["START", "SUBSCRIBE"]:
        handle_opt_in(from_number)
        return "", 200

    # Process message
    process_incoming_sms(from_number, body, media_urls)

    return "", 200

@app.route("/webhooks/twilio/voice/status", methods=["POST"])
@validate_twilio_signature
def voice_status_callback():
    """Handle call status updates."""
    call_sid = request.form.get("CallSid")
    status = request.form.get("CallStatus")
    duration = request.form.get("CallDuration")
    direction = request.form.get("Direction")

    # Call statuses: initiated, ringing, in-progress, completed, busy, no-answer, canceled, failed

    logger.info(f"Call {call_sid}: {status} ({duration}s)")

    if status == "completed":
        # Call ended normally
        log_call_completion(call_sid, duration)

    elif status in ["busy", "no-answer", "canceled", "failed"]:
        # Call didn't connect
        handle_failed_call(call_sid, status)

    return "", 200

# Helper functions
def update_message_status(message_sid: str, status: str):
    """Update message status in database."""
    pass

def handle_failed_message(message_sid: str, error_code: str, error_msg: str):
    """Handle failed message delivery."""
    # Notify team, retry logic, etc.
    pass

def handle_opt_out(phone: str):
    """Handle user opting out of messages."""
    # Mark user as opted out in database
    # IMPORTANT: Must respect this!
    pass

def handle_opt_in(phone: str):
    """Handle user opting back in."""
    pass

def process_incoming_sms(from_phone: str, body: str, media: list):
    """Process incoming SMS message."""
    pass

def log_call_completion(call_sid: str, duration: str):
    """Log completed call."""
    pass

def handle_failed_call(call_sid: str, status: str):
    """Handle call that didn't connect."""
    pass

### 反模式

- 未验证 X-Twilio-Signature
- 暴露未经身份验证的 webhook URL
- 未处理退订关键词（STOP）
- 阻塞 webhook 响应（应快速返回）

### 速率限制和重试模式

处理 Twilio 速率限制并实施适当的重试逻辑。

默认限制：
- 短信：每秒 80 条消息（MPS）
- 语音：因号码类型和地区而异
- API 调用：每秒 100 个请求

错误代码：
- 20429：语音 API 速率限制
- 30429：消息 API 速率限制

**适用场景**：高容量消息应用、批量短信活动、自动化呼叫系统

import time
import random
from functools import wraps
from twilio.base.exceptions import TwilioRestException
import logging

logger = logging.getLogger(__name__)

def exponential_backoff_retry(
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    rate_limit_codes: list = [20429, 30429]
):
    """
    Decorator for exponential backoff retry on rate limits.

    Uses jitter to prevent thundering herd.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except TwilioRestException as e:
                    last_exception = e

                    # Only retry on rate limit errors
                    if e.code not in rate_limit_codes:
                        raise

                    if attempt == max_retries:
                        logger.error(f"Max retries exceeded: {e}")
                        raise

                    # Calculate delay with jitter
                    delay = min(
                        base_delay * (2 ** attempt) + random.uniform(0, 1),
                        max_delay
                    )

                    logger.warning(
                        f"Rate limited (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {delay:.1f}s"
                    )
                    time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator

# Usage
from twilio.rest import Client

client = Client(account_sid, auth_token)

@exponential_backoff_retry(max_retries=5)
def send_sms(to: str, body: str):
    return client.messages.create(
        to=to,
        from_=from_number,
        body=body
    )

# Bulk sending with rate limiting
import asyncio
from asyncio import Semaphore

class RateLimitedSender:
    """
    Send messages with built-in rate limiting.
    Stays under Twilio's 80 MPS limit.
    """

    def __init__(self, client, from_number: str, mps: int = 50):
        self.client = client
        self.from_number = from_number
        self.mps = mps
        self.semaphore = Semaphore(mps)

    async def send_bulk(self, messages: list[dict]) -> list[dict]:
        """
        Send messages with rate limiting.

        Args:
            messages: List of {"to": "+1...", "body": "..."}

        Returns:
            Results for each message
        """
        tasks = [
            self._send_with_limit(msg["to"], msg["body"])
            for msg in messages
        ]

        return await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_with_limit(self, to: str, body: str):
        """Send single message with semaphore-based rate limit."""
        async with self.semaphore:
            try:
                # Use sync client in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: self.client.messages.create(
                        to=to,
                        from_=self.from_number,
                        body=body
                    )
                )
                return {"success": True, "sid": result.sid, "to": to}

            except TwilioRestException as e:
                return {"success": False, "error": str(e), "to": to}

            finally:
                # Delay to maintain rate limit
                await asyncio.sleep(1 / self.mps)

# Usage
async def send_campaign():
    sender = RateLimitedSender(client, from_number, mps=50)

    messages = [
        {"to": "+14155551234", "body": "Hello!"},
        {"to": "+14155555678", "body": "Hello!"},
        # ... thousands of messages
    ]

    results = await sender.send_bulk(messages)

    successful = sum(1 for r in results if r.get("success"))
    print(f"Sent {successful}/{len(messages)} messages")

### 反模式

- 立即重试，无退避
- 无抖动导致惊群效应
- 重试非速率限制错误
- 超过 Twilio 的 MPS 限制

## 关键风险点

### 向已退订用户发送消息（错误 21610）

严重程度：高

场景：向电话号码发送短信

症状：
消息失败，错误代码 21610。Twilio 拒绝消息。用户从未收到短信。同一号码之前有效。

原因：
收件人回复了"STOP"（或 UNSUBSCRIBE、CANCEL 等）到您号码的先前消息。Twilio 自动遵守退订并阻止从您的账户向该号码发送更多消息。

这是美国消息传递的法律要求（TCPA、CTIA 指南）。您无法覆盖此设置 - 用户必须回复"START"才能重新订阅。

推荐修复方案：

## 在数据库中跟踪退订状态

```python
# In your webhook handler
@app.route("/webhooks/sms/incoming", methods=["POST"])
def incoming_sms():
    from_number = request.form.get("From")
    body = request.form.get("Body", "").strip().upper()

    # Standard opt-out keywords
    if body in ["STOP", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"]:
        mark_user_opted_out(from_number)
        return "", 200

    # Standard opt-in keywords
    if body in ["START", "SUBSCRIBE", "YES", "UNSTOP"]:
        mark_user_opted_in(from_number)
        return "", 200

    # Process other messages...

# Before sending
def send_sms_safe(to: str, body: str):
    if is_user_opted_out(to):
        return {"success": False, "error": "User has opted out"}

    try:
        return send_sms(to, body)
    except TwilioRestException as e:
        if e.code == 21610:
            # Update database - they opted out via carrier
            mark_user_opted_out(to)
        raise
```

## 包含退订说明
在营销消息中添加"回复 STOP 退订"。

### 电话无法接通但有效（错误 30003）

严重程度：中

场景：向手机号码发送短信

症状：
消息失败，错误 30003。号码有效且之前有效。间歇性 - 有时有效，有时失败。

原因：
错误 30003 表示"目标手机无法接通"。手机存在但目前无法接收消息。常见原因：
- 手机关机
- 飞行模式
- 超出信号范围
- 运营商网络问题
- 手机存储已满

与 30006（永久无法接通）不同，30003 通常是暂时的。

推荐修复方案：

## 为临时故障实施重试逻辑

```python
TRANSIENT_ERRORS = [30003, 30008, 30009]  # Retriable errors

async def send_with_retry(to: str, body: str, max_retries: int = 3):
    for attempt in range(max_retries):
        result = send_sms(to, body)

        if result["success"]:
            return result

        if result.get("error_code") not in TRANSIENT_ERRORS:
            # Don't retry permanent failures
            return result

        # Exponential backoff: 5min, 15min, 45min
        delay = 300 * (3 ** attempt)
        await asyncio.sleep(delay)

    return {"success": False, "error": "Max retries exceeded"}
```

## 提供备用渠道

```python
async def notify_user(user, message):
    # Try SMS first
    result = await send_sms(user.phone, message)

    if result.get("error_code") == 30003:
        # Phone unreachable - try email
        await send_email(user.email, message)
        return {"channel": "email", "status": "sent"}

    return {"channel": "sms", "status": result["status"]}
```

### 消息被运营商过滤阻止

严重程度：高

场景：向美国电话号码发送短信

症状：
消息显示为"已发送"但从未"已传递"。Twilio 无错误。用户表示从未收到消息。特定运营商或消息内容有规律。

原因：
美国运营商（Verizon、AT&T、T-Mobile）积极过滤垃圾短信。如果满足以下条件，您的消息可能被阻止：
- 包含 URL（特别是短 URL 或未知域名）
- 看起来像钓鱼（紧急、账户、验证、立即点击）
- 同一号码大量发送
- 未使用注册的 A2P 10DLC
- 发送者信誉低

运营商不会告诉 Twilio 消息被过滤的原因 - 它们只是静默丢弃。

推荐修复方案：

## 注册 A2P 10DLC（美国要求）

```
1. Go to Twilio Console > Messaging > Trust Hub
2. Register your business brand
3. Create a messaging campaign (describes use case)
4. Wait for approval (can take days)
5. Associate phone numbers with campaign
```

## 消息内容最佳实践

```python
def sanitize_message(text: str) -> str:
    """Make message less likely to be filtered."""
    # Avoid URL shorteners - use full domain
    # Avoid spam trigger words
    # Keep it conversational, not promotional

    # Example: Instead of this
    bad = "URGENT: Verify your account now! Click: bit.ly/abc"

    # Do this
    good = "Hi! Your order #1234 is ready. Questions? Reply here."

    return text

# Use toll-free or short code for high volume
# 10DLC is for <10K msg/day
# Toll-free: up to 10K msg/day
# Short code: 100K+ msg/day
```

## 监控传递率

```python
def track_delivery_rate():
    sent = get_messages_with_status("sent")
    delivered = get_messages_with_status("delivered")

    rate = len(delivered) / len(sent) * 100

    if rate < 95:
        alert_team(f"Delivery rate dropped to {rate}%")
```

### 未验证 Webhook 签名

严重程度：严重

场景：接收 Twilio webhook 回调

症状：
攻击者向您的端点发送虚假 webhook。处理欺诈交易。伪造的来电消息触发操作。

原因：
Twilio 使用 X-Twilio-Signature 头对所有 webhook 请求进行签名。如果您不验证此签名，任何知道您 webhook URL 的人都可以发送伪装成 Twilio 的虚假请求。

这可能导致：
- 虚假消息传递确认
- 伪造的来电消息
- 欺诈性验证批准

推荐修复方案：

## 始终验证签名

```python
from twilio.request_validator import RequestValidator
from flask import Flask, request, abort
from functools import wraps
import os

def require_twilio_signature(f):
    """Decorator to validate Twilio webhook requests."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

        # Full URL including query string
        url = request.url

        # POST body as dict
        params = request.form.to_dict()

        # Signature header
        signature = request.headers.get("X-Twilio-Signature", "")

        if not validator.validate(url, params, signature):
            abort(403)

        return f(*args, **kwargs)
    return wrapper

@app.route("/webhooks/twilio", methods=["POST"])
@require_twilio_signature  # ALWAYS use this
def twilio_webhook():
    # Safe to process
    pass
```

## 常见验证陷阱

```python
# URL must match EXACTLY what Twilio called
# If behind proxy, you might need:
url = request.headers.get("X-Forwarded-Proto", "http") + "://" + \
      request.headers.get("X-Forwarded-Host", request.host) + \
      request.path

# If using ngrok, URL changes each restart
# Use consistent URL in production
```

### WhatsApp 消息超出 24 小时窗口（错误 63016）

严重程度：高

场景：向用户发送 WhatsApp 消息

症状：
消息失败，错误 63016。"消息超出允许的窗口。"模板消息有效，但常规消息失败。

原因：
WhatsApp 对未经请求的消息有严格规则：
- 用户必须先向您发送消息
- 您只能在他们最后一条消息后 24 小时内回复
- 24 小时后，您必须使用预批准的模板消息

这可以防止垃圾邮件并维护 WhatsApp 作为平台的信任度。

推荐修复方案：

## 按用户跟踪会话窗口

```python
from datetime import datetime, timedelta

class WhatsAppSession:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.window_hours = 24

    def start_session(self, phone: str):
        """Start/refresh 24-hour session on incoming message."""
        key = f"wa_session:{phone}"
        expires = datetime.now() + timedelta(hours=self.window_hours)
        self.redis.set(key, expires.isoformat(), ex=self.window_hours * 3600)

    def can_send_freeform(self, phone: str) -> bool:
        """Check if we can send non-template message."""
        key = f"wa_session:{phone}"
        expires_str = self.redis.get(key)

        if not expires_str:
            return False

        expires = datetime.fromisoformat(expires_str)
        return datetime.now() < expires

    def send_message(self, phone: str, body: str, template_sid: str = None):
        """Send message, using template if outside window."""
        if self.can_send_freeform(phone):
            return send_whatsapp_message(phone, body)
        elif template_sid:
            return send_whatsapp_template(phone, template_sid)
        else:
            return {
                "success": False,
                "error": "Outside session window, template required"
            }
```

## 来电消息 webhook

```python
@app.route("/webhooks/whatsapp", methods=["POST"])
def whatsapp_incoming():
    from_phone = request.form.get("From").replace("whatsapp:", "")

    # Start/refresh session
    session.start_session(from_phone)

    # Process message...
```

## 为常见消息创建已批准的模板

```
1. Twilio Console > Content Template Builder
2. Create template with {{1}} placeholders
3. Submit for WhatsApp approval (takes 24-48 hours)
4. Use content_sid to send
```

### 暴露账户 SID 或 Auth Token

严重程度：严重

场景：部署 Twilio 集成

症状：
Twilio 账户出现未经授权的费用。发送了您未发送的消息。未经授权购买了电话号码。

原因：
如果攻击者获取了您的账户 SID + Auth Token，他们可以完全访问您的 Twilio 账户。他们可以：
- 发送消息（向您的账户收费）
- 购买电话号码
- 访问通话录音
- 修改您的配置

常见暴露点：
- 在源代码中硬编码（推送到 GitHub）
- 在客户端 JavaScript 中
- 在 Docker 镜像中
- 在日志中

推荐修复方案：

## 永远不要硬编码凭据

```python
# BAD - never do this
client = Client("AC1234...", "abc123...")

# GOOD - environment variables
client = Client(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_AUTH_TOKEN"]
)

# GOOD - secrets manager
from aws_secretsmanager import get_secret
creds = get_secret("twilio-credentials")
client = Client(creds["sid"], creds["token"])
```

## 使用 API Key 代替 Auth Token

```python
# Auth Token has full account access
# API Keys can be scoped and revoked

# Create API Key in Twilio Console
client = Client(
    os.environ["TWILIO_API_KEY_SID"],
    os.environ["TWILIO_API_KEY_SECRET"],
    os.environ["TWILIO_ACCOUNT_SID"]
)

# If compromised, revoke just that key
```

## 如果暴露，立即轮换令牌

```
1. Twilio Console > Account > API credentials
2. Rotate Auth Token
3. Update all deployments with new token
4. Review account activity for unauthorized use
```

### 验证速率限制超出（错误 60203）

严重程度：中

场景：发送验证码

症状：
验证请求失败，错误 60203。"此电话号码已达到最大发送尝试次数。"

原因：
Twilio Verify 有内置速率限制以防止滥用：
- 每个服务每个电话号码每 10 分钟 5 次验证尝试
- 有助于防止短信泵送欺诈
- 防止暴力破解攻击

如果用户确实需要更多尝试次数，您可能存在用户体验问题。

推荐修复方案：

## 同时实施应用级速率限制

```python
from datetime import datetime, timedelta
import redis

class VerifyRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
        # Stricter than Twilio's limit
        self.max_attempts = 3
        self.window_minutes = 10

    def can_request(self, phone: str) -> bool:
        key = f"verify_rate:{phone}"
        attempts = self.redis.get(key)

        if attempts and int(attempts) >= self.max_attempts:
            return False

        return True

    def record_attempt(self, phone: str):
        key = f"verify_rate:{phone}"
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, self.window_minutes * 60)
        pipe.execute()

    def get_wait_time(self, phone: str) -> int:
        """Return seconds until user can request again."""
        key = f"verify_rate:{phone}"
        ttl = self.redis.ttl(key)
        return max(0, ttl)

# Usage
limiter = VerifyRateLimiter(redis_client)

@app.route("/verify/send", methods=["POST"])
def send_verification():
    phone = request.json["phone"]

    if not limiter.can_request(phone):
        wait = limiter.get_wait_time(phone)
        return {
            "error": f"Too many attempts. Try again in {wait} seconds."
        }, 429

    result = twilio_verify.send_verification(phone)

    if result["success"]:
        limiter.record_attempt(phone)

    return result
```

## 提供清晰的用户反馈

```python
# Show remaining attempts
# Show countdown timer
# Offer alternative (voice call, email)
```

## 验证检查

### 硬编码的 Twilio 凭据

严重程度：错误

Twilio 凭据绝不能硬编码

消息：检测到硬编码的 Twilio SID。使用环境变量。

### 源代码中的 Auth Token

严重程度：错误

Auth Token 应存储在环境变量中

消息：硬编码的 auth token。使用 os.environ['TWILIO_AUTH_TOKEN']。

### 无签名验证的 Webhook

严重程度：错误

Twilio webhooks 必须验证 X-Twilio-Signature

消息：无签名验证的 webhook。添加 RequestValidator 检查。

### 客户端代码中的 Twilio 凭据

严重程度：错误

永远不要向浏览器暴露 Twilio 凭据

消息：Twilio 凭据在客户端暴露。仅在服务器端使用。

### 无 E.164 电话号码验证

严重程度：警告

发送前应验证电话号码

消息：向未经 E.164 验证的电话发送消息。

### 硬编码的电话号码

严重程度：警告

电话号码应来自配置或数据库

消息：硬编码的电话号码。使用配置或环境变量。

### 无 Twilio 异常处理

严重程度：警告

Twilio 调用应处理 TwilioRestException

消息：无错误处理的 Twilio API 调用。捕获 TwilioRestException。

### 未处理特定错误代码

严重程度：信息

专门处理常见的 Twilio 错误代码

消息：考虑处理特定错误代码（21610、30003 等）。

### 无退订关键词处理

严重程度：警告

短信系统必须处理 STOP/UNSUBSCRIBE 关键词

消息：无退订处理。检查 STOP/UNSUBSCRIBE 关键词。

### 发送前未检查退订状态

严重程度：警告

发送短信前检查用户是否已退订

消息：考虑在发送前检查退订状态。

## 协作

### 委派触发器

- 用户需要 AI 语音助手 -> voice-agents（Twilio 提供电话，voice-agents 技能用于 AI 对话）
- 用户需要 Slack 通知 -> slack-bot-builder（将短信警报与 Slack 通知集成）
- 用户需要完整认证系统 -> auth-specialist（Twilio Verify 是更广泛认证的一个组件）
- 用户需要工作流自动化 -> workflow-automation（从自动化工作流触发短信/通话）
- 用户需要高容量消息 -> devops（扩展 webhooks，监控传递率）

## 适用场景
- 用户提及或暗示：twilio
- 用户提及或暗示：发送短信
- 用户提及或暗示：文本消息
- 用户提及或暗示：语音通话
- 用户提及或暗示：电话验证
- 用户提及或暗示：2FA 短信
- 用户提及或暗示：WhatsApp API
- 用户提及或暗示：可编程消息
- 用户提及或暗示：IVR 系统
- 用户提及或暗示：TwiML
- 用户提及或暗示：电话号码验证

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
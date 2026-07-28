import os
from fastapi_mail import FastMail, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME= os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD= os.getenv("MAIL_PASSWORD"),
    MAIL_FROM= os.getenv("MAIL_FROM"),
    MAIL_PORT= os.getenv("MAIL_PORT"),
    MAIL_SERVER= os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME= os.getenv("MAIL_FROM_NAME"),
    USE_CREDENTIALS= os.getenv("USE_CREDENTIALS"),
    VALIDATE_CERTS= os.getenv("VALIDATE_CERTS"),
    MAIL_STARTTLS= os.getenv("MAIL_STARTTLS"),
    MAIL_SSL_TLS= os.getenv("MAIL_SSL_TLS")
)

fast_mail = FastMail(conf)

forgot_password_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,Helvetica,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:40px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="background:#ff6b35;padding:30px;">
                            <h1 style="margin:0;color:#ffffff;">
                                FoodieFreak
                            </h1>
                        </td>
                    </tr>
                    <!-- Body -->
                    <tr>
                        <td style="padding:40px;color:#333333;">
                            <h2 style="margin-top:0;">
                                Reset Your Password
                            </h2>
                            <p>
                                Hello {{name}},
                            </p>
                            <p>
                                We received a request to reset the password for your
                                <strong>FoodieFreak</strong> account.
                            </p>
                            <p>
                                Click the button below to create a new password.
                            </p>
                            <table cellpadding="0" cellspacing="0" align="center" style="margin:35px auto;">
                                <tr>
                                    <td bgcolor="#ff6b35" style="border-radius:6px;">
                                        <a href="{{reset_link}}"
                                           style="
                                           display:inline-block;
                                           padding:15px 35px;
                                           color:#ffffff;
                                           text-decoration:none;
                                           font-size:16px;
                                           font-weight:bold;">
                                            Reset Password
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            <p>
                                This password reset link will expire in
                                <strong>5 minutes</strong>.
                            </p>
                            <p>
                                If you did not request a password reset, you can safely
                                ignore this email. Your password will remain unchanged.
                            </p>
                            <hr style="border:none;border-top:1px solid #eeeeee;margin:30px 0;">
                            <p style="font-size:14px;color:#777777;">
                                If the button above doesn't work, copy and paste the
                                following link into your browser:
                            </p>
                            <p style="word-break:break-all;font-size:13px;color:#555555;">
                                {{reset_link}}
                            </p>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="background:#fafafa;padding:25px;font-size:13px;color:#777777;">
                            <p style="margin:0;">
                                © {{year}} FoodieFreak. All rights reserved.
                            </p>
                            <p style="margin:8px 0 0;">
                                This is an automated email. Please do not reply.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


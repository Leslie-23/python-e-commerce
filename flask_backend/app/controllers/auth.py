import bcrypt
from datetime import datetime, timedelta
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity

from app.models.user import User
from app.models.otp import OTP
from app.models.password_reset_token import PasswordResetToken
from app.utils.sanitize_user import sanitize_user
from app.utils.emails import send_mail
from app.utils.generate_otp import generate_otp


def signup():
    try:
        data = request.get_json()

        # Check if user already exists
        existing_user = User.objects(email=data['email']).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        # Hash password
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode(
            'utf-8')        # Create new user
        new_user = User(**data)
        new_user.save()

        # TODO: Send verification OTP (temporarily disabled for debugging)
        # if not send_verification_otp(new_user):
        #     return jsonify({"message": "Failed to send verification OTP"}), 500
        print(f"✅ User created successfully: {new_user.email}")

        # Generate JWT token
        user_data = sanitize_user(new_user)
        access_token = create_access_token(identity=str(new_user.id))

        # Create response
        response = jsonify(user_data)
        set_access_cookies(response, access_token)

        return response, 201
    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({"message": "Error occurred during signup, please try again later"}), 500


def login():
    try:
        data = request.get_json()

        # Find user by email
        user = User.objects(email=data['email']).first()
        if not user:
            return jsonify({"message": "Invalid email or password"}), 400

        # Check password
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            # Generate JWT token
            return jsonify({"message": "Invalid email or password"}), 400
        user_data = sanitize_user(user)
        access_token = create_access_token(identity=str(user.id))

        # Create response
        response = jsonify(user_data)
        set_access_cookies(response, access_token)

        return response, 200
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({"message": "Error occurred during login, please try again later"}), 500


def logout():
    response = jsonify({"message": "Logged out successfully"})
    unset_jwt_cookies(response)
    return response, 200


def check_auth():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        return jsonify(sanitize_user(user)), 200
    except Exception as e:
        return jsonify({"message": "Authentication failed"}), 401


def send_verification_otp(user):
    try:
        # Generate OTP
        otp_code = generate_otp()

        # Save OTP to database
        OTP(email=user.email, otp=otp_code).save()

        # For development: print OTP to console
        print(f"🔐 OTP for {user.email}: {otp_code}")

        # Try to send email, but don't fail if email service isn't configured
        try:
            email_subject = "Verify your email address"
            email_body = f"""
            <html>
                <body>
                    <h2>Email Verification</h2>
                    <p>Your verification code is: <strong>{otp_code}</strong></p>
                    <p>This code will expire in 10 minutes.</p>
                </body>
            </html>
            """
            send_mail(user.email, email_subject, email_body)
            print(f"📧 Email sent to {user.email}")
        except Exception as email_error:
            print(f"⚠️  Email service not configured: {email_error}")
            print(f"📱 Please use this OTP from console: {otp_code}")

        return True
    except Exception as e:
        print(f"Error sending verification OTP: {e}")
        return False


def verify_otp():
    try:
        data = request.get_json()
        # Frontend sends {otp: otpValue, userId: userId}
        user_id = data.get('userId')
        otp_code = data.get('otp')

        # Find user by ID
        user = User.objects.get(id=user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Find the most recent OTP for this user's email
        otp_record = OTP.objects(email=user.email).order_by(
            '-created_at').first()

        if not otp_record:
            return jsonify({"message": "Invalid OTP"}), 400

        # Check if OTP has expired
        if datetime.utcnow() > otp_record.expires_at:
            return jsonify({"message": "OTP has expired"}), 400

        # Check if OTP matches
        if otp_record.otp != otp_code:
            return jsonify({"message": "Invalid OTP"}), 400

        # Update user's verification status
        user.is_verified = True
        user.save()

        # Delete the used OTP
        otp_record.delete()

        # Return updated user data
        user_data = sanitize_user(user)
        return jsonify(user_data), 200
    except Exception as e:
        print(f"Error in verify_otp: {e}")
        return jsonify({"message": "Error occurred during OTP verification"}), 500


def resend_otp():
    try:
        data = request.get_json()
        user_id = data.get('user')  # Frontend sends {user: userId}

        # Find user by ID
        user = User.objects.get(id=user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Delete any existing OTPs for this user
        OTP.objects(email=user.email).delete()

        # Send new OTP
        if send_verification_otp(user):
            return jsonify({"message": "OTP sent successfully"}), 200
        else:
            return jsonify({"message": "Failed to send OTP"}), 500
    except Exception as e:
        print(f"Error in resend_otp: {e}")
        return jsonify({"message": "Error occurred during OTP resend"}), 500


def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')

        # Find user
        user = User.objects(email=email).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Generate a reset token
        import secrets
        reset_token = secrets.token_urlsafe(32)

        # Save token to database
        PasswordResetToken(email=email, token=reset_token).save()

        # Send password reset email
        reset_url = f"{request.host_url.rstrip('/')}/reset-password?token={reset_token}&email={email}"
        email_subject = "Reset Your Password"
        email_body = f"""
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>Click the link below to reset your password:</p>
                <p><a href="{reset_url}">Reset Password</a></p>
                <p>This link will expire in 1 hour.</p>
                <p>If you didn't request this, please ignore this email.</p>
            </body>
        </html>
        """
        send_mail(user.email, email_subject, email_body)

        return jsonify({"message": "Password reset instructions sent to your email"}), 200
    except Exception as e:
        print(f"Error in forgot_password: {e}")
        return jsonify({"message": "Error occurred during password reset request"}), 500


def reset_password():
    try:
        data = request.get_json()
        email = data.get('email')
        token = data.get('token')
        new_password = data.get('password')

        # Find token
        token_record = PasswordResetToken.objects(
            email=email, token=token).first()
        if not token_record:
            return jsonify({"message": "Invalid or expired reset token"}), 400

        # Check if token has expired
        if datetime.utcnow() > token_record.expires_at:
            return jsonify({"message": "Reset token has expired"}), 400

        # Find user
        user = User.objects(email=email).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Update password
        hashed_password = bcrypt.hashpw(
            new_password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
        user.save()

        # Delete the used token
        token_record.delete()

        return jsonify({"message": "Password reset successfully"}), 200
    except Exception as e:
        print(f"Error in reset_password: {e}")
        return jsonify({"message": "Error occurred during password reset"}), 500

from typing import Dict, Any

"""
Static data functions to simulate a retriever for Payment Reminder System.
Replace with real DB/vector retrieval later.
"""

def get_profile_data():
    return {
        "customer_id": "CUST-00123",
        "name": "Harshith Nalla",
        "email": "harshith.nalla@example.com",
        "phone": "+91-98xxxxxxx",
        "address": "123, Example St, Bangalore, India",
        "member_since": "2021-04-15"
    }

def get_loan_details():
    return {
        "loan_id": "LN-98765",
        "product": "Home Loan",
        "principal": 500000,
        "outstanding_balance": 420000,
        "annual_rate_percent": 7.5,
        "next_emi_date": "2025-10-05",
        "next_emi_amount": 35500,
        "emi_frequency": "Monthly",
        "tenure_months": 240,
        "remaining_tenure_months": 180,
        "last_payment_date": "2025-09-05",
        "payment_history_summary": {
            "on_time_last_6": 5,
            "late_last_6": 1
        }
    }

def update_profile():
    return {
        "note": "User requested to update profile.",
        "allowed_updates": ["phone", "email", "address"],
        "process": "Authenticate -> Provide new details -> Update in system",
        "support": "Contact support if self-update not available"
    }

def make_payment():
    return {
        "note": "User requested to make a payment.",
        "payment_methods": ["UPI", "Net Banking", "Credit Card", "Debit Card"],
        "upi_id": "pay@bank",
        "bank_account": "XXXX-XXXX-1234",
        "instructions": "Select a method and confirm payment securely."
    }

def get_payment_history():
    return {
        "recent_payments": [
            {"date": "2025-09-05", "amount": 35500, "status": "On-time"},
            {"date": "2025-08-05", "amount": 35500, "status": "On-time"},
            {"date": "2025-07-05", "amount": 35500, "status": "Late"},
        ],
        "missed_payments": 1,
        "total_paid": 800000
    }

def payment_action():
    return {
        "note": "User requested scheduling/reminders/auto-pay setup.",
        "options": {
            "schedule_payment": "Set date/time for future payment",
            "auto_debit": "Enable auto-debit from registered account",
            "reminders": "SMS/Email reminders before due date"
        },
        "default_reminder": "2 days before due date"
    }

def get_emi_breakdown():
    return {
        "emi_amount": 35500,
        "principal_component": 25000,
        "interest_component": 10500,
        "next_due_date": "2025-10-05"
    }

def get_due_date_extension_policy():
    return {
        "eligibility": True,
        "max_extension_days": 15,
        "fee_percent": 2,
        "note": "Extension allowed only twice during loan tenure"
    }


def get_prepayment_info():
    return {
        "prepayment_allowed": True,
        "penalty_percent": 3,
        "minimum_amount": 50000,
        "note": "Prepayment reduces outstanding balance and EMI tenure."
    }

def get_partial_payment_policy():
    return {
        "allowed": True,
        "minimum_percent": 50,
        "impact": "Partial payment reduces outstanding balance but EMI date remains same."
    }


def get_account_linking_info():
    return {
        "linked_accounts": ["XXXX-1234 (HDFC)", "XXXX-5678 (SBI)"],
        "supported_modes": ["Bank Transfer", "UPI", "Debit Card"],
        "note": "You can add or remove payment accounts from profile settings."
    }

def get_notification_preferences():
    return {
        "channels": ["SMS", "Email", "Push Notifications"],
        "current_preference": ["SMS", "Email"],
        "note": "You can customize reminders from notification settings."
    }

def get_penalty_waiver_policy():
    return {
        "eligibility": False,
        "note": "Penalty waiver is only available for customers with 12 months of on-time payment history."
    }

def get_topup_loan_info():
    return {
        "eligible": True,
        "max_amount": 200000,
        "interest_rate": 8.0,
        "note": "Top-up loan approval subject to credit check."
    }

def get_general_help():
    return {
        "examples": [
            "How to pay EMI?",
            "How to change registered phone number?",
            "How to update address?"
        ],
        "guidance": "Visit your profile settings or contact support for updates."
    }


def get_human_context():
    return {
        "note": "User explicitly requested human support.",
        "recommended_action": "Connect user to a human agent.",
        "support_channels": {
            "phone": "+91-1800-123-456",
            "email": "support@example.com",
            "chat": "https://example.com/livechat"
        },
        "availability": "24x7 support available"
    }

def reminder_request():
    return {
        "note": "User asked for reminders/notifications.",
        "reminder_methods": ["SMS", "Email", "App Notification"],
        "default_frequency": "Before each EMI",
        "customization": "User can choose reminder time (1 day, 2 days, 1 week before)"
    }

def fee_interest_info():
    return {
        "note": "User requested info about fees/interest/penalties.",
        "interest_rate": "7.5% annual",
        "late_fee_policy": "₹500 flat after 3 days delay",
        "penalty_interest": "2% monthly on overdue amount",
        "grace_period": "3 days"
    }

def security_query():
    return {
        "note": "User requested security/authentication help.",
        "options": [
            "Change password",
            "Forgot password recovery",
            "Verify identity with OTP"
        ],
        "support_contact": "security-support@example.com",
        "guidance": "Always keep credentials safe, never share OTP."
    }

def faq_info_request():
    return {
        "note": "User asked FAQs about the system.",
        "accepted_payment_methods": ["UPI", "Net Banking", "Cards"],
        "emi_calculation": "Based on reducing balance method",
        "support_timings": "24x7 for online, 9am-6pm IST for branches",
        "documentation": "See FAQs at https://example.com/faq"
    }




def get_other():
    return {
        "note": "User query did not match any specific intent.",
        "examples": [
            "weather updates",
            "general chit-chat",
            "unrelated questions"
        ],
        "guidance": "Redirect conversation back to financial services (loan or profile)."
    }



# =================== PAYMENT INTENTS ===================
def make_payment():
    return {
        "status": "success",
        "method": "default",
        "amount": 5000,
        "currency": "INR",
        "message": "Payment processed successfully"
    }

def make_payment_upi():
    return {
        "status": "success",
        "method": "UPI",
        "upi_app": "Google Pay",
        "amount": 5000,
        "currency": "INR",
        "message": "Payment via UPI completed"
    }

def make_payment_netbanking():
    return {
        "status": "success",
        "method": "NetBanking",
        "bank": "HDFC",
        "amount": 5000,
        "currency": "INR",
        "message": "Payment via NetBanking completed"
    }

def make_payment_card():
    return {
        "status": "success",
        "method": "Card",
        "card_type": "Debit",
        "amount": 5000,
        "currency": "INR",
        "message": "Payment via card completed"
    }

def make_payment_cash():
    return {
        "status": "pending",
        "method": "Cash",
        "branch": "Bangalore Main Branch",
        "amount": 5000,
        "currency": "INR",
        "message": "Payment via cash pending"
    }

def schedule_payment():
    return {
        "status": "scheduled",
        "schedule_date": "2025-10-20",
        "amount": 5000,
        "currency": "INR",
        "message": "EMI scheduled successfully"
    }

def not_willing_to_pay():
    return {
        "status": "declined",
        "message": "User chose not to pay"
    }

def reminder_setup():
    return {
        "status": "success",
        "reminder_type": "SMS",
        "time": "09:00 AM",
        "message": "Reminder set for upcoming EMI"
    }

def make_payment_qr():
    return {
        "status": "success",
        "method": "QR",
        "amount": 5000,
        "currency": "INR",
        "message": "Payment via QR code completed"
    }

def schedule_auto_debit():
    return {
        "status": "success",
        "method": "Auto Debit",
        "start_date": "2025-10-18",
        "frequency": "monthly",
        "message": "Auto debit scheduled"
    }

def payment_failed():
    return {
        "status": "failed",
        "reason": "Insufficient funds",
        "message": "Payment could not be processed"
    }

def payment_success():
    return {
        "status": "success",
        "amount": 5000,
        "currency": "INR",
        "message": "Payment completed successfully"
    }

# =================== LOAN / EMI INTENTS ===================
# def get_loan_details():
#     return {
#         "loan_id": "LN-00123",
#         "balance": 150000,
#         "emi": 5000,
#         "due_date": "2025-10-25",
#         "interest_rate": 8.25
#     }

# def get_emi_breakdown():
#     return {
#         "emi": 5000,
#         "principal": 4000,
#         "interest": 1000,
#         "tenure_remaining": 24
#     }

def get_due_date_extension_policy():
    return {
        "policy": "Extension up to 15 days allowed",
        "fee": 200,
        "message": "You can extend due date by 15 days with fee"
    }

def get_partial_payment_policy():
    return {
        "allowed": True,
        "minimum_amount": 2500,
        "message": "Partial payment allowed from 50% of EMI"
    }

def get_topup_loan_info():
    return {
        "eligible": True,
        "max_amount": 50000,
        "interest_rate": 9.0,
        "message": "You are eligible for top-up loan"
    }

def get_prepayment_info():
    return {
        "allowed": True,
        "penalty": 500,
        "message": "Prepayment allowed with penalty of 500 INR"
    }

def loan_status_alert():
    return {
        "alert_enabled": True,
        "next_emi_date": "2025-10-25",
        "message": "EMI alert activated"
    }

def loan_interest_query():
    return {
        "interest_rate": 8.25,
        "message": "Your current loan interest rate is 8.25%"
    }

def loan_penalty_query():
    return {
        "penalty_amount": 200,
        "message": "Late payment penalty is 200 INR"
    }

# =================== PROFILE / ACCOUNT INTENTS ===================
# def get_profile_data():
#     return {
#         "customer_id": "CUST-00123",
#         "name": "Harshith Nalla",
#         "email": "harshith.nalla@example.com",
#         "phone": "+91-98xxxxxxx",
#         "address": "123, Example St, Bangalore, India",
#         "member_since": "2021-04-15"
#     }

def update_email():
    return {
        "status": "success",
        "updated_field": "email",
        "new_value": "new_email@example.com"
    }

def update_phone():
    return {
        "status": "success",
        "updated_field": "phone",
        "new_value": "+91-9876543210"
    }

def update_address():
    return {
        "status": "success",
        "updated_field": "address",
        "new_value": "456, New Address, Bangalore, India"
    }

def link_bank_account():
    return {
        "status": "success",
        "account_number": "XXXX1234",
        "bank": "HDFC",
        "message": "Bank account linked successfully"
    }

def unlink_bank_account():
    return {
        "status": "success",
        "account_number": "XXXX1234",
        "bank": "HDFC",
        "message": "Bank account unlinked successfully"
    }

def security_password_reset():
    return {
        "status": "success",
        "message": "Password reset link sent to registered email"
    }

def security_otp_issue():
    return {
        "status": "pending",
        "message": "OTP issue reported, please try again"
    }

def update_name():
    return {
        "status": "success",
        "updated_field": "name",
        "new_value": "Harshith Kumar"
    }

def update_kyc():
    return {
        "status": "success",
        "updated_field": "KYC",
        "message": "KYC details updated successfully"
    }

def update_password():
    return {
        "status": "success",
        "message": "Password updated successfully"
    }

# =================== HUMAN / SUPPORT INTENTS ===================
def get_human_context():
    return {
        "status": "pending",
        "message": "Request forwarded to human agent"
    }

def get_general_help():
    return {
        "status": "success",
        "message": "Here is the guide for your request"
    }

def faq_info_request():
    return {
        "status": "success",
        "faqs": [
            "How to pay EMI?",
            "Penalty rules",
            "Loan extension options"
        ]
    }

def complaint_register():
    return {
        "status": "success",
        "message": "Your complaint has been registered",
        "ticket_id": "CMP-00123"
    }

def feedback_submission():
    return {
        "status": "success",
        "message": "Thank you for your feedback"
    }

def technical_support():
    return {
        "status": "pending",
        "message": "Technical support team notified"
    }

# =================== CONFIRMATION / DENIAL ===================
def handle_yes_or_no():
    return {
        "status": "success",
        "message": "Confirmation / Denial registered"
    }

# =================== OTHER / SMALL TALK ===================
def get_other():
    return {
        "status": "success",
        "message": "This is a generic response"
    }
          

user_context = {"awaiting_confirmation": False, "last_action": None}

def handle_not_willing_to_pay(user_input: str) -> str:
    user_context["awaiting_confirmation"] = True
    user_context["last_action"] = "not_willing_to_pay"
    return "Are you sure you don't want to make the payment?"

def handle_yes_or_no(user_input: str) -> str:
    if user_context["awaiting_confirmation"]:
        if "yes" in user_input.lower():
            ...
    return "Could you please clarify that?"
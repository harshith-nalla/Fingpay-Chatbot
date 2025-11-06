import re
from statistics import mean
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.static_data import (
    get_profile_data, get_loan_details, get_human_context, get_other,
    update_profile, make_payment, get_payment_history, payment_action,
    get_emi_breakdown, get_due_date_extension_policy, get_prepayment_info,
    get_partial_payment_policy, get_account_linking_info,
    get_notification_preferences, get_penalty_waiver_policy,
    get_topup_loan_info, get_general_help, reminder_request,
    fee_interest_info, security_query, faq_info_request, handle_yes_or_no
)


class IntentClassifier:
    """
    Cosine Similarity + TF-IDF based lightweight intent classifier.
    Fallback to RAG retrieval if no strong intent is found.
    """

    def __init__(self):
        self.intents = {
           "make_payment_upi": {
        "examples": [
            "Pay via UPI",
            "Use Google Pay",
            "Send payment through UPI"
        ],
        "keywords": ["upi", "google pay", "phonepe", "paytm", "payment"],
        "handler": make_payment
    },
    "make_payment_netbanking": {
        "examples": [
            "Pay via net banking",
            "Use my bank portal to pay",
            "Transfer EMI online"
        ],
        "keywords": ["net banking", "bank transfer", "payment"],
        "handler": make_payment
    },
    "make_payment_card": {
        "examples": [
            "Pay using debit card",
            "Pay via credit card",
            "Use card to pay EMI"
        ],
        "keywords": ["debit card", "credit card", "card payment"],
        "handler": make_payment
    },
    "make_payment_cash": {
        "examples": [
            "Pay cash at branch",
            "I’ll pay in cash",
            "Offline payment for EMI"
        ],
        "keywords": ["cash", "branch", "offline payment"],
        "handler": make_payment
    },
    "schedule_payment": {
        "examples": [
            "Set EMI for tomorrow",
            "Pay next week automatically",
            "Schedule EMI payment"
        ],
        "keywords": ["schedule", "remind", "auto pay"],
        "handler": payment_action
    },
    "not_willing_to_pay": {
        "examples": [
            "I can't pay today",
            "I don’t want to pay",
            "I will not pay this month",
            "I’ll skip this payment"
        ],
        "keywords": ["not pay", "don’t want", "skip payment", "later"],
        "handler": payment_action
    },
    "reminder_setup": {
        "examples": [
            "Remind me before EMI",
            "Set SMS reminder",
            "Notify me about payment"
        ],
        "keywords": ["remind", "notification", "alert"],
        "handler": reminder_request
    },
    "make_payment_qr": {
    "examples": [
        "I want to make payment using QR code",
        "Provide QR code",
        "I will scan QR to complete payment",
        "I will se QR payment"
    ],
    "keywords": ["qr", "scan", "payment"],
    "handler": make_payment
},
"schedule_auto_debit": {
    "examples": [
        "Set up auto debit",
        "Automatically pay EMI every month",
        "Recurring payment setup"
    ],
    "keywords": ["auto debit", "recurring", "automatic"],
    "handler": payment_action
},
# "payment_failed": {
#     "examples": [
#         "Payment didn’t go through",
#         "EMI payment failed",
#         "Transaction failed"
#     ],
#     "keywords": ["failed", "error", "issue"],
#     "handler": payment_action
# },
"payment_success": {
    "examples": [
        "Payment completed",
        "EMI paid successfully",
        "Transaction successful"
    ],
    "keywords": ["success", "completed", "done"],
    "handler": payment_action
},

    # =================== LOAN / EMI INTENTS ===================
    "loan_balance": {
        "examples": [
            "Tell me my loan status",
            "What is the outstanding balance?",
            "Loan details"
        ],
        "keywords": ["loan", "balance", "outstanding"],
        "handler": get_loan_details
    },
    "emi_breakdown": {
        "examples": [
            "Show EMI split",
            "Principal and interest",
            "EMI breakdown"
        ],
        "keywords": ["emi", "breakdown", "principal", "interest", "split"],
        "handler": get_emi_breakdown
    },
    "request_extension": {
        "examples": [
            "Can I extend my due date?",
            "Delay my EMI",
            "Request extension"
        ],
        "keywords": ["extend", "delay", "extension"],
        "handler": get_due_date_extension_policy
    },
    "request_partial_payment": {
        "examples": [
            "Can I pay half EMI?",
            "Partial repayment",
            "Make partial payment"
        ],
        "keywords": ["partial", "half", "installment"],
        "handler": get_partial_payment_policy
    },
    "topup_loan_request": {
        "examples": [
            "Can I get a top-up loan?",
            "Increase my loan amount",
            "Eligibility for top-up"
        ],
        "keywords": ["topup", "extra loan", "increase loan"],
        "handler": get_topup_loan_info
    },
    "prepayment_request": {
        "examples": [
            "I want to prepay my loan",
            "Pay off early",
            "Prepayment rules"
        ],
        "keywords": ["prepay", "early closure", "penalty"],
        "handler": get_prepayment_info
    },

    "loan_status_alert": {
    "examples": [
        "Alert me if my EMI is due",
        "Notify about upcoming EMI"
    ],
    "keywords": ["alert", "notification", "emi due"],
    "handler": reminder_request
},
"loan_interest_query": {
    "examples": [
        "What is my interest rate?",
        "Current rate for my loan",
        "Interest on my EMI"
    ],
    "keywords": ["interest", "rate", "loan"],
    "handler": fee_interest_info
},
"loan_penalty_query": {
    "examples": [
        "How much is the late fee?",
        "Penalty for delayed EMI"
    ],
    "keywords": ["penalty", "late fee", "charges"],
    "handler": fee_interest_info
},

    # =================== PROFILE / ACCOUNT INTENTS ===================
    "view_profile": {
        "examples": [
            "Show my profile",
            "Get my account details",
            "Check my registered info"
        ],
        "keywords": ["profile", "account", "details"],
        "handler": get_profile_data
    },
    "update_email": {
        "examples": [
            "Change my email",
            "Update registered email"
        ],
        "keywords": ["email", "update", "change"],
        "handler": update_profile
    },
    "update_phone": {
        "examples": [
            "Change my phone number",
            "Update registered mobile"
        ],
        "keywords": ["phone", "mobile", "update", "change"],
        "handler": update_profile
    },
    "update_address": {
        "examples": [
            "Update my address",
            "Change my current address"
        ],
        "keywords": ["address", "update", "change"],
        "handler": update_profile
    },
    "link_bank_account": {
        "examples": [
            "Add new bank account",
            "Link my account"
        ],
        "keywords": ["link", "bank", "account"],
        "handler": get_account_linking_info
    },
    "unlink_bank_account": {
        "examples": [
            "Remove my bank account",
            "Unlink account"
        ],
        "keywords": ["unlink", "bank", "account"],
        "handler": get_account_linking_info
    },
    "security_password_reset": {
        "examples": [
            "Forgot password",
            "Reset password"
        ],
        "keywords": ["password", "reset", "forgot"],
        "handler": security_query
    },
    "security_otp_issue": {
        "examples": [
            "OTP not received",
            "Issue with OTP"
        ],
        "keywords": ["otp", "issue", "code"],
        "handler": security_query
    },

    "update_name": {
    "examples": [
        "Change my registered name",
        "Update account name"
    ],
    "keywords": ["name", "update", "change"],
    "handler": update_profile
},
"update_kyc": {
    "examples": [
        "Update my KYC details",
        "Change ID proof"
    ],
    "keywords": ["kyc", "id", "update"],
    "handler": update_profile
},
"update_password": {
    "examples": [
        "Change my password",
        "Update login password"
    ],
    "keywords": ["password", "change", "update"],
    "handler": security_query
},

    # =================== HUMAN / SUPPORT INTENTS ===================
    "talk_to_agent": {
        "examples": [
            "I want to talk to a human",
            "Connect me to support",
            "Speak to agent"
        ],
        "keywords": ["agent", "human", "representative", "support"],
        "handler": get_human_context
    },
    "general_help_payment": {
        "examples": [
            "How to pay EMI?",
            "Guide me to pay EMI"
        ],
        "keywords": ["help", "guide", "payment"],
        "handler": get_general_help
    },
    "general_help_account": {
        "examples": [
            "How to update my number?",
            "How to change address?"
        ],
        "keywords": ["help", "guide", "account"],
        "handler": get_general_help
    },
    "faq_info": {
        "examples": [
            "Show FAQ",
            "Support timings?",
            "Frequently asked questions"
        ],
        "keywords": ["faq", "questions", "support"],
        "handler": faq_info_request
    },

    "complaint_register": {
    "examples": [
        "I want to lodge a complaint",
        "File a complaint regarding EMI"
    ],
    "keywords": ["complaint", "issue", "problem"],
    "handler": get_human_context
},
"feedback_submission": {
    "examples": [
        "Submit feedback",
        "Provide my feedback"
    ],
    "keywords": ["feedback", "review", "rate"],
    "handler": get_human_context
},
"technical_support": {
    "examples": [
        "I am facing technical issues",
        "Support for app login",
        "App not working"
    ],
    "keywords": ["technical", "issue", "support", "app"],
    "handler": get_human_context
},

    # =================== CONFIRMATION / DENIAL ===================
    "affirm": {
        "examples": ["yes", "yeah", "yep", "sure", "of course"],
        "keywords": ["yes", "yeah", "yep", "sure"],
        "handler": handle_yes_or_no
    },
    "deny": {
        "examples": ["no", "nope", "not really", "nah"],
        "keywords": ["no", "nope", "nah"],
        "handler": handle_yes_or_no
    },

    "greeting": {
    "examples": ["hello", "hi", "good morning", "good evening"],
    "keywords": ["hello", "hi", "hey", "greetings"],
    "handler": get_other
},
"thanks": {
    "examples": ["thanks", "thank you", "thx", "much appreciated"],
    "keywords": ["thanks", "thank", "thx"],
    "handler": get_other
},
"small_talk": {
    "examples": ["How are you?", "What's up?", "Tell me a joke"],
    "keywords": ["how", "joke", "weather", "chat"],
    "handler": get_other
},

"human_context": {
    "examples": [
        "how are you",
        "what's up",
        "who made you",
        "hello",
        "good morning"
    ],
    "keywords": ["hi", "hello", "hey", "good morning", "good evening"],
    "handler": get_human_context
},


    "other": {
        "examples": ["hello", "thanks", "what's the weather", "random chit-chat"],
        "keywords": [],
        "handler": get_other
    }

        }

        self.MAX_SCORE_THRESHOLD = 0.60
        self.BEST_SCORE_THRESHOLD = 0.50
        self.AMBIGUITY_DELTA = 0.08
        self.ACCOUNT_RE = re.compile(r"\b(?:acc(?:ount)?\s*:?\s*)?(\d{4,12})\b")

    def _cosine_similarity(self, text, examples):
        corpus = [text] + examples
        vectorizer = TfidfVectorizer().fit(corpus)
        tfidf_matrix = vectorizer.transform(corpus)
        sim_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        return sim_scores

    def classify(self, text):
        text_norm = " ".join(text.lower().split())
        results = {}

        print("\n[Classifier] -----------------------------")
        print(f"[Classifier] Input text: {text_norm}")

        # direct keyword check for human context
        for kw in self.intents["human_context"]["keywords"]:
            if kw in text_norm:
                print(f"[Classifier] Matched human keyword '{kw}' → intent=human_context")
                handler_func = self.intents["human_context"]["handler"]
                return {"chosen_intent": "human_context", "confidence": 1.0, "handler": handler_func}

        # compute cosine similarity for each intent
        for intent_name, intent_meta in self.intents.items():
            scores = self._cosine_similarity(text_norm, intent_meta["examples"])
            max_example = max(scores) if len(scores) else 0.0
            avg_example = mean(scores) if len(scores) else 0.0

            keywords = intent_meta.get("keywords", [])
            if keywords:
                present = sum(1 for kw in keywords if kw in text_norm)
                keyword_score = present / len(keywords)
            else:
                keyword_score = 0.0

            final_score = 0.7 * max_example + 0.2 * avg_example + 0.1 * keyword_score

            results[intent_name] = {
                "max_example_score": max_example,
                "avg_example_score": avg_example,
                "keyword_score": keyword_score,
                "final_score": final_score
            }

            print(f"[Classifier] Intent '{intent_name}': "
                  f"max={max_example:.3f}, avg={avg_example:.3f}, "
                  f"kw={keyword_score:.3f}, final={final_score:.3f}")

        ranked = sorted(results.items(), key=lambda kv: kv[1]["final_score"], reverse=True)
        top_name, top_stats = ranked[0]
        second_name, second_stats = ranked[1] if len(ranked) > 1 else (None, {"final_score": 0.0})

        print(f"[Classifier] Top candidate: {top_name} (score={top_stats['final_score']:.3f})")
        if second_name:
            print(f"[Classifier] 2nd candidate: {second_name} (score={second_stats['final_score']:.3f})")

        if (top_stats["max_example_score"] >= self.MAX_SCORE_THRESHOLD) or \
           (top_stats["avg_example_score"] >= self.BEST_SCORE_THRESHOLD):
            if (top_stats["final_score"] - second_stats["final_score"]) < self.AMBIGUITY_DELTA:
                chosen = "other"
                handler_func = self.intents["other"]["handler"]
                print("[Classifier] Ambiguity detected → defaulting to 'other'")
            else:
                chosen = top_name
                handler_func = self.intents[top_name]["handler"]
                print(f"[Classifier] Chosen intent: {chosen}")
        else:
            chosen = "other"
            handler_func = self.intents["other"]["handler"]
            print("[Classifier] No strong match → fallback to 'other'")
        print("The handler function is :",handler_func)
        return {"chosen_intent": chosen, "confidence": top_stats["final_score"], "handler": handler_func}


    # ------------------- HANDLERS -------------------

    # def handle_loan_details(self, text):
    #     return {"loan_status": "Active", "outstanding": "₹25,000", "next_emi": "2025-10-10"}

    # def handle_profile_data(self, text):
    #     return {"name": "Harshith Nalla", "email": "harshith@example.com", "phone": "+91-9876543210"}

    # def handle_human_context(self, text):
    #     return "Connecting you to a human representative..."

    # def handle_other(self, text):
    #     if any(w in text.lower() for w in ["hello", "hi", "hey"]):
    #         return "Hi!"
    #     if "thanks" in text.lower():
    #         return "You're welcome."
    #     return "Okay."

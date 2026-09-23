from pathlib import Path
import csv
import random

ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "datasets"

DATASET_DIR.mkdir(exist_ok=True)

random.seed(42)

# ============================================================
# TOXICITY DATA
# ============================================================

toxic_messages = [
    "You are stupid",
    "You are an idiot",
    "You are useless",
    "Nobody likes you",
    "I hate you",
    "Shut up",
    "You are completely annoying",
    "You are a terrible person",
    "Stop bothering me",
    "You have no idea what you are doing",
    "This is the dumbest thing ever",
    "You are so rude",
    "Go away",
    "You are worthless",
    "I cannot stand you",
]

normal_messages = [
    "Thank you for your help",
    "Have a wonderful day",
    "Can you help me with this project?",
    "Please send me the report",
    "The meeting is scheduled for tomorrow",
    "I appreciate your support",
    "Your project looks good",
    "Please review this document",
    "Can you explain this topic?",
    "The assignment deadline is Friday",
    "Let us discuss the project",
    "Please share the notes",
    "I agree with your suggestion",
    "The class starts at ten AM",
    "Thank you for explaining this",
]

toxicity_path = DATASET_DIR / "toxicity.csv"

with toxicity_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "id",
        "text",
        "label"
    ])

    row_id = 1

    # 600 toxic + 600 normal
    for _ in range(600):

        text = random.choice(
            toxic_messages
        )

        writer.writerow([
            row_id,
            text,
            1
        ])

        row_id += 1

    for _ in range(600):

        text = random.choice(
            normal_messages
        )

        writer.writerow([
            row_id,
            text,
            0
        ])

        row_id += 1


# ============================================================
# CYBER THREAT DATA
# ============================================================

phishing_messages = [
    "Your account will be blocked. Verify your password immediately.",
    "Urgent account verification is required.",
    "Click the link to verify your account.",
    "Your bank account needs urgent verification.",
    "Confirm your login credentials now.",
    "Your account security check is pending.",
    "Verify your account immediately using the provided link.",
    "Your online account will be suspended unless verified.",
]

scam_messages = [
    "Congratulations, you won a prize.",
    "You have won a lottery prize.",
    "Claim your reward by clicking the link.",
    "You are selected for a special cash reward.",
    "Congratulations, you have won a free gift.",
    "Pay a small fee to receive your prize.",
    "You have been selected for a reward.",
    "Claim your unexpected bonus today.",
]

credential_messages = [
    "Send me your OTP to confirm the transaction.",
    "Please provide your password for verification.",
    "Share your login credentials immediately.",
    "Send the authentication code to confirm your account.",
    "Provide your OTP to complete verification.",
    "Tell me your account password.",
    "Share your security code now.",
    "Give me your login details for verification.",
]

malware_messages = [
    "Download this unknown attachment to unlock your account.",
    "Install this file to receive your update.",
    "Open the attached executable immediately.",
    "Download this suspicious application.",
    "Run the attached file to fix your computer.",
    "Install this unknown software to continue.",
    "Open this unexpected executable attachment.",
    "Download the attached program now.",
]

normal_messages = [
    "Please attend the project meeting at 10 AM.",
    "The assignment deadline is Friday.",
    "Can you share the project report?",
    "Your appointment is scheduled for tomorrow.",
    "Please review the attached project document.",
    "The college seminar starts at 11 AM.",
    "Can you send me the class notes?",
    "The team meeting will start after lunch.",
    "Please submit your assignment before Friday.",
    "The project presentation is next week.",
]

threat_path = DATASET_DIR / "cyber_threat.csv"

with threat_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "id",
        "text",
        "threat",
        "category"
    ])

    row_id = 1

    categories = [
        (phishing_messages, "phishing"),
        (scam_messages, "scam"),
        (credential_messages, "credential_theft"),
        (malware_messages, "malware"),
    ]

    # 250 examples for each threat category
    for messages, category in categories:

        for _ in range(250):

            text = random.choice(
                messages
            )

            writer.writerow([
                row_id,
                text,
                1,
                category
            ])

            row_id += 1

    # 1000 normal examples
    for _ in range(1000):

        text = random.choice(
            normal_messages
        )

        writer.writerow([
            row_id,
            text,
            0,
            "normal"
        ])

        row_id += 1


print()
print("=" * 60)
print("NLPShield datasets created successfully")
print("=" * 60)
print()
print("Toxicity dataset:")
print(toxicity_path)
print("Rows: 1200")
print()
print("Cyber threat dataset:")
print(threat_path)
print("Rows: 2000")
print()

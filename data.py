"""Mock data for the Solace prototype: lessons, scenarios, leaderboard.

Everything here is demo/seed data standing in for what would eventually come
from open-banking data, a CMS, and a real user database.
"""

# --- Detect layer: questionnaire -> derived tags ------------------------

QUESTIONNAIRE = [
    {
        "id": "income",
        "question": "How does money mostly come in?",
        "options": [
            ("steady", "One regular payslip"),
            ("mixed", "A mix of jobs / gig work"),
            ("irregular", "Irregular — loans, family, occasional work"),
        ],
    },
    {
        "id": "buffer",
        "question": "If your card was declined tomorrow, what would you do?",
        "options": [
            ("buffer", "Move money from savings — no big deal"),
            ("thin", "Scrape by until payday"),
            ("none", "I don't have a plan for this"),
        ],
    },
    {
        "id": "credit",
        "question": "What's your relationship with credit right now?",
        "options": [
            ("none", "Never used a credit card or BNPL"),
            ("light", "Used BNPL once or twice"),
            ("active", "I use BNPL or a credit card regularly"),
        ],
    },
    {
        "id": "goal",
        "question": "What's on your mind most right now?",
        "options": [
            ("save", "Building any kind of savings"),
            ("debt", "Getting on top of what I owe"),
            ("grow", "Starting to invest or grow money"),
        ],
    },
]

# maps (question_id, answer_value) -> tag shown back to the user
TAG_RULES = {
    ("income", "irregular"): "Irregular income",
    ("income", "mixed"): "Multiple income sources",
    ("buffer", "thin"): "Thin savings buffer",
    ("buffer", "none"): "No savings buffer",
    ("credit", "light"): "New to credit",
    ("credit", "active"): "Active BNPL/credit use",
    ("goal", "save"): "Focused on saving",
    ("goal", "debt"): "Managing debt",
    ("goal", "grow"): "Ready to invest",
}

# --- Learn layer ----------------------------------------------------------

LESSONS = [
    {
        "id": "apr",
        "title": "APR vs. interest rate",
        "minutes": 4,
        "tags": ["Active BNPL/credit use", "New to credit"],
        "summary": "The number on the advert is never the number you pay. Here's the gap, and why it matters.",
        "body": [
            "The 'interest rate' is the cost of borrowing for a year, before fees. "
            "APR (Annual Percentage Rate) rolls in the fees too — it's the number that actually tells you what "
            "a card or loan costs.",
            "A card advertised at '19.9% representative APR' doesn't mean you'll get 19.9% — 'representative' "
            "means at least 51% of accepted applicants get that rate or better. Yours could be higher.",
            "Rule of thumb: compare APRs, not interest rates, when you're shopping around — and always read what "
            "'representative' is doing in that sentence.",
        ],
        "reviewed_by": "Reviewed with a credit union economist",
    },
    {
        "id": "buffer",
        "title": "Why a small buffer beats a big plan",
        "minutes": 3,
        "tags": ["Thin savings buffer", "No savings buffer", "Irregular income"],
        "summary": "£200 sitting still stops more financial damage than any spreadsheet will.",
        "body": [
            "Most financial stress isn't caused by not earning enough — it's caused by one unplanned cost hitting "
            "a £0 balance and cascading into overdraft fees, missed payments, or high-interest borrowing.",
            "A starter buffer of even £100-£200, kept separate from your spending money, breaks that cascade. "
            "It doesn't need to be 3-6 months of expenses to be useful — it needs to exist.",
            "If income is irregular, treat the buffer as priority #1 before extra repayments or investing — it's "
            "what keeps a bad week from becoming a bad year.",
        ],
        "reviewed_by": "Reviewed with a credit union economist",
    },
    {
        "id": "bnpl",
        "title": "How Buy Now Pay Later actually works",
        "minutes": 4,
        "tags": ["Active BNPL/credit use", "Managing debt"],
        "summary": "It's marketed as a payment method. It behaves like a loan. Here's the difference.",
        "body": [
            "BNPL splits a purchase into instalments with no interest — as long as you pay on time. Miss one, "
            "and most providers add fees, and some report missed payments to credit reference agencies.",
            "Because it's split across several purchases and providers, it's easy to lose track of how much is "
            "actually committed each month until several instalments land in the same week.",
            "A simple habit: before checking out with BNPL, write down the next payment date next to your existing "
            "bills — not just in the app's own list.",
        ],
        "reviewed_by": "Reviewed with a credit union economist",
    },
    {
        "id": "compound",
        "title": "Compound growth, honestly explained",
        "minutes": 5,
        "tags": ["Ready to invest", "Focused on saving"],
        "summary": "Why starting at 19 beats starting at 29, even with less money.",
        "body": [
            "Compound growth means your returns start earning their own returns. The effect is small in year one "
            "and large after year ten — which is why the biggest single factor in most outcomes is start date, "
            "not amount invested.",
            "£50/month from 19 can outgrow £100/month started at 29, purely from extra time in the market.",
            "This isn't a reason to rush into risk you don't understand — it's a reason to start something small "
            "and low-risk now rather than wait for a 'better' amount later.",
        ],
        "reviewed_by": "Reviewed with a regulated investment adviser",
    },
    {
        "id": "credit-score",
        "title": "What actually builds a credit file",
        "minutes": 3,
        "tags": ["New to credit", "Managing debt"],
        "summary": "Not having debt isn't the same as having a good credit file.",
        "body": [
            "A 'thin file' — little to no borrowing history — can make it harder to get a mortgage or phone "
            "contract later, even with perfect money management otherwise.",
            "A small, fully-repaid credit commitment (a low-limit card, used lightly and paid off in full every "
            "month) is one of the most common ways to build a track record safely.",
            "The single biggest factor in most scoring models is payment history — paying on time, every time, "
            "matters more than the amount borrowed.",
        ],
        "reviewed_by": "Reviewed with a credit union economist",
    },
]

# --- Practice layer: scenario simulator -----------------------------------

SCENARIOS = [
    {
        "id": "rent-vs-card",
        "tags": ["Thin savings buffer", "No savings buffer", "Irregular income"],
        "prompt": "Your rent (£420) is due Friday. Your card minimum payment (£35) is due Monday. "
                  "Your balance today covers one of them comfortably, not both.",
        "options": [
            {
                "id": "a",
                "text": "Pay rent in full, pay only the card minimum late",
                "outcome": "good",
                "feedback": "Rent is the higher-consequence bill — missing it risks your home. A few days late "
                            "on a card minimum usually means a fee, not a default, as long as it's paid within "
                            "the grace period most providers allow.",
            },
            {
                "id": "b",
                "text": "Pay the card in full, ask your landlord for 3 extra days on rent",
                "outcome": "okay",
                "feedback": "Reasonable if your landlord is flexible — but this only works if you actually ask "
                            "before the due date, not after. Silence is what damages the relationship, not lateness.",
            },
            {
                "id": "c",
                "text": "Split both payments and dip into your overdraft",
                "outcome": "poor",
                "feedback": "This is the most expensive option — overdraft fees on top of two partial payments, "
                            "and neither bill is actually cleared. It feels like progress but usually costs more "
                            "than picking one bill and paying it properly.",
            },
        ],
    },
    {
        "id": "bnpl-stack",
        "tags": ["Active BNPL/credit use"],
        "prompt": "You've got 3 BNPL plans running (£18, £24, £40 a month). A 4th purchase would add another £15/month. "
                  "You can technically afford it this month.",
        "options": [
            {
                "id": "a",
                "text": "Go ahead — this month's budget covers it",
                "outcome": "poor",
                "feedback": "This is how BNPL stacking sneaks up on people — each plan is affordable alone, but "
                            "four plans landing in different weeks is much easier to lose track of than one bill.",
            },
            {
                "id": "b",
                "text": "Check all 4 payment dates against your bills before deciding",
                "outcome": "good",
                "feedback": "This is the habit that actually prevents BNPL problems — not avoiding it altogether, "
                            "but always seeing the full committed total in one place before adding to it.",
            },
            {
                "id": "c",
                "text": "Skip it and pay in full instead",
                "outcome": "okay",
                "feedback": "Avoids the stacking risk entirely, but only works if you actually have the cash — "
                            "otherwise you've just moved the strain somewhere less visible.",
            },
        ],
    },
    {
        "id": "first-investment",
        "tags": ["Ready to invest", "Focused on saving"],
        "prompt": "You've got £500 spare. A friend says to put it all into a single trending stock they've made money on.",
        "options": [
            {
                "id": "a",
                "text": "Put it all in — they've had good returns",
                "outcome": "poor",
                "feedback": "One person's result isn't evidence of a good strategy — it's a single data point. "
                            "Concentrating everything in one stock is one of the highest-risk ways to invest.",
            },
            {
                "id": "b",
                "text": "Make sure there's a savings buffer first, then consider a diversified option",
                "outcome": "good",
                "feedback": "Buffer before investing, and diversified before concentrated — in that order, this is "
                            "close to what most regulated advisers would actually recommend for a first £500.",
            },
            {
                "id": "c",
                "text": "Keep it all in cash savings instead",
                "outcome": "okay",
                "feedback": "Safe, but if a buffer already exists, cash sitting long-term loses value to inflation — "
                            "this is a reasonable step one, not a permanent plan.",
            },
        ],
    },
]

# --- Reward layer -----------------------------------------------------

POINTS_PER_LESSON = 15
POINTS_PER_SCENARIO = 20
CHECKIN_POINTS = 5
TOPUP_THRESHOLD = 100  # points needed to unlock a cash top-up
TOPUP_AMOUNT_GBP = 2

# --- Social layer (mock) -----------------------------------------------

LEADERBOARD = [
    {"name": "Amara", "streak": 12, "you": False},
    {"name": "Marcus", "streak": 9, "you": False},
    {"name": "Jess", "streak": 7, "you": False},
    {"name": "Priya", "streak": 5, "you": False},
]


def tags_for_answers(answers: dict) -> list:
    """Turn raw questionnaire answers into human-readable profile tags."""
    tags = []
    for qid, value in answers.items():
        tag = TAG_RULES.get((qid, value))
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def relevant(items: list, tags: list) -> list:
    """Sort items so ones matching the user's tags come first."""
    def score(item):
        return -len(set(item.get("tags", [])) & set(tags))
    return sorted(items, key=score)

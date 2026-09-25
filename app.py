import streamlit as st
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



#page configuration 
st.set_page_config(
    page_title="CyberSift",
    page_icon="🛡️",
    layout="centered"
)


#load dataset

@st.cache_data
def load_data():

    df = pd.read_csv(
        "sms.tsv",
        sep="\t",
        header=None,
        names=["label", "message"]
    )

    return df


df = load_data()


#data preprocessing

df["label"] = df["label"].map({
    "ham": 0,
    "spam": 1
})

df = df.dropna()


#model train
@st.cache_resource
def train_model():

    X = df["message"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                max_features=10000
            )
        ),
        (
            "naive_bayes",
            MultinomialNB()
        )
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    return model, accuracy


model, accuracy = train_model()



#cybersecurity rule engine
def security_analysis(message):

    message_lower = message.lower()

    score = 0
    indicators = []

    #urgency detection
    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "hurry",
        "limited time",
        "final warning",
        "account will be blocked"
    ]

    for word in urgency_words:

        if word in message_lower:

            score += 10

            indicators.append(
                f"Urgency detected: '{word}'"
            )


    #financial keywords

    financial_words = [
        "bank",
        "account",
        "payment",
        "money",
        "cash",
        "refund",
        "loan",
        "credit card",
        "debit card"
    ]

    for word in financial_words:

        if word in message_lower:

            score += 10

            indicators.append(
                f"Financial keyword detected: '{word}'"
            )


    #crediantials requests
    credential_words = [
        "password",
        "otp",
        "pin",
        "cvv",
        "verification code",
        "login",
        "username"
    ]

    for word in credential_words:

        if word in message_lower:

            score += 20

            indicators.append(
                f"Credential-related keyword: '{word}'"
            )


    #suspicious links

    url_pattern = r"https?://\S+|www\.\S+"

    urls = re.findall(
        url_pattern,
        message
    )

    if urls:

        score += 20

        indicators.append(
            f"Suspicious link detected ({len(urls)} URL)"
        )


     # prize/reward scam patterns
    prize_words = [
        "winner",
        "won",
        "lottery",
        "prize",
        "reward",
        "free gift",
        "congratulations"
    ]

    for word in prize_words:

        if word in message_lower:

            score += 15

            indicators.append(
                f"Prize/reward pattern: '{word}'"
            )


    return min(score, 100), indicators


#risk classification 

def calculate_risk(spam_probability, security_score):


    # Combine ML probability and cybersecurity score
    final_score = (
        (spam_probability * 100) * 0.70
        +
        security_score * 0.30
    )

    # SAFE
    if final_score < 30:

        return (
            "SAFE",
            "🟢",
            final_score
        )

    # SUSPICIOUS
    elif final_score < 70:

        return (
            "SUSPICIOUS",
            "🟡",
            final_score
        )

    # DANGEROUS
    else:

        return (
            "DANGEROUS",
            "🔴",
            final_score
        )


# user interface

st.title(" 🛡️ CyberSift ")

st.write(
    " Spam Classifier — AI Message Security Analyzer ,\n"
    " Stay Ahead of Spam & Scams "
)


st.divider()


# message input
message = st.text_area(
    "📩 Enter your message ",
    height=180,
    placeholder=(
        "Example: "
        "URGENT! Your account will be blocked. "
        "Verify your password immediately."
    )
)


# Analyse button 

if st.button(
    "🔍 Analyze Message",
    use_container_width=True
):

    if not message.strip():

        st.warning(
            "Please enter a message first."
        )

    else:

        # ML prediction 

        probabilities = model.predict_proba(
            [message]
        )[0]

        spam_probability = probabilities[1]


       #Security analysis

        security_score, indicators = (
            security_analysis(message)
        )


        # final risk
        risk, emoji, final_score = (
            calculate_risk(
                spam_probability,
                security_score
            )
        )


        # result

        st.divider()

        st.subheader("🔎 Security Analysis")


        if risk == "SAFE":

            st.success(
                f"{emoji} {risk}"
            )

        elif risk == "SUSPICIOUS":

            st.warning(
                f"{emoji} {risk}"
            )

        else:

            st.error(
                f"{emoji} {risk}"
            )


        # scores

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Spam Probability",
                f"{spam_probability * 100:.1f}%"
            )

        with col2:

            st.metric(
                "Security Score",
                f"{security_score}/100"
            )

        with col3:

            st.metric(
                "Final Risk",
                f"{final_score:.1f}/100"
            )


        st.progress(
            min(float(final_score) / 100, 1.0)
        )


        #detected indicators

        st.subheader(
            "🚨 Detected Security Indicators"
        )


        if indicators:

            for indicator in indicators:

                st.write(
                    f"⚠️ {indicator}"
                )

        else:

            st.write(
                "✅ No major security indicators detected."
            )


        # Recomendations
        st.subheader(
            "💡 Recommendation"
        )


        if risk == "SAFE":

            st.info(
                "The message appears to be safe. "
                "However, always verify unexpected requests."
            )

        elif risk == "SUSPICIOUS":

            st.warning(
                "Be careful with this message. "
                "Avoid clicking unknown links or "
                "sharing personal information."
            )

        else:

            st.error(
                "Do not click suspicious links or "
                "share passwords, OTPs, PINs or banking information."
            )


# sidebar

st.sidebar.title("🛡️ About")

st.sidebar.write(
    "**CyberSift**"
)

st.sidebar.write(
    "**Machine Learning:** Naive Bayes"
)

st.sidebar.write(
    "**Feature Extraction:** TF-IDF"
)

st.sidebar.write(
    "**Security:** Rule Engine"
)

st.sidebar.write(
    "**Risk Levels:**"
)

st.sidebar.write(
    "🟢 SAFE"
)

st.sidebar.write(
    "🟡 SUSPICIOUS"
)

st.sidebar.write(
    "🔴 DANGEROUS"
)

st.sidebar.write(
    f"**Model Accuracy:** "
    f"{accuracy * 100:.2f}%"
)


#page configuration

st.set_page_config(
    page_title="CyberSift",
    page_icon="🛡️",
    layout="centered"
)

#theme selector

st.sidebar.title("🎨 Appearance")

theme = st.sidebar.selectbox(
    "Choose Theme",
    [
        "Dark",
        "Cyber Blue"
    ]
)

#custom themes

if theme == "Dark":

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0e1117;
            color: white;
        }

        h1, h2, h3 {
            color: white;
        }

        .stTextArea textarea {
            background-color: #1b1f27;
            color: white;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


elif theme == "Cyber Blue":

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #061826;
            color: #e6f7ff;
        }

        h1, h2, h3 {
            color: #00d9ff;
        }

        .stTextArea textarea {
            background-color: #0b2638;
            color: #ffffff;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

st.set_page_config(page_title="FAST neuro.ai", page_icon="🧠", layout="wide")

rename_map = {
    "gender": "Gender",
    "age": "Age",
    "hypertension": "High Blood Pressure",
    "heart_disease": "Heart Disease",
    "ever_married": "Marital Status",
    "work_type": "Type of Employment",
    "residence_type": "Area of Residence",
    "avg_glucose_level": "Average Blood Sugar (mg/dL)",
    "bmi": "BMI",
    "smoking_status": "Smoking Status"
}

def main_app():
    """Main application"""

    api_key = st.secrets.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None

    with st.sidebar:
        st.header("Your Personal Health Profile")

        st.subheader("Demographics")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.slider("Age", min_value=1, max_value=100, value=50)
        ever_married = st.radio("Marital Status", ["Yes", "No"], horizontal=True)

        st.subheader("Lifestyle")
        residence_type = st.radio("Area of Residence", ["Urban", "Rural"])
        smoking_status = st.selectbox("Smoking Status", ["Never smoked", "Formerly smoked", "Currently smoking", "Unknown"])
        work_type = st.selectbox("Employment Type", ["Private sector", "Self-employed", "Government job", "Child", "Never worked"])

        st.subheader("Medical History")
        st.write("Please tick the checkbox if it applies to you.")
        heart_disease = st.checkbox("Heart Disease")
        hypertension = st.checkbox("Hypertension")

        st.subheader("Clinical Features")
        bmi = st.slider("BMI", min_value=10.0, max_value=60.0, value=24.0, step=0.1)
        avg_glucose_level = st.slider("Average Blood Sugar (mg/dL)", min_value=50.0, max_value=280.0, value=80.0, step=0.5)

        run = st.button("Run Assessment to Get Your Individual Stroke Risk Score")

    if run:
        st.session_state["inputs"] = {
            "gender": gender,
            "age": age,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "ever_married": ever_married,
            "work_type": work_type,
            "residence_type": residence_type,
            "avg_glucose_level": avg_glucose_level,
            "bmi": bmi,
            "smoking_status": smoking_status
        }
        st.rerun()

    if "inputs" not in st.session_state:
        st.session_state["inputs"] = None

    inputs = st.session_state["inputs"]

    st.title("FAST neuro.ai")
    st.write("Welcome! Our app helps assess potential stroke risk using medical data. Please note that this does not replace consultation with a doctor.")
    st.divider()

    score_col, summary_col, api_col = st.columns([1, 1, 1], gap="large")

    with score_col:
        st.subheader("Stroke Risk Score")
        st.info("PLACEHOLDER")

        fig, ax = plt.subplots()
        ax.bar(["Risk Score"], [0])
        ax.set_ylim(0, 100)
        ax.set_ylabel("Percent")
        ax.set_title("Predicted Risk Score")
        st.pyplot(fig)

    with summary_col:
        st.subheader("Your Input Summary")

        if inputs:
            summary = {
                rename_map.get(k, k): "Yes" if v is True else ("No" if v is False else v)
                for k, v in inputs.items()
            }
            st.dataframe(
                pd.DataFrame.from_dict(summary, orient="index", columns=["Value"]),
                use_container_width=True,
            )
        else:
            st.info("Please fill in the sidebar and run assessment.")

    with api_col:
        st.subheader("Next Steps and Help: What Your Risk Score Means")

        with st.expander("AI-powered Interpretation with OpenAI", expanded=True):
            ai_disabled = not inputs or client is None
            if st.button("Interpret My Personal Stroke Risk", disabled=ai_disabled):
                prompt = f"""
A person has the following profile:
- Gender: {inputs['gender']}, Age: {inputs['age']}, Marital Status: {inputs['ever_married']}
- Type of Employment: {inputs['work_type']}, Area of Residence: {inputs['residence_type']}
- BMI: {inputs['bmi']}, Average Blood Sugar (mg/dL): {inputs['avg_glucose_level']}
- Smoking Status: {inputs['smoking_status']}
- Heart Disease: {"Yes" if inputs['heart_disease'] else "No"}
- High Blood Pressure: {"Yes" if inputs['hypertension'] else "No"}

In 3-4 sentences, explain in simple language what these inputs mean for the person's predicted stroke risk.
Suggest two concrete lifestyle changes to lower risk over time.
"""

                with st.spinner("Consulting OpenAI..."):
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a medical assistant explaining stroke risk in simple language. Make clear that you do not replace a licensed doctor."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                    st.write(completion.choices[0].message.content)

main_app()

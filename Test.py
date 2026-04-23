import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

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
    "smoking_status": "Smoking Status",
}


def main_app():
    """Main application"""

    api_key = st.secrets.get("OPENAI_API_KEY", None)
    client = OpenAI(api_key=api_key) if (api_key and OpenAI is not None) else None

    with st.sidebar:
        st.header("Your Personal Health Profile")

        st.subheader("Demographics")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.slider("Age", min_value=1, max_value=100, value=50)
        ever_married = st.radio("Marital Status", ["Yes", "No"], horizontal=True)

        st.subheader("Lifestyle")
        residence_type = st.radio("Area of Residence", ["Urban", "Rural"])
        smoking_status = st.selectbox(
            "Smoking Status",
            ["Never smoked", "Formerly smoked", "Currently smoking", "Unknown"]
        )
        work_type = st.selectbox(
            "Employment Type",
            ["Private sector", "Self-employed", "Government job", "Child", "Never worked"]
        )

        st.subheader("Medical History")
        st.write("Please tick the checkbox if it applies to you.")
        heart_disease = st.checkbox("Heart Disease")
        hypertension = st.checkbox("Hypertension")

        st.subheader("Clinical Features")
        bmi = st.slider("BMI", min_value=10.0, max_value=60.0, value=24.0, step=0.1)
        avg_glucose_level = st.slider(
            "Average Blood Sugar (mg/dL)",
            min_value=50.0,
            max_value=280.0,
            value=80.0,
            step=0.5
        )

        run = st.button("Run Assessment to Get Your Individual Stroke Risk Score")

    if "inputs" not in st.session_state:
        st.session_state["inputs"] = None

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
            "smoking_status": smoking_status,
        }

    inputs = st.session_state["inputs"]

    st.title("FAST neuro.ai")
    st.write(
        "Welcome! Our app helps assess potential stroke risk using medical data. "
        "Please note that this does not replace consultation with a doctor."
    )
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

        st.divider()

        st.subheader("Risk Factors")
        st.info("PLACEHOLDER")

        factors_placeholder = {
            "Age >= 65": inputs["age"] >= 65 if inputs else False,
            "High Blood Pressure": inputs["hypertension"] if inputs else False,
            "Heart Disease": inputs["heart_disease"] if inputs else False,
            "BMI >= 30": inputs["bmi"] >= 30 if inputs else False,
            "High Blood Sugar (>140 mg/dL)": inputs["avg_glucose_level"] > 140 if inputs else False,
            "Active Smoker": inputs["smoking_status"] == "Currently smoking" if inputs else False,
        }

        factor_df = pd.DataFrame(
            [
                {
                    "Risk Factor": k,
                    "Present": "🔴 Yes" if v else "🟢 No"
                }
                for k, v in factors_placeholder.items()
            ]
        )
        st.dataframe(factor_df, hide_index=True, use_container_width=True)
        st.metric("Active Risk Factors", f"{sum(factors_placeholder.values())} / 6")

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

        st.divider()
        st.subheader("Key Metrics")
        st.caption("PLACEHOLDER")

    with api_col:
        st.subheader("Next Steps and Help: What Your Risk Score Means")

        with st.expander("AI-powered Interpretation with OpenAI", expanded=True):
            if not inputs:
                st.info("Run an assessment first.")
            elif client is None:
                st.warning("No OpenAI API key found. Add OPENAI_API_KEY in your app secrets to use this feature.")
            else:
                if st.button("Interpret My Personal Stroke Risk"):
                    prompt = f"""
A person has the following profile:
- Gender: {inputs['gender']}, Age: {inputs['age']}, Marital Status: {inputs['ever_married']}
- Type of Employment: {inputs['work_type']}, Area of Residence: {inputs['residence_type']}
- BMI: {inputs['bmi']}, Average Blood Sugar (mg/dL): {inputs['avg_glucose_level']}
- Smoking Status: {inputs['smoking_status']}
- Heart Disease: {"Yes" if inputs['heart_disease'] else "No"}
- High Blood Pressure: {"Yes" if inputs['hypertension'] else "No"}

In 3-4 sentences, explain in simple language what these inputs mean for the person's predicted
stroke risk. Suggest two concrete lifestyle changes to lower stroke risk over time.
"""

                    with st.spinner("Consulting OpenAI..."):
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are a medical assistant explaining stroke risk in simple language. "
                                        "Make the user aware you do not replace a licensed doctor."
                                    ),
                                },
                                {
                                    "role": "user",
                                    "content": prompt,
                                },
                            ],
                        )
                        st.write(completion.choices[0].message.content)

        with st.expander("Finding the nearest doctor with Google Maps", expanded=True):
            st.markdown(
                "FAST neuro.ai leverages Google Maps to find the nearest doctor by postcode with just one click."
            )
            st.text_input("Postcode", placeholder="e.g. 9000")
            st.button("Find doctors near me", disabled=True)


main_app()
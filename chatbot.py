import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import re
import json
import io
from fpdf import FPDF
from PIL import Image
import tempfile
from datetime import datetime
from crews.chatbot_crew import chatbot_crew

st.set_page_config(page_title="IEM Admission Chatbot", page_icon="🎓")
st.title("🎓 Admin Chatbot for IEM Admissions")

# ----------------- PDF saving logic with charts ---------------- #
def save_chat_to_pdf(chat_history):
    from fpdf import FPDF
    import matplotlib.pyplot as plt
    import tempfile
    import pandas as pd
    import io
    import re

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Chat Transcript", ln=True, align="C")
    pdf.ln(10)

    for msg in chat_history:
        role = msg["role"].capitalize()
        content = msg["content"]

        # Clean markdown symbols
        content = content.replace("**", "")
        content = re.sub(r"#+ ", "", content)
        lines = content.splitlines()

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{role}:", ln=True)
        pdf.set_font("Arial", "", 12)

        for line in lines:
            line = line.strip()

            if not line:
                pdf.ln(2)

            elif line.startswith("* "):
                # Bullet point
                pdf.cell(5)
                pdf.cell(0, 10, f"- {line[2:]}", ln=True)

            elif "|" in line and line.count("|") >= 2:
                # Table row
                cols = [col.strip() for col in line.split("|") if col.strip()]
                if len(cols) == 0:
                    continue
                col_width = pdf.w / len(cols) - 5
                max_chars = int(col_width // 2.5)

                for col in cols:
                    cell_text = col[:max_chars] + "..." if len(col) > max_chars else col
                    pdf.cell(col_width, 8, cell_text, border=1)
                pdf.ln(8)

            else:
                # Regular paragraph
                pdf.multi_cell(0, 10, line)

        pdf.ln(5)

        # Render visualizations if present
        if msg.get("visualizations"):
            for vis in msg["visualizations"]:
                fig, ax = plt.subplots()

                if vis["type"] == "bar":
                    df = pd.DataFrame(vis["data"], index=["Count"]).T
                    df.plot(kind="bar", legend=False, ax=ax)
                    ax.set_title(vis["title"])

                elif vis["type"] == "pie":
                    labels = list(vis["data"].keys())
                    values = list(vis["data"].values())
                    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
                    ax.axis("equal")
                    ax.set_title(vis["title"])

                else:
                    plt.close(fig)
                    continue

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                    fig.savefig(tmpfile.name, bbox_inches="tight")
                    pdf.image(tmpfile.name, w=160)
                plt.close(fig)
                pdf.ln(10)

    # Return as BytesIO buffer
    pdf_output = pdf.output(dest="S").encode("latin1")
    return io.BytesIO(pdf_output)


# ---------------- Chat UI and response handling ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display old messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("visualizations"):
            for vis in msg["visualizations"]:
                st.subheader(f"📊 {vis['title']}")
                if vis["type"] == "bar":
                    st.bar_chart(pd.DataFrame(vis["data"], index=["Count"]).T)
                elif vis["type"] == "pie":
                    labels = list(vis["data"].keys())
                    values = list(vis["data"].values())
                    fig, ax = plt.subplots()
                    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
                    ax.axis("equal")
                    st.pyplot(fig)
                elif vis["type"] == "metric":
                    st.metric(vis["title"], vis["value"])

# Input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking... 🤔"):
        response = chatbot_crew.kickoff({"user_input": user_input})

    response_text = str(response)
    response_clean = re.sub(r"```json\s*({.*?})\s*```", "", response_text, flags=re.DOTALL)

    json_match = re.search(r"```json\s*({.*?})\s*```", response_text, re.DOTALL)
    vis_data = json.loads(json_match.group(1)) if json_match else {}
    visualizations = vis_data.get("visualizations", []) if isinstance(vis_data, dict) else []

    with st.chat_message("assistant"):
        st.markdown(response_clean)
        for vis in visualizations:
            st.subheader(f"📊 {vis['title']}")
            if vis["type"] == "bar":
                st.bar_chart(pd.DataFrame(vis["data"], index=["Count"]).T)
            elif vis["type"] == "pie":
                labels = list(vis["data"].keys())
                values = list(vis["data"].values())
                fig, ax = plt.subplots()
                ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
                ax.axis("equal")
                st.pyplot(fig)
            elif vis["type"] == "metric":
                st.metric(vis["title"], vis["value"])
        # 📋 Detect and parse markdown-style table from plain text
        table_lines = []
        collecting = False

        for line in response_clean.splitlines():
            if "|" in line and line.count("|") >= 2:
                table_lines.append(line.strip())
                collecting = True
            elif collecting and line.strip() == "":
                break
            elif collecting:
                table_lines.append(line.strip())

        if len(table_lines) >= 3:
            headers = [h.strip() for h in table_lines[0].split("|") if h.strip()]
            rows = []
            for row in table_lines[2:]:
                cols = [c.strip() for c in row.split("|") if c.strip()]
                if len(cols) == len(headers):
                    rows.append(cols)
            if rows:
                df_table = pd.DataFrame(rows, columns=headers)
                st.markdown("### 📋 Table Detected:")
                st.dataframe(df_table)

                csv_buffer = io.StringIO()
                df_table.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="⬇️ Download Table as CSV",
                    data=csv_buffer.getvalue(),
                    file_name="student_table.csv",
                    mime="text/csv"
                )

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response_clean,
        "visualizations": visualizations
    })

# ----------------- PDF Download ----------------- #
if st.session_state.chat_history:
    st.markdown("---")
    if st.button("💾 Save Chat as PDF"):
        pdf_buffer = save_chat_to_pdf(st.session_state.chat_history)
        st.download_button("⬇️ Download Chat as PDF", data=pdf_buffer, file_name="chat_transcript.pdf", mime="application/pdf")
        st.success("✅ PDF with charts generated successfully!")

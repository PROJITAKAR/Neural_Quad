from crewai.tools import tool
import google.generativeai as genai
from config.config import GEMINI_API_KEY
import chromadb


genai.configure(api_key=GEMINI_API_KEY)
chroma_client = chromadb.PersistentClient(path="./admission_db")
admission_collection = chroma_client.get_or_create_collection(name="admission_progress")

@tool
def fetch_student_summaries(user_input: str) -> list[str]:
    """
    Uses Gemini to analyze a natural language admin query,
    constructs a filter, and returns matching student summaries.
    """
    result = admission_collection.get(include=["documents", "metadatas"])
    documents = result.get("documents", [])
    ids = result.get("ids", [])
    metadatas = result.get("metadatas", [])

    if not documents or not ids:
        return ["❌ No student data available."]

    # Reconstruct records in your exact format:
    formatted_records = []
    for i in range(len(documents)):
        sid = ids[i]
        name = metadatas[i].get("name", "Unknown") if i < len(metadatas) else "Unknown"
        summary = documents[i]
        record = f"Student ID: {sid}\nName: {name}\nSummary: {summary}"
        formatted_records.append(record)

    full_text = "\n--------------------------------------------------\n".join(formatted_records)

    # Prompt Gemini to decide what IDs to fetch
    prompt = f"""
You are an intelligent assistant working for a college admission team.

Your job is to **analyze user queries** and **identify student records** based on their meaning.

## User Query:
\"\"\"{user_input}\"\"\"

## Student Records (Structured):
Each record follows this format:
- Student ID
- Name
- Summary: includes Document status, Admission status (Shortlisted/Not), Loan (Approved/Not), Email status, and Error if any.

### Task:
1. Go through the student records below.
2. Based on the query above, **select the student IDs that match**.
3. Your response should ONLY contain a list of matching student IDs (like S001, S015, etc.), one per line.
4. If no records match, reply with 'NONE'.
5.If the admin query does not mention specific student IDs, names, or conditions,then fetch summaries for **all students** by default.This helps in generating overall statistics and trends.

DO NOT return explanations or summaries. Just the IDs.

## Records:
{full_text}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    filtered_ids = [line.strip() for line in response.text.splitlines() if line.strip().startswith("S")]

    if not filtered_ids:
        return ["❌ No matching students found."]

    # Fetch summaries only for those IDs
    match_result = admission_collection.get(ids=filtered_ids)
    return match_result.get("documents", ["❌ Could not retrieve summaries."])



@tool
def format_student_summaries(summaries: list[str],user_input: str) -> list[str]:
    """
    Takes raw student summaries and returns a formatted, ChatGPT-style response using Gemini.
    """
    if not summaries:
        return "❌ No summaries provided to format."

    joined = "\n\n".join([f"- {s}" for s in summaries])

    prompt = """
        You are a smart AI assistant for a college admission office.

        Your job is to analyze and respond to the admin's query below. You are provided:
        1. The admin's query in natural language.
        2. A list of student summaries, each with:
        - Student ID and Name
        - Admission Status (Shortlisted/Not Shortlisted)
        - Loan Info (Approved/Not Approved/NA)
        - Document Status and Email Sent Status

        ---

        ## Admin Query:
        \"\"\"{user_input}\"\"\"

        ---

        ## Student Summaries:
        \"\"\"{joined}\n\"\"\"

        ---

        ## Your task:
        - First, understand the admin's intent based on their query.
        - If they are asking for **student-level details**, format those records neatly in markdown.
        - If they are asking for an **analysis** (e.g., trends, counts, or comparisons), give a high-level insight-driven report.
        - If both are implied, provide both: start with a summary/analysis, then give student details.
        - if the user asks who you are, what you do, or what your role is or anything you think out of the scope: 
            - You should always politely introduce yourself. 
            - Explain that you are the IEM Admission Assistant chatbot and describe your capabilities (student status, loan updates, document review, admission summary, etc).then don't give user data that time.
        

        ### When formatting student details:
        - Use clear section headers: **Admission**, **Documents**, **Loan**, **Email**
        - Use bullet points or short paragraphs for clarity
        - You can give **tables** as well.
        - strictly use table,if it is asked by user.
        - Explain things like "Not Shortlisted (Rank above 9500)" in plain language
        - Do NOT use emojis
        
        ### When providing analysis:
        - Provide total counts: total students, shortlisted, not shortlisted
        - Highlight reasons for rejection, document issues, or loan trends
        - Mention any interesting patterns (e.g., "Most rejected students had rank above 9500")

        Keep the tone professional and concise. Use markdown headings and bullet lists.

        ### For visualizations:(use JSON block)(optional)
            -you can use if you thinks it is necessary 
            -it will add some insight
            - If they want analysis, summarize patterns or trends or you think it is needed then at the **end**, include a JSON block with this structure:

        Template:-(try to follow this format only for visualization but you can change the content)
        ```json
         {{
            "visualizations": [
                {{
                    "title": "Admission Status",
                    "type": "pie",
                    "data": {{
                        "Shortlisted": 15,
                        "Not Shortlisted": 35
                    }}
                }},
                {{
                    "title": "Loan Status",
                    "type": "bar",
                    "data": {{
                        "Approved": 12,
                        "Not Approved": 10,
                        "NA": 8
                    }}
                }},
                {{
                    "title": "Document Errors",
                    "type": "metric",
                    "value": 6
                }}
            ]
        }}
        ```
        Only include the JSON — no extra explanation.

        This JSON will be used for chart visualizations.
        

    """
    final_prompt = prompt.format(user_input=user_input, joined=joined)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    response = model.generate_content(final_prompt)
    return response.text

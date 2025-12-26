import streamlit as st
import pandas as pd
import mysql.connector
from groq import Groq

# ---------------- Upload CSV → Load into MySQL ----------------
def load_file(uploaded_file, mysql_host, mysql_user, mysql_password, mysql_db):
    df = pd.read_csv(uploaded_file)

    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
    )

    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS data_table")

    col_defs = ", ".join([f"`{col}` TEXT" for col in df.columns])
    cursor.execute(f"CREATE TABLE data_table ({col_defs})")

    data = [tuple(row.astype(str)) for _, row in df.iterrows()]
    placeholders = ", ".join(["%s"] * len(df.columns))
    cursor.executemany(f"INSERT INTO data_table VALUES ({placeholders})", data)
    conn.commit()
    cursor.close()

    return conn, df.columns.tolist(), df

# ---------------- English → SQL Generator ----------------
def generate_sql(question, columns, client):
    schema = ", ".join(columns)
    prompt = f"""
Convert English to SQL.
Table: data_table
Columns: {schema}
Return ONLY SQL.
Question: {question}
"""
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an SQL generator."},
            {"role": "user", "content": prompt},
        ],
        temperature=0
    )

    sql = completion.choices[0].message.content.strip()

    # cleanup
    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "").strip()

    if sql.lower().startswith("sql"):
        sql = sql[3:].strip()

    if not sql.endswith(";"):
        sql += ";"

    return sql

# ---------------- Show SQL Bot Page ----------------
def show_sql_bot(api_key, mysql_host, mysql_user, mysql_password, mysql_db):
    st.title("SQL Bot")

    client = Groq(api_key=api_key)

    uploaded = st.file_uploader("Upload CSV for SQL Bot", type=["csv"])

    if uploaded:
        conn, columns, df = load_file(uploaded, mysql_host, mysql_user, mysql_password, mysql_db)

        st.write("### Data Preview")
        st.dataframe(df.head(100))

        if st.checkbox("Show summary statistics"):
            st.write(df.describe())

        question = st.text_input("Ask your question:")

        if question:
            with st.spinner("Generating SQL & executing..."):
                try:
                    sql = generate_sql(question, columns, client)
                    st.code(sql, language="sql")

                    result_df = pd.read_sql(sql, conn)

                    st.write("### Query Result")
                    st.dataframe(result_df)

                    csv = result_df.to_csv(index=False).encode("utf-8")
                    st.download_button("Download Result CSV", csv, "query_result.csv")

                    st.success("Query executed successfully!")

                except Exception as e:
                    st.error(f"SQL Error: {e}")

        conn.close()

    if st.button("⬅ Back"):
        st.session_state.page = "landing"
        st.rerun()

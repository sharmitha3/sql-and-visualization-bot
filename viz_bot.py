import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.io as pio

pio.templates.default = "plotly"

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

    return conn, df

# ---------------- Show Viz Bot Page ----------------
def show_viz_bot(mysql_host, mysql_user, mysql_password, mysql_db):
    st.title("Visualization Bot")

    uploaded = st.file_uploader("Upload CSV for Viz Bot", type=["csv"])

    if uploaded:
        conn, df = load_file(uploaded, mysql_host, mysql_user, mysql_password, mysql_db)

        st.write("### Data Preview")
        st.dataframe(df.head(100))

        chart_type = st.selectbox(
            "Choose Chart Type",
            ["Bar chart", "Line chart", "Scatter plot", "Pie chart", "Histogram", "Area chart"]
        )

        numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
        all_columns = df.columns.tolist()

        if chart_type in ["Bar chart", "Line chart", "Scatter plot", "Area chart"]:
            x_axis = st.selectbox("X-axis", all_columns)
            y_axis = st.selectbox("Y-axis", numeric_columns)
        elif chart_type == "Pie chart":
            x_axis = st.selectbox("Category", all_columns)
            y_axis = None
        elif chart_type == "Histogram":
            x_axis = st.selectbox("Column", numeric_columns)
            y_axis = None

        if st.button("Generate Chart"):
            if chart_type == "Bar chart":
                fig = px.bar(df, x=x_axis, y=y_axis)
            elif chart_type == "Line chart":
                fig = px.line(df, x=x_axis, y=y_axis)
            elif chart_type == "Scatter plot":
                fig = px.scatter(df, x=x_axis, y=y_axis)
            elif chart_type == "Area chart":
                fig = px.area(df, x=x_axis, y=y_axis)
            elif chart_type == "Pie chart":
                fig = px.pie(df, names=x_axis)
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_axis)

            st.plotly_chart(fig)
            html_str = fig.to_html(full_html=True, include_plotlyjs='cdn')
            html_bytes = html_str.encode("utf-8")
            st.download_button(
                label="📥 Download Chart (HTML)",
                data=html_bytes,
                file_name="chart.html",
                mime="text/html"
            )

        conn.close()

    if st.button("⬅ Back"):
        st.session_state.page = "landing"
        st.rerun()

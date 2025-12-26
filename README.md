# sql-and-visualization-bot
<b>1. Project Aim</b><br>
This project allows users to upload CSV files and explore their data easily using plain English queries and interactive visualizations. It has two main parts:<br>
- SQL Bot: Ask questions in English, and the system automatically generates SQL queries to retrieve results from the uploaded CSV.<br>
- Visualization Bot: Create charts like bar, line, scatter, pie, histogram, and area charts from CSV data.<br><br>

<b>2. Algorithm / How It Works</b><br>

<b>SQL Bot:</b><br>
1. User uploads a CSV file.<br>
2. Data is loaded into a temporary MySQL table.<br>
3. The user types a question in plain English.<br>
4. The Groq API generates the SQL query based on the table schema.<br>
5. The SQL query is executed, and results are displayed and downloadable as CSV.<br><br>

<b>Visualization Bot:</b><br>
1. User uploads a CSV file.<br>
2. Data is loaded into MySQL.<br>
3. User selects the chart type (Bar, Line, Scatter, Pie, Histogram, Area).<br>
4. User selects the columns for axes/categories.<br>
5. The chart is generated using Plotly and can be previewed or downloaded as HTML.<br><br>

<b>3. Steps to Run the Project</b><br>
1. Clone the repository to your computer.<br>
2. Install dependencies using <code>pip install -r requirements.txt</code>.<br>
3. Create a <code>.env</code> file in the project folder with your credentials:<br>
&nbsp;&nbsp;- GROQ_API_KEY<br>
&nbsp;&nbsp;- MYSQL_HOST<br>
&nbsp;&nbsp;- MYSQL_USER<br>
&nbsp;&nbsp;- MYSQL_PASSWORD<br>
&nbsp;&nbsp;- MYSQL_DATABASE<br>
4. Run the Streamlit app using <code>streamlit run app.py</code>.<br>
5. Use the sidebar to navigate between SQL Bot and Visualization Bot.<br><br>

<b>4. Features</b><br>
- Upload CSV and explore data instantly.<br>
- Automatic SQL query generation from plain English.<br>
- Interactive charts with Plotly.<br>
- Download results or charts directly.<br>
- Simple, beginner-friendly interface with Streamlit.<br><br>

<b>5. Folder Structure (Recommended)</b><br>
- app.py<br>
- sql_bot.py<br>
- viz_bot.py<br>
- requirements.txt<br>
- README.md<br>
- .env (contains environment variables, not uploaded to GitHub)<br><br>

<b>6. Dependencies</b><br>
- streamlit<br>
- pandas<br>
- mysql-connector-python<br>
- plotly<br>
- python-dotenv<br>
- groq<br><br>



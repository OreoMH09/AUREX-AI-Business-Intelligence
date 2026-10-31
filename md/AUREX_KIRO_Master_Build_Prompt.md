# AUREX — KIRO IDE MASTER BUILD PROMPT

## Project
**AUREX — Multimodal RAG-Based Business Intelligence and Decision Support System**

You are a senior Python AI/ML engineer, RAG architect, agentic AI engineer, data analyst, backend/frontend engineer, QA engineer and DevOps engineer.

Build this as a serious final-year B.Tech CSE(AIML) portfolio project. Do not build a toy chatbot.

---

# 1. PROJECT GOAL

Build an AI Business Intelligence system where a user uploads business data in:

- PDF
- Excel/XLSX
- CSV

The user can ask natural-language business questions. The system should:

1. Retrieve relevant information using RAG.
2. Analyze structured data using Python/Pandas.
3. Compare historical and current periods.
4. Identify trends and patterns.
5. Generate on-demand business visualizations.
6. Perform what-if/scenario analysis.
7. Generate evidence-grounded business suggestions.
8. Produce a professional analytical report.
9. Show the sources/evidence used.

Core principle:

**Retrieval → Calculation → Visualization → Reasoning → Recommendation → Report**

---

# 2. CURRENT SCOPE

Implement now:

- PDF ingestion
- Excel/XLSX ingestion
- CSV ingestion
- Text/table extraction
- Metadata extraction
- Dataset profiling
- Chunking
- Embeddings
- Vector database
- Semantic retrieval
- Hybrid retrieval where practical
- Reranking where practical
- RAG answer generation
- AI agent/tool orchestration
- Pandas/NumPy analytics
- KPI calculation
- Year-over-year comparison
- Historical comparison
- Trend analysis
- Scenario/what-if analysis
- On-demand charts
- Interactive dashboard
- Evidence/source citations
- Business suggestions
- Report generation/export
- FastAPI backend
- Streamlit frontend
- Evaluation
- Tests
- Logging
- Error handling
- Docker
- Documentation

Keep these ONLY for future scope:

- Automated scheduled enterprise data pipelines
- Real-time ERP/CRM synchronization
- Autonomous financial transactions
- Autonomous business actions
- Full Power BI replacement
- Guaranteed future prediction

Architecture should allow these later without rewriting the core.

---

# 3. TECHNOLOGY

Use Python only for application logic.

Recommended:

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Streamlit
- LangChain or LlamaIndex
- Hugging Face/Sentence Transformers embeddings
- ChromaDB (preferred) or FAISS
- Ollama/local open-source LLM where practical
- Pandas
- NumPy
- openpyxl
- PyMuPDF
- OCR library where needed
- Plotly
- pytest
- RAGAS/custom evaluation
- Docker

Use abstractions so the LLM/vector/embedding provider can be changed without rewriting the application.

Avoid unnecessary dependencies.

---

# 4. ARCHITECTURE

```text
                         USER
                           |
                           v
                  +------------------+
                  |   STREAMLIT UI   |
                  +--------+---------+
                           |
                           v
                    +-------------+
                    |   FASTAPI   |
                    +------+------+
                           |
                           v
                    +-------------+
                    | AI AGENT /  |
                    | ORCHESTRATOR|
                    +------+------+
                           |
              +------------+-------------+
              |            |             |
              v            v             v
             RAG       ANALYTICS    VISUALIZATION
           ENGINE       ENGINE          ENGINE
              |            |             |
              v            v             v
        PDF/XLSX/CSV    Pandas         Plotly
              |         NumPy
              v            |             |
        Vector Store       |             |
              |            |             |
              +------------+-------------+
                           |
                           v
                    REPORT GENERATOR
                           |
              +------------+-------------+
              |            |             |
              v            v             v
          Findings       Charts      Suggestions
                           |
                           v
                     SOURCES/EVIDENCE
```

---

# 5. DATA INGESTION

Create a common ingestion pipeline:

```text
File
 ↓
File Type Detection
 ↓
Parser
 ↓
Cleaning / Normalization
 ↓
Metadata
 ↓
Profiling
 ↓
Chunking / Structured Representation
 ↓
Embeddings
 ↓
Vector Store
```

## PDF

Extract:

- text
- page numbers
- headings/sections where possible
- tables where possible
- metadata
- OCR for scanned documents where necessary

## Excel

Process:

- workbook
- sheets
- headers
- rows
- columns
- data types
- missing values

Preserve sheet names and useful table context.

## CSV

Process:

- headers
- rows
- data types
- missing values

Never destroy the original meaning of the dataset.

---

# 6. DATA PROFILING

After XLSX/CSV upload, automatically identify where possible:

- numeric columns
- categorical columns
- date columns
- year/month columns
- revenue
- sales
- profit
- expenses/cost
- product
- region
- customer

Do not rely only on exact column names. Use robust semantic matching.

Display:

- row count
- column count
- data types
- missing values
- date range
- detected business fields

Only calculate a KPI when the required data actually exists.

---

# 7. METADATA

Preserve metadata for citations and filtering.

Example:

```python
{
    "document_id": "...",
    "filename": "annual_report.pdf",
    "file_type": "pdf",
    "page": 31,
    "section": "Financial Performance",
    "year": 2025
}
```

Excel:

```python
{
    "document_id": "...",
    "filename": "sales.xlsx",
    "file_type": "xlsx",
    "sheet": "Sales",
    "year": 2025
}
```

Never fabricate page, sheet, year or source information.

---

# 8. RAG

Implement:

```text
Query
 ↓
Query understanding
 ↓
Semantic retrieval
 ↓
Optional keyword/hybrid retrieval
 ↓
Metadata filtering
 ↓
Optional reranking
 ↓
Relevant context
 ↓
LLM
 ↓
Answer + citations
```

Support:

- top-k
- metadata filtering
- document filtering
- year filtering where available
- source tracking

RAG must retrieve evidence rather than invent answers.

If evidence is insufficient, return:

> Insufficient evidence in the uploaded data to provide a reliable answer.

---

# 9. IMPORTANT: RAG IS NOT THE CALCULATOR

Do not ask the LLM to perform critical business arithmetic.

Use Python/Pandas/NumPy for:

- totals
- averages
- percentages
- growth
- margins
- comparisons
- rankings
- scenarios

The LLM interprets the calculated results.

Example:

```text
User:
Compare 2024 and 2025 revenue.

Agent
 ↓
RAG finds relevant data
 ↓
Analytics calculates values
 ↓
Visualization creates chart
 ↓
LLM explains
 ↓
Sources displayed
```

---

# 10. AI AGENT

Build a controlled tool-using agent.

Tools:

```text
search_documents()
retrieve_information()
analyze_dataset()
calculate_kpis()
compare_periods()
analyze_trends()
generate_chart()
run_scenario()
generate_report()
get_source_information()
```

Examples:

```text
"What is revenue?"
→ retrieval + analytics

"Show monthly revenue."
→ retrieval + analytics + visualization

"Compare 2024 and 2025."
→ retrieval + comparison + visualization

"What happens if expenses rise 10%?"
→ retrieval + scenario calculation

"How can we improve revenue?"
→ evidence + analytics + trend analysis + recommendation
```

Do NOT create an uncontrolled autonomous loop.

Use:

```text
Query
 ↓
Intent
 ↓
Tool selection
 ↓
Tool execution
 ↓
Evidence validation
 ↓
Result synthesis
 ↓
Final answer
```

Set maximum tool calls and timeouts.

---

# 11. ANALYTICS ENGINE

Create reusable deterministic functions:

```python
calculate_revenue()
calculate_profit()
calculate_margin()
calculate_growth_rate()
calculate_yoy_change()
compare_periods()
rank_products()
rank_regions()
analyze_expenses()
analyze_trend()
```

Handle:

- missing columns
- missing values
- invalid types
- division by zero
- insufficient historical data

---

# 12. HISTORICAL COMPARISON

Support:

- previous year vs current year
- month-over-month
- quarter-over-quarter where data supports it
- product comparisons
- regional comparisons

Example:

```text
2024 Revenue: ₹80L
2025 Revenue: ₹94L

Absolute Change: ₹14L
Growth: 17.5%
```

Generate a comparison visualization when appropriate.

---

# 13. TREND ANALYSIS

Identify where supported:

- increasing trends
- decreasing trends
- sudden changes
- peaks
- drops
- possible seasonal patterns

Do not claim causation unless evidence supports it.

Use:

**Observed fact → calculation → interpretation → possible explanation**

---

# 14. "CAN LAST YEAR HAPPEN AGAIN?"

Support:

> Last year sales declined in Q3. Is a similar pattern appearing this year?

Process:

```text
Historical data
 ↓
Current data
 ↓
Compare patterns
 ↓
Trend similarity
 ↓
Scenario/forecast if appropriate
 ↓
Explain uncertainty
```

Use language such as:

- "A similar pattern is visible."
- "Current data shows signs consistent with..."
- "If the current trend continues..."
- "This does not guarantee the same outcome."

Never claim certainty about future events.

---

# 15. SCENARIO / WHAT-IF ANALYSIS

Implement deterministic scenarios such as:

> What happens if expenses increase by 10%?

> What happens if revenue grows by 15%?

> What happens if price changes by 5%?

Return:

- baseline
- scenario
- difference
- assumptions
- visualization where useful

Clearly label scenario results as estimates, not actual outcomes.

---

# 16. ON-DEMAND VISUALIZATION

This is a major feature.

User can ask:

> Show monthly revenue.

> Compare this year's sales with last year's.

> Show product performance.

> Show regional sales.

> Show expense distribution.

> Show revenue vs profit.

The agent chooses an appropriate chart from available data.

Support:

- line
- bar
- grouped bar
- stacked bar
- pie/donut
- area
- scatter
- histogram
- KPI cards
- comparison charts

Use Plotly for interactive charts.

Do NOT claim to replace Power BI.

Describe this as:

**on-demand business intelligence visualization.**

Before creating a chart:

- verify columns
- verify data types
- handle missing values
- choose correct aggregation
- use clear title/axes
- prevent misleading charts

---

# 17. NATURAL-LANGUAGE DASHBOARD

Add an excellent optional feature:

User:

> Create a dashboard for 2025 business performance.

The system automatically selects relevant:

- KPI cards
- revenue chart
- profit chart
- expense chart
- product chart
- regional chart

Only show charts supported by the uploaded data.

---

# 18. REPORT GENERATION

Generate:

```text
BUSINESS PERFORMANCE REPORT

1. Executive Summary
2. Key Performance Indicators
3. Revenue Analysis
4. Profit Analysis
5. Expense Analysis
6. Product Performance
7. Regional Performance
8. Historical Comparison
9. Trend Analysis
10. Scenario Analysis
11. Key Findings
12. AI Suggestions
13. Risks and Assumptions
14. Sources and Evidence
```

Do not include unsupported sections.

Allow report export to PDF/HTML where practical.

Include charts, tables, findings, assumptions and sources.

---

# 19. EVIDENCE-GROUNDED SUGGESTIONS

Suggestions must be based on retrieved evidence and analytics.

Use:

```text
Recommendation
↓
Reason
↓
Evidence
↓
Assumptions
↓
Risk
↓
Suggested next step
```

Example:

> The sales data shows sustained growth in Region B. A controlled regional expansion pilot could be considered, subject to cost and market validation.

Do not guarantee profit or business growth.

---

# 20. EVIDENCE PANEL

For each answer/report, show:

```text
Evidence Used

1. Annual_Report_2025.pdf
   Page: 31

2. Sales_2025.xlsx
   Sheet: Sales

3. Expenses.csv
```

Allow users to inspect retrieved context where practical.

---

# 21. EVIDENCE QUALITY

Use qualitative evidence status instead of fake confidence numbers.

Examples:

```text
Evidence Quality: Strong
```

or

```text
Evidence Quality: Limited
```

Explain why.

Never invent a confidence percentage.

---

# 22. STREAMLIT UI

Create a professional UI.

## Home

- AUREX branding
- project description
- system status
- documents
- dataset summary

## Upload

- multiple-file upload
- ingestion status
- errors
- document list

## AI Business Analyst

- chat
- answers
- charts
- tables
- evidence
- assumptions

## Dashboard

- dynamic KPI cards
- charts
- trends
- comparisons

## Data Explorer

- rows
- columns
- data types
- missing values
- statistics

## Reports

- generate
- preview
- export

## Evaluation

- retrieval metrics
- answer metrics
- numerical accuracy
- latency

---

# 23. FASTAPI

Implement:

```text
GET  /health
POST /documents/upload
POST /documents/ingest
GET  /documents
DELETE /documents/{document_id}
POST /query
POST /search
POST /analyze
POST /visualize
POST /report
POST /scenario
GET  /evaluation
```

Use Pydantic schemas and OpenAPI documentation.

---

# 24. PROJECT STRUCTURE

Use a clean modular structure similar to:

```text
aurex/
├── app/
│   ├── main.py
│   ├── api/routes/
│   ├── core/
│   ├── ingestion/
│   ├── rag/
│   ├── agents/
│   ├── tools/
│   ├── analytics/
│   ├── visualization/
│   ├── reports/
│   ├── evaluation/
│   └── models/
├── frontend/
│   ├── streamlit_app.py
│   ├── pages/
│   └── components/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── docs/
├── scripts/
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

Adapt where needed, but maintain separation of concerns.

---

# 25. STORAGE

Use SQLite for lightweight application metadata if needed.

Store:

- document records
- ingestion status
- dataset metadata
- analysis history where appropriate

Use ChromaDB/FAISS for vector data.

Do not store secrets.

---

# 26. SAMPLE DATA

Create small synthetic/demo files for testing:

```text
sample_sales.csv
sample_finance.xlsx
sample_annual_report.pdf
```

Clearly label them as demo/synthetic.

Never present synthetic data as real company data.

---

# 27. SECURITY

Implement:

- environment variables
- no hardcoded secrets
- upload validation
- safe filenames
- file size limits
- allowed extensions
- path traversal protection
- temporary file cleanup

Do not expose stack traces to users.

---

# 28. LOGGING

Log:

- ingestion events
- document IDs
- retrieval events
- agent tool selection
- analytics operations
- errors
- latency

Do not unnecessarily log sensitive document contents.

---

# 29. EVALUATION

Create realistic evaluation questions:

```text
What was total revenue in 2025?
Which product had the highest sales?
Compare 2024 and 2025 revenue.
Which region declined?
What caused the expense increase?
Show monthly revenue.
What happens if expenses increase by 10%?
Is the current trend similar to last year?
```

Measure where applicable:

### Retrieval
- Hit Rate
- Recall@K
- Precision@K
- MRR

### RAG
- Faithfulness
- Answer relevance
- Context relevance
- Citation correctness

### Numerical
- calculation correctness
- comparison correctness
- scenario correctness

### Visualization
- correct chart type
- correct columns
- correct aggregation

### System
- latency
- error rate

Never invent metrics. Display actual measured results only.

---

# 30. TESTING

Implement:

## Unit tests

- PDF parser
- Excel parser
- CSV parser
- profiling
- metadata
- chunking
- retrieval
- calculations
- chart generation
- citations

## Integration tests

```text
Upload
→ Ingest
→ Index
→ Retrieve
→ Analyze
→ Generate
```

## End-to-end tests

Test complete user workflows.

---

# 31. PROMPT ENGINEERING

Create separate prompts for:

- intent detection
- retrieval query generation
- answer generation
- report generation
- recommendation generation
- chart selection

All prompts must instruct:

- use supplied evidence
- never invent values
- never invent sources
- distinguish facts from recommendations
- state uncertainty
- use analytics results when available

---

# 32. ERROR HANDLING

Handle:

- unsupported files
- corrupt PDFs
- malformed Excel
- malformed CSV
- missing columns
- empty data
- OCR failures
- embedding failures
- vector DB failures
- unavailable LLM
- invalid queries
- visualization failures
- insufficient evidence

Return useful user-friendly messages.

---

# 33. ADDITIONAL EXCELLENT FEATURES

Implement these if reliable:

### Dataset Health Report

```text
Rows: 10,000
Missing values: 2.4%
Duplicate rows: 0.3%
Date coverage: 2022–2025
```

### Explain This Chart

User selects a chart and asks:

> Explain this trend.

The system explains using the underlying data and evidence.

### What-If Controls

Streamlit sliders for:

- revenue growth
- expense increase
- price change

Then recalculate the scenario.

### Follow-up Context

Support:

```text
Compare 2024 and 2025.
→ Now show it by region.
→ Which region caused the decline?
```

Maintain controlled session context.

---

# 34. SAFETY / BUSINESS RULES

Never:

- guarantee profit
- guarantee business growth
- guarantee future events
- fabricate data
- fabricate sources
- invent missing values
- confuse scenarios with actual results
- present assumptions as facts

Use:

**Facts → Calculations → Interpretation → Recommendation**

---

# 35. FUTURE SCOPE

Do not implement now, but document:

```text
Current:
Files → RAG → Agent → Analytics → Visualization → Report

Future:
APIs / ERP / CRM / Email
→ Automated Pipeline
→ Real-time Monitoring
→ Multiple Specialized Agents
→ Human-approved Actions
→ Enterprise Deployment
```

---

# 36. README

Create a professional README with:

1. Project title
2. Problem
3. Solution
4. Features
5. Architecture
6. Technology stack
7. Supported formats
8. RAG workflow
9. Agent workflow
10. Analytics
11. Visualization
12. Example queries
13. Screenshots
14. Installation
15. Configuration
16. Local execution
17. Docker
18. Evaluation
19. Limitations
20. Future scope
21. Roadmap
22. License

Include:

> AUREX is a decision-support and analytical system. Its recommendations are evidence-grounded suggestions and should not be treated as guaranteed financial outcomes.

---

# 37. DOCUMENTATION

Create:

```text
docs/
├── architecture.md
├── rag_pipeline.md
├── agent.md
├── analytics.md
├── visualization.md
├── evaluation.md
└── api.md
```

Document important technical decisions.

---

# 38. DEVELOPMENT METHOD

DO NOT generate everything blindly in one step.

Build incrementally:

### Stage 1
Inspect repository and create architecture.

### Stage 2
Project scaffolding.

### Stage 3
FastAPI health endpoint.

### Stage 4
Streamlit shell.

### Stage 5
PDF ingestion.

### Stage 6
Excel/CSV ingestion.

### Stage 7
Metadata + profiling.

### Stage 8
Embeddings + ChromaDB.

### Stage 9
RAG retrieval.

### Stage 10
RAG generation + citations.

### Stage 11
Analytics engine.

### Stage 12
Visualization engine.

### Stage 13
AI Agent.

### Stage 14
Historical comparison.

### Stage 15
Scenario engine.

### Stage 16
Report generation.

### Stage 17
Evaluation.

### Stage 18
Testing.

### Stage 19
Docker.

### Stage 20
README/documentation.

After EVERY stage:

1. Run tests.
2. Run the application.
3. Fix errors.
4. Verify functionality.
5. Update documentation.
6. Only continue when the current stage works.

---

# 39. CODING RULES

- Python only.
- Clean modular architecture.
- Type hints.
- Pydantic models.
- No hardcoded secrets.
- Environment configuration.
- Proper exception handling.
- Logging.
- Reusable services.
- Small functions.
- Clear naming.
- Avoid unnecessary dependencies.
- Prefer free/open-source components.
- Do not implement fake functionality.

If a feature cannot be implemented reliably, document it rather than faking it.

Do not delete useful existing work.

---

# 40. FINAL QUALITY GATE

Before declaring complete:

### Data
- [ ] PDF works
- [ ] Excel works
- [ ] CSV works
- [ ] metadata works
- [ ] profiling works

### RAG
- [ ] embeddings work
- [ ] vector DB works
- [ ] retrieval works
- [ ] citations work
- [ ] insufficient-evidence handling works

### Analytics
- [ ] KPI calculation works
- [ ] historical comparison works
- [ ] trend analysis works
- [ ] scenario analysis works

### Agent
- [ ] intent detection works
- [ ] tool selection works
- [ ] bounded execution works
- [ ] errors handled

### Visualization
- [ ] natural-language chart requests work
- [ ] chart selection works
- [ ] validation works
- [ ] interactive charts work

### Reports
- [ ] report generation works
- [ ] evidence included
- [ ] charts included
- [ ] assumptions included
- [ ] export works

### Application
- [ ] FastAPI works
- [ ] Streamlit works
- [ ] Docker works
- [ ] tests pass
- [ ] README complete
- [ ] documentation complete
- [ ] no secrets committed

---

# 41. FINAL PRODUCT

The final system should behave like an:

## AI Business Analyst

Technically:

**Multimodal RAG + Agentic Tool Use + Structured Data Analytics + On-Demand Visualization + Evidence-Grounded Reporting**

Example:

```text
User:
Analyze our business performance this year compared with last year.
Show important graphs and tell me what we should focus on.

        ↓

     AI AGENT

        ↓

Retrieve PDF / Excel / CSV

        ↓

Analyze data

        ↓

Compare historical periods

        ↓

Detect important trends

        ↓

Select visualizations

        ↓

Generate charts

        ↓

Generate evidence-grounded suggestions

        ↓

FINAL REPORT

Executive Summary
KPI Comparison
Revenue Chart
Profit Chart
Product Analysis
Regional Analysis
Historical Comparison
Key Findings
Suggestions
Risks & Assumptions
Sources / Evidence
```

---

# 42. FINAL INSTRUCTION

Start by inspecting the existing KIRO repository.

Do not ask unnecessary clarification questions because this specification is the source of truth.

Build incrementally.

At each stage report:

- what was implemented
- files changed
- tests executed
- problems found
- fixes applied
- next stage

Do not claim completion until the feature actually works.

Prioritize:

**Correctness > Reliability > Maintainability > Fancy Features**

The final project must be demonstrable in a B.Tech project presentation/viva and suitable for GitHub, LinkedIn and a technical resume.

# AUREX
## Multimodal RAG-Based Business Intelligence and Decision Support System

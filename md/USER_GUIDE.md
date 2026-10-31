# AUREX User Guide

Complete guide for using the AUREX Business Intelligence System.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Uploading Documents](#uploading-documents)
3. [Asking Questions](#asking-questions)
4. [Using the Dashboard](#using-the-dashboard)
5. [Generating Reports](#generating-reports)
6. [Tips & Best Practices](#tips--best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQs](#faqs)

---

## Getting Started

### First Time Setup

1. **Start the Application**
   - Windows: Double-click `START_AUREX.bat`
   - Linux/Mac: Run `./start_aurex.sh`
   - Docker: Run `docker-compose up -d`

2. **Access the Interface**
   - Open browser: http://localhost:8501
   - You'll see the AUREX homepage with navigation menu

3. **Verify System Status**
   - Backend should be running on port 8000
   - Ollama should be running with llama3.1:8b model
   - ChromaDB will initialize automatically

### Navigation

AUREX has 4 main pages accessible from the sidebar:

📤 **Upload** - Upload and ingest business documents  
🤖 **AI Business Analyst** - Ask questions and get insights  
📊 **Dashboard** - View analytics and visualizations  
📄 **Reports** - Generate professional business reports  

---

## Uploading Documents

### Supported File Types

- **PDF**: Business reports, invoices, contracts, presentations
- **Excel (.xlsx)**: Financial statements, sales data, inventory
- **CSV**: Transaction logs, customer data, metrics

### How to Upload

1. **Navigate to Upload Page**
   - Click "📤 Upload" in the sidebar

2. **Select Document**
   - Click "Browse files" or drag-and-drop
   - Choose your document

3. **Upload**
   - Click "Upload Document"
   - Wait for confirmation message

4. **Ingest (Process)**
   - After upload, click "Ingest Document"
   - This extracts content and creates searchable embeddings
   - Processing time: 5-30 seconds depending on size

5. **Verify**
   - Check "Uploaded Documents" section
   - Status should show "Ready" or "Indexed"

### Document Requirements

**PDF Documents:**
- Maximum size: 100MB
- Pages: Any number
- Format: Text-based or scanned (OCR supported)
- Best quality: Clean formatting, clear text

**Excel Files:**
- Maximum size: 50MB
- Sheets: Multiple sheets supported
- Format: .xlsx (not .xls)
- Best quality: Clear headers, structured data

**CSV Files:**
- Maximum size: 50MB
- Encoding: UTF-8 preferred
- Format: Standard CSV with headers
- Best quality: Consistent delimiters, clean data

### Tips for Better Results

✅ **DO:**
- Use clear, descriptive filenames
- Upload complete documents (all pages)
- Use high-quality scans for PDFs
- Include headers in Excel/CSV files
- Upload documents in chronological order

❌ **DON'T:**
- Upload corrupted or password-protected files
- Use extremely large files (>100MB)
- Upload duplicate documents
- Use inconsistent data formats

---

## Asking Questions

### Basic Questions

Navigate to **AI Business Analyst** page and ask questions in natural language.

#### Example Questions

**Financial Queries:**
- "What was the total revenue in 2025?"
- "What is the profit margin?"
- "How much did we spend on marketing?"
- "What was the net profit last quarter?"

**Product Analysis:**
- "Which product generated the highest sales?"
- "List the top 3 products by revenue"
- "What is the performance of Product A?"
- "Compare sales of Product A and Product B"

**Regional Analysis:**
- "Which region has the highest revenue?"
- "What are the sales figures for the North region?"
- "Compare performance across all regions"

**Trend Analysis:**
- "Is revenue increasing or decreasing?"
- "Show quarterly revenue trends"
- "What is the growth rate compared to last year?"

**Comparative Queries:**
- "Compare Q1 and Q2 revenue"
- "What is the year-over-year growth?"
- "How does 2025 compare to 2024?"

### Advanced Queries

**Multi-Metric:**
- "Show revenue, profit, and margin for 2025"
- "What are all the key performance indicators?"

**Conditional:**
- "Which products have profit margin above 20%?"
- "List regions where revenue exceeds 100 Lakhs"

**Aggregation:**
- "What is the average monthly revenue?"
- "Calculate total expenses across all categories"

### Question Format Tips

✅ **Good Questions:**
- Clear and specific
- Include time periods when relevant
- Mention specific metrics
- Use business terminology

❌ **Avoid:**
- Vague questions ("Tell me about the business")
- Multiple unrelated questions in one query
- Questions about data not in documents

### Understanding Answers

Each answer includes:

1. **Answer Text**: AI-generated response
2. **Sources**: Documents and pages used
3. **Relevance Score**: How confident the system is
4. **Processing Time**: How long it took

**Example Answer:**
```
Answer: The total revenue in 2025 was 450 Lakhs according to 
the business performance report.

Sources:
- Document: report_2025.pdf
- Page: 3
- Relevance: 0.87
```

### Follow-up Questions

You can ask follow-up questions based on previous answers:
1. "Tell me more about that"
2. "What about profit?"
3. "Show me the breakdown"
4. "What caused this increase?"

---

## Using the Dashboard

The Dashboard provides real-time analytics and visualizations.

### Dashboard Components

1. **KPI Cards**
   - Revenue, Profit, Margin, Product Count
   - Shows current values
   - Color-coded indicators

2. **Charts**
   - Revenue trends (line chart)
   - Product distribution (bar chart)
   - Regional performance (pie chart)
   - Profit margin gauge

3. **Filters**
   - Document ID filter (sidebar)
   - Time period filter (coming soon)
   - Metric selector (coming soon)

### How to Use Dashboard

1. **Navigate to Dashboard**
   - Click "📊 Dashboard" in sidebar

2. **View KPIs**
   - See key metrics at the top
   - Check for percentage changes
   - Note any trends

3. **Explore Charts**
   - Hover over data points for details
   - Click legend items to show/hide
   - Zoom in/out on charts
   - Pan across time series

4. **Filter Data**
   - Enter document ID in sidebar (optional)
   - Click "Refresh Data" to update
   - Charts update automatically

5. **Export**
   - Right-click chart → "Save as image"
   - Use browser print function for PDF

### Chart Types

**Indicator Cards**
- Single metric display
- Shows value and change
- Example: "Total Revenue: 450 L"

**Bar Charts**
- Compare categories
- Example: Sales by product

**Line Charts**
- Show trends over time
- Example: Quarterly revenue

**Pie Charts**
- Show distribution
- Example: Regional market share

**Gauge Charts**
- Show progress toward goal
- Example: Profit margin vs target

### Dashboard Tips

✅ **DO:**
- Refresh regularly for latest data
- Use filters to focus analysis
- Explore interactive features
- Export important charts

❌ **DON'T:**
- Overload with too many filters
- Ignore data source information
- Rely on cached data

---

## Generating Reports

Create professional business reports with automated insights.

### Report Types

**Executive Report**
- High-level summary
- Key insights only
- Best for: Management presentations
- Length: 2-3 pages

**Detailed Report**
- Comprehensive analysis
- All available metrics
- Best for: In-depth review
- Length: 5-10 pages

**Summary Report**
- Quick overview
- Essential KPIs
- Best for: Status updates
- Length: 1-2 pages

### How to Generate Reports

1. **Navigate to Reports Page**
   - Click "📄 Reports" in sidebar

2. **Configure Report**
   - Select report type (Executive/Detailed/Summary)
   - Choose format (HTML/Markdown/JSON)
   - Optionally enter document ID filter
   - Add optional title/description

3. **Generate**
   - Click "Generate Report"
   - Wait 15-30 seconds for processing
   - System will show progress

4. **Review**
   - Read generated summary
   - Check insights and recommendations
   - Verify source citations

5. **Download or Preview**
   - Click "Download Report" for file
   - Click "Preview in Browser" for HTML reports
   - Share with stakeholders

### Report Content

All reports include:

**Executive Summary**
- Brief overview of business performance
- Key findings and trends

**KPI Section**
- Revenue, profit, margin
- Product and regional performance
- Growth metrics

**Insights**
- Data-driven observations
- Patterns and anomalies
- Comparative analysis

**Recommendations**
- Evidence-based suggestions
- Action items
- Risk considerations

**Sources**
- Document citations
- Page/sheet references
- Data provenance

### Report Formats

**HTML**
- ✅ Formatted with styling
- ✅ Easy to view in browser
- ✅ Can include charts (future)
- ✅ Best for: Sharing, presentations

**Markdown**
- ✅ Plain text with structure
- ✅ Easy to edit
- ✅ Version control friendly
- ✅ Best for: Documentation, collaboration

**JSON**
- ✅ Structured data
- ✅ Machine-readable
- ✅ API integration
- ✅ Best for: Automation, processing

### Customizing Reports

Current customizations:
- Report type
- Output format
- Document filter
- Title (optional)

Future enhancements:
- Custom sections
- Chart inclusion
- Branding/logo
- Email delivery

### Report Tips

✅ **DO:**
- Generate reports regularly
- Archive important reports
- Review recommendations carefully
- Share with relevant stakeholders

❌ **DON'T:**
- Generate without reviewing data
- Ignore source citations
- Over-rely on automated insights
- Share sensitive data without authorization

---

## Tips & Best Practices

### Document Management

1. **Naming Convention**
   - Use descriptive names: `Q1_Report_2025.pdf`
   - Include dates: `Sales_January_2025.xlsx`
   - Avoid special characters

2. **Organization**
   - Upload documents by period
   - Keep similar documents together
   - Delete outdated documents

3. **Quality**
   - Ensure documents are complete
   - Use high-resolution scans
   - Verify data accuracy before upload

### Query Optimization

1. **Be Specific**
   ```
   ❌ "What about sales?"
   ✅ "What was the total sales revenue in Q1 2025?"
   ```

2. **Include Context**
   ```
   ❌ "Show trends"
   ✅ "Show quarterly revenue trends for 2025"
   ```

3. **One Topic Per Question**
   ```
   ❌ "What are revenue, profit, and top products?"
   ✅ "What was the total revenue?" (then ask about profit)
   ```

### Performance Optimization

1. **Upload Management**
   - Upload during off-peak hours
   - Process large files individually
   - Delete unused documents

2. **Query Efficiency**
   - Use document filters when possible
   - Ask focused questions
   - Avoid very broad queries

3. **System Maintenance**
   - Restart services periodically
   - Clear browser cache if slow
   - Monitor disk space

---

## Troubleshooting

### Common Issues

**1. Document Won't Upload**

*Symptoms:* Error message during upload

*Solutions:*
- Check file size (<100MB)
- Verify file type (PDF/Excel/CSV)
- Ensure file is not corrupted
- Try different browser
- Check disk space

**2. Slow Query Response**

*Symptoms:* Questions take too long

*Solutions:*
- Simplify question
- Use document filter
- Check Ollama is running
- Restart backend service
- Reduce number of uploaded documents

**3. No Answer Returned**

*Symptoms:* "No information available"

*Solutions:*
- Verify documents are ingested
- Rephrase question
- Check document contains relevant data
- Try broader question first

**4. Dashboard Not Loading**

*Symptoms:* Blank or error on dashboard

*Solutions:*
- Check documents are uploaded
- Click "Refresh Data"
- Verify backend is running
- Clear browser cache
- Check browser console for errors

**5. Report Generation Failed**

*Symptoms:* Error when generating report

*Solutions:*
- Ensure documents are ingested
- Try different report type
- Use simpler format (JSON first)
- Check available disk space
- Review backend logs

### Getting Help

1. **Check Logs**
   - Backend logs in console
   - Frontend errors in browser console

2. **Restart Services**
   ```bash
   # Windows
   START_AUREX.bat
   
   # Docker
   docker-compose restart
   ```

3. **Verify System**
   - http://localhost:8000/api/health
   - Check Ollama: http://localhost:11434/api/tags

4. **Contact Support**
   - GitHub Issues
   - Email support
   - Documentation

---

## FAQs

### General

**Q: What file types are supported?**  
A: PDF, Excel (.xlsx), and CSV files.

**Q: Is my data secure?**  
A: Yes, all processing is done locally. No data leaves your machine.

**Q: Can I use AUREX offline?**  
A: Yes, once Ollama is set up, no internet is required.

**Q: How many documents can I upload?**  
A: No strict limit, but performance depends on system resources.

### Documents

**Q: Can I upload scanned PDFs?**  
A: Yes, OCR support is available for scanned documents.

**Q: What if my Excel file has multiple sheets?**  
A: All sheets are processed automatically.

**Q: Can I delete uploaded documents?**  
A: Yes, use the delete button in the Upload page.

**Q: Do I need to re-upload documents after restart?**  
A: No, documents are persisted in ChromaDB.

### Queries

**Q: Can I ask questions in other languages?**  
A: Currently English only. Multi-language support planned.

**Q: Why does the same question give different answers?**  
A: LLM responses can vary slightly. Use source citations to verify.

**Q: Can I see query history?**  
A: Not currently, but feature is planned.

**Q: How many sources are used per query?**  
A: Default is top 5 most relevant chunks. Configurable in settings.

### Analytics

**Q: How are KPIs extracted?**  
A: Using LLM-based extraction with numerical pattern matching.

**Q: Can I customize KPI definitions?**  
A: Not currently. Future enhancement planned.

**Q: Why don't I see all metrics?**  
A: Metrics depend on data available in uploaded documents.

### Reports

**Q: Can I schedule automatic reports?**  
A: Not currently. Manual generation only.

**Q: Can I customize report templates?**  
A: Not currently. Pre-defined templates only.

**Q: Where are reports saved?**  
A: In `data/reports/` directory.

**Q: Can I email reports directly?**  
A: Not currently. Download and email manually.

---

## Advanced Features

### Custom Configurations

Edit `.env` file for custom settings:

```env
# Number of documents to retrieve
TOP_K=5

# Similarity threshold (0-1)
SIMILARITY_THRESHOLD=0.3

# LLM model
OLLAMA_MODEL=llama3.1:8b
```

### API Usage

For programmatic access, use the REST API:

```python
import httpx

# Query example
response = httpx.post(
    "http://localhost:8000/api/query",
    json={"question": "What was the revenue?"}
)
print(response.json())
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full API reference.

### Docker Deployment

For production deployment:

```bash
# Production
docker-compose up -d

# Development (with hot-reload)
docker-compose -f docker-compose.dev.yml up -d
```

See [DOCKER.md](DOCKER.md) for detailed deployment guide.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Enter` | Submit query (AI Analyst page) |
| `Ctrl + R` | Refresh dashboard |
| `Esc` | Clear input field |

---

## Glossary

**RAG**: Retrieval-Augmented Generation - AI technique combining search and generation

**KPI**: Key Performance Indicator - Measurable business metric

**Embedding**: Numerical representation of text for similarity search

**Vector Store**: Database for storing and searching embeddings

**LLM**: Large Language Model - AI for text generation

**Chunk**: Small segment of document for processing

**Similarity Score**: How relevant a document chunk is to query (0-1)

---

## Getting More Help

- **Documentation**: Check [README.md](README.md)
- **API Docs**: http://localhost:8000/docs
- **GitHub Issues**: Report bugs and request features
- **Email Support**: your.email@example.com

---

**Last Updated**: September 2026  
**Version**: 1.0.0

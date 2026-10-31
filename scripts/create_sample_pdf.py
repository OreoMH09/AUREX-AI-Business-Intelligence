"""
Create Sample PDF for Testing
Generates a simple PDF with business data
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pathlib import Path


def create_sample_business_report():
    """Create a sample business report PDF"""
    
    output_dir = Path("data/sample")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "sample_business_report_2025.pdf"
    
    # Create PDF
    doc = SimpleDocTemplate(
        str(output_file),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    
    # Container for elements
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story.append(Paragraph("Business Performance Report 2025", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Executive Summary Section
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    summary_text = """
    The company achieved strong financial performance in 2025, with total revenue reaching ₹94 lakhs, 
    representing a 17.5% increase compared to 2024. Profit margins improved to 22%, and all major 
    product categories showed positive growth.
    """
    story.append(Paragraph(summary_text, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Financial Performance Section
    story.append(Paragraph("Financial Performance", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    # Revenue Table
    revenue_data = [
        ['Year', 'Revenue (₹ Lakhs)', 'Profit (₹ Lakhs)', 'Margin (%)'],
        ['2023', '75', '15', '20'],
        ['2024', '80', '16', '20'],
        ['2025', '94', '20.68', '22'],
    ]
    
    revenue_table = Table(revenue_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    revenue_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(revenue_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Product Performance Section
    story.append(Paragraph("Product Performance", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    product_data = [
        ['Product', 'Sales (₹ Lakhs)', 'Units Sold', 'Growth (%)'],
        ['Product A', '35', '1200', '15'],
        ['Product B', '28', '950', '20'],
        ['Product C', '20', '800', '10'],
        ['Product D', '11', '450', '25'],
    ]
    
    product_table = Table(product_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(product_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Regional Performance
    story.append(Paragraph("Regional Performance", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    regional_data = [
        ['Region', 'Sales (₹ Lakhs)', 'Growth (%)'],
        ['Region A', '40', '18'],
        ['Region B', '32', '25'],
        ('Region C', '22', '-5'),
    ]
    
    regional_table = Table(regional_data, colWidths=[2*inch, 2*inch, 2*inch])
    regional_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff7f0e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(regional_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Key Findings
    story.append(Paragraph("Key Findings", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    findings = [
        "1. Revenue growth exceeded targets by 5%",
        "2. Product B showed the highest growth rate at 25%",
        "3. Region B emerged as the fastest-growing market",
        "4. Region C requires strategic intervention due to declining sales",
        "5. Overall profit margin improved from 20% to 22%"
    ]
    
    for finding in findings:
        story.append(Paragraph(finding, styles['BodyText']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Recommendations
    story.append(Paragraph("Recommendations", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    recommendations = """
    Based on the analysis, we recommend:
    
    • Increase investment in Product B and Product D given their high growth rates
    • Investigate the cause of decline in Region C and develop a recovery plan
    • Expand operations in Region B to capitalize on strong market demand
    • Maintain focus on operational efficiency to sustain improved profit margins
    """
    
    story.append(Paragraph(recommendations, styles['BodyText']))
    
    # Build PDF
    doc.build(story)
    
    print(f"Sample PDF created: {output_file}")
    return output_file


if __name__ == "__main__":
    try:
        create_sample_business_report()
        print("✅ Sample PDF generated successfully!")
    except ImportError:
        print("⚠️  reportlab not installed. Install with: pip install reportlab")
    except Exception as e:
        print(f"❌ Error creating sample PDF: {e}")

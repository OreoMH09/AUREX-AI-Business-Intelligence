"""
AUREX Excel Parser
Parses Excel files (.xlsx, .xls) and extracts data
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.ingestion.base import ParsedDocument, DocumentChunk
from app.core import get_logger

logger = get_logger(__name__)


class ExcelParser:
    """Parser for Excel files"""
    
    def __init__(self):
        """Initialize Excel parser"""
        logger.info("ExcelParser initialized")
    
    def parse(self, file_path: Path) -> ParsedDocument:
        """
        Parse an Excel file
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            ParsedDocument with extracted data
        """
        try:
            logger.info(f"Parsing Excel file: {file_path}")
            
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            logger.info(f"Found {len(sheet_names)} sheets: {sheet_names}")
            
            # Extract metadata
            metadata = {
                "file_name": file_path.name,
                "file_size": file_path.stat().st_size,
                "sheet_count": len(sheet_names),
                "sheet_names": sheet_names,
                "parsed_at": datetime.utcnow().isoformat()
            }
            
            # Parse each sheet
            chunks = []
            tables = []
            full_text = []
            
            for sheet_name in sheet_names:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    
                    # Skip empty sheets
                    if df.empty:
                        logger.warning(f"Sheet '{sheet_name}' is empty, skipping")
                        continue
                    
                    # Extract sheet info
                    sheet_info = {
                        "sheet_name": sheet_name,
                        "rows": len(df),
                        "columns": len(df.columns),
                        "column_names": df.columns.tolist()
                    }
                    
                    # Convert to text representation
                    text_lines = [f"Sheet: {sheet_name}"]
                    text_lines.append(f"Columns: {', '.join(df.columns.tolist())}")
                    text_lines.append("")
                    
                    # Add rows as text
                    for idx, row in df.iterrows():
                        row_text = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                        text_lines.append(row_text)
                    
                    sheet_text = "\n".join(text_lines)
                    full_text.append(sheet_text)
                    
                    # Create chunk for this sheet
                    chunk = DocumentChunk(
                        chunk_id=f"sheet_{sheet_name}",
                        content=sheet_text,
                        metadata={
                            "sheet_name": sheet_name,
                            "chunk_type": "sheet",
                            **sheet_info
                        },
                        page_number=sheet_names.index(sheet_name) + 1
                    )
                    chunks.append(chunk)
                    
                    # Store table data
                    tables.append({
                        "sheet_name": sheet_name,
                        "data": df.to_dict('records'),
                        "columns": df.columns.tolist(),
                        "shape": df.shape
                    })
                    
                    logger.info(f"Parsed sheet '{sheet_name}': {len(df)} rows, {len(df.columns)} columns")
                    
                except Exception as e:
                    logger.error(f"Error parsing sheet '{sheet_name}': {e}")
                    continue
            
            # Combine all text
            combined_text = "\n\n".join(full_text)
            
            # Add summary metadata
            metadata["total_rows"] = sum(len(df) for df in [pd.read_excel(file_path, sheet_name=sn) for sn in sheet_names])
            metadata["total_chunks"] = len(chunks)
            
            parsed_doc = ParsedDocument(
                text=combined_text,
                chunks=chunks,
                metadata=metadata,
                tables=tables,
                page_count=len(sheet_names)
            )
            
            logger.info(f"Excel file parsed successfully: {len(chunks)} chunks, {len(tables)} tables")
            return parsed_doc
            
        except Exception as e:
            logger.error(f"Error parsing Excel file {file_path}: {e}", exc_info=True)
            raise
    
    def extract_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract summary statistics from a DataFrame
        
        Args:
            df: DataFrame to summarize
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object', 'category']).columns.tolist()
        }
        
        # Add numeric statistics if available
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            summary["numeric_stats"] = df[numeric_cols].describe().to_dict()
        
        return summary

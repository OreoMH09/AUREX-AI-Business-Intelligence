"""
AUREX CSV Parser
Parses CSV files and extracts data
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from app.ingestion.base import ParsedDocument, DocumentChunk
from app.core import get_logger

logger = get_logger(__name__)


class CSVParser:
    """Parser for CSV files"""
    
    def __init__(self, encoding: str = 'utf-8'):
        """
        Initialize CSV parser
        
        Args:
            encoding: File encoding (default: utf-8)
        """
        self.encoding = encoding
        logger.info(f"CSVParser initialized with encoding: {encoding}")
    
    def parse(self, file_path: Path) -> ParsedDocument:
        """
        Parse a CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            ParsedDocument with extracted data
        """
        try:
            logger.info(f"Parsing CSV file: {file_path}")
            
            # Try reading with default encoding
            try:
                df = pd.read_csv(file_path, encoding=self.encoding)
            except UnicodeDecodeError:
                # Try common alternative encodings
                logger.warning(f"UTF-8 decoding failed, trying latin-1")
                df = pd.read_csv(file_path, encoding='latin-1')
            
            logger.info(f"CSV loaded: {len(df)} rows, {len(df.columns)} columns")
            
            # Extract metadata
            metadata = {
                "file_name": file_path.name,
                "file_size": file_path.stat().st_size,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "parsed_at": datetime.utcnow().isoformat()
            }
            
            # Create text representation
            text_lines = [f"CSV File: {file_path.name}"]
            text_lines.append(f"Columns: {', '.join(df.columns.tolist())}")
            text_lines.append(f"Total Rows: {len(df)}")
            text_lines.append("")
            
            # Add sample rows as text
            for idx, row in df.iterrows():
                row_text = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                text_lines.append(row_text)
            
            full_text = "\n".join(text_lines)
            
            # Create chunks (split by rows if large)
            chunks = self._create_chunks(df, file_path.name)
            
            # Create table representation
            tables = [{
                "data": df.to_dict('records'),
                "columns": df.columns.tolist(),
                "shape": df.shape,
                "summary": self._extract_summary(df)
            }]
            
            parsed_doc = ParsedDocument(
                text=full_text,
                chunks=chunks,
                metadata=metadata,
                tables=tables,
                page_count=1
            )
            
            logger.info(f"CSV file parsed successfully: {len(chunks)} chunks")
            return parsed_doc
            
        except Exception as e:
            logger.error(f"Error parsing CSV file {file_path}: {e}", exc_info=True)
            raise
    
    def _create_chunks(self, df: pd.DataFrame, filename: str, chunk_size: int = 100) -> List[DocumentChunk]:
        """
        Create chunks from DataFrame
        
        Args:
            df: DataFrame to chunk
            filename: Source filename
            chunk_size: Number of rows per chunk
            
        Returns:
            List of DocumentChunks
        """
        chunks = []
        total_rows = len(df)
        
        # If DataFrame is small, create single chunk
        if total_rows <= chunk_size:
            text_lines = []
            for idx, row in df.iterrows():
                row_text = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                text_lines.append(row_text)
            
            chunk = DocumentChunk(
                chunk_id=f"chunk_0",
                content="\n".join(text_lines),
                metadata={
                    "filename": filename,
                    "chunk_type": "csv_data",
                    "rows": total_rows,
                    "columns": df.columns.tolist()
                },
                page_number=1
            )
            chunks.append(chunk)
        else:
            # Split into multiple chunks
            for i in range(0, total_rows, chunk_size):
                chunk_df = df.iloc[i:i+chunk_size]
                
                text_lines = []
                for idx, row in chunk_df.iterrows():
                    row_text = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                    text_lines.append(row_text)
                
                chunk = DocumentChunk(
                    chunk_id=f"chunk_{i//chunk_size}",
                    content="\n".join(text_lines),
                    metadata={
                        "filename": filename,
                        "chunk_type": "csv_data",
                        "rows": len(chunk_df),
                        "row_range": f"{i}-{i+len(chunk_df)}",
                        "columns": df.columns.tolist()
                    },
                    page_number=i//chunk_size + 1
                )
                chunks.append(chunk)
        
        return chunks
    
    def _extract_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract summary statistics from DataFrame
        
        Args:
            df: DataFrame to summarize
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            "shape": df.shape,
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

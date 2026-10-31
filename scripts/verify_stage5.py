"""
Stage 5 Verification Script
Verify that PDF ingestion works correctly
"""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ingestion.pdf_parser import PDFParser
from app.core import logger

def main():
    """Run verification tests"""
    print("=" * 60)
    print("STAGE 5 VERIFICATION - PDF INGESTION")
    print("=" * 60)
    print()
    
    # Test 1: PDF Parser Initialization
    print("TEST 1: PDF Parser Initialization")
    try:
        parser = PDFParser(enable_ocr=False)
        print("✅ PDF Parser initialized successfully")
        print(f"   Supported extensions: {parser.supported_extensions}")
        print(f"   OCR available: {parser.ocr_available}")
    except Exception as e:
        print(f"❌ PDF Parser initialization failed: {e}")
        return False
    
    print()
    
    # Test 2: Heading Detection
    print("TEST 2: Heading Detection Algorithm")
    test_headings = [
        ("1. Introduction", True),
        ("Chapter 1", True),
        ("EXECUTIVE SUMMARY", True),
        ("This is a very long sentence that should not be detected as a heading", False),
        ("ab", False),
    ]
    
    all_passed = True
    for text, expected in test_headings:
        result = parser._is_likely_heading(text)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{text[:50]}...' -> {result} (expected {expected})")
        if result != expected:
            all_passed = False
    
    if not all_passed:
        print("❌ Some heading detection tests failed")
        return False
    
    print()
    
    # Test 3: Check Sample Directory
    print("TEST 3: Sample Directory Structure")
    sample_dir = Path("data/sample")
    if sample_dir.exists():
        print(f"✅ Sample directory exists: {sample_dir}")
    else:
        print(f"⚠️  Sample directory not found (will be created on first use)")
    
    print()
    
    # Test 4: Import Checks
    print("TEST 4: Required Imports")
    required_modules = [
        ("fitz", "PyMuPDF"),
        ("PIL", "Pillow"),
        ("app.core", "Core module"),
        ("app.models", "Models module"),
        ("app.ingestion.base", "Base parser"),
    ]
    
    all_imported = True
    for module_name, description in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {description} ({module_name})")
        except ImportError as e:
            print(f"❌ {description} ({module_name}) - MISSING")
            all_imported = False
    
    if not all_imported:
        print("\n⚠️  Some dependencies are missing. Run: pip install -r requirements.txt")
        return False
    
    print()
    
    # Test 5: Document Service
    print("TEST 5: Document Service")
    try:
        from app.ingestion.document_service import document_service
        print("✅ Document service initialized")
        print(f"   Upload directory: {document_service.upload_dir}")
        print(f"   Documents in registry: {len(document_service.documents)}")
    except Exception as e:
        print(f"❌ Document service failed: {e}")
        return False
    
    print()
    
    # Summary
    print("=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    print()
    print("✅ Stage 5 PDF Ingestion is ready!")
    print()
    print("Next steps:")
    print("1. Generate sample PDF: python scripts/create_sample_pdf.py")
    print("2. Start backend: python app/main.py")
    print("3. Start frontend: streamlit run frontend/streamlit_app.py")
    print("4. Upload a PDF via the Upload page")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

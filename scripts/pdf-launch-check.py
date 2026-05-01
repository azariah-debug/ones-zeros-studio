#!/usr/bin/env python3
"""
PDF LAUNCH TRIPLE CHECK SYSTEM
Ones & Zeros Studio

Validates PDFs before shipping — checks pages, size, content, branding.
Usage: python3 pdf-launch-check.py /path/to/file.pdf
"""

import os
import sys

try:
    from pypdf import PdfReader
except ImportError:
    print("❌ pypdf not installed. Run: pip3 install pypdf")
    sys.exit(1)

def check_pdf(path):
    results = {"ok": False, "pages": 0, "size_kb": 0, "issues": [], "checks": {}}
    
    if not os.path.exists(path):
        results["issues"].append("FILE NOT FOUND")
        return results
    
    size_kb = os.path.getsize(path) / 1024
    results["size_kb"] = round(size_kb, 1)
    
    try:
        reader = PdfReader(path)
        pages = len(reader.pages)
        results["pages"] = pages
        results["checks"]["min_pages"] = pages >= 8
        results["checks"]["min_size"] = size_kb >= 30
        first_text = reader.pages[0].extract_text() if pages > 0 else ""
        results["checks"]["has_content"] = len(first_text) > 100
        results["checks"]["brand"] = "zeros" in first_text.lower() or "01" in first_text
        results["ok"] = all(results["checks"].values())
        
        if not results["ok"]:
            for check, passed in results["checks"].items():
                if not passed:
                    results["issues"].append(f"FAIL: {check}")
    except Exception as e:
        results["issues"].append(f"ERROR: {e}")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pdf-launch-check.py <file.pdf>")
        sys.exit(1)
    
    path = sys.argv[1]
    print(f"Checking: {path}")
    r = check_pdf(path)
    
    print(f"\nPages: {r['pages']}")
    print(f"Size: {r['size_kb']} KB")
    print(f"Status: {'✅ PASS' if r['ok'] else '❌ FAIL'}")
    
    for issue in r["issues"]:
        print(f"  → {issue}")
    
    for check, passed in r["checks"].items():
        icon = "✅" if passed else "❌"
        print(f"  {icon} {check}")
    
    sys.exit(0 if r["ok"] else 1)

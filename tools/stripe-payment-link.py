#!/usr/bin/env python3
"""
Stripe Payment Link Generator
Ones & Zeros Studio

Create Stripe payment links from the CLI.
Requires: stripe Python package + STRIPE_SECRET_KEY env var

Usage:
    python3 -c "$(curl -s https://raw.githubusercontent.com/azariah-debug/ones-zeros-studio/main/tools/stripe-payment-link.py)"
"""

import os
import sys
import json
import urllib.request

STRIPE_KEY = os.environ.get("STRIPE_SECRET_KEY") or os.environ.get("STRIPE_TEST_SECRET_KEY", "")

def create_payment_link(price_id, product_name=""):
    """Create a Stripe payment link for a given price ID."""
    if not STRIPE_KEY:
        print("❌ Set STRIPE_SECRET_KEY or STRIPE_TEST_SECRET_KEY environment variable")
        sys.exit(1)
    
    data = urllib.parse.urlencode({
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": "1",
        "metadata[product]": product_name,
    }).encode()
    
    req = urllib.request.Request(
        "https://api.stripe.com/v1/payment_links",
        data=data,
        headers={"Authorization": f"Bearer {STRIPE_KEY}"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            url = result.get("url", "")
            if url:
                print(f"✅ {product_name}: {url}")
            else:
                print(f"❌ {product_name}: {result}")
            return url
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 stripe-payment-link.py <price_id> [product_name]")
        print("Example: python3 stripe-payment-link.py price_abc123 'My Product'")
        sys.exit(1)
    
    price_id = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "Product"
    create_payment_link(price_id, name)

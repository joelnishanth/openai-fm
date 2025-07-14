import argparse
import os
import requests


LISTING_URL = os.getenv("LISTING_URL", "http://localhost:8000")
SCANNER_URL = os.getenv("SCANNER_URL", "http://localhost:8001")
DMCA_URL = os.getenv("DMCA_URL", "http://localhost:8002")


def main():
    parser = argparse.ArgumentParser(description="DMCA Process CLI")
    parser.add_argument("--shop-url", required=True)
    parser.add_argument("--auto-generate", action="store_true")
    parser.add_argument("--output-dir", default="./dmca_forms")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    resp = requests.post(f"{SCANNER_URL}/scan", json={"shop_url": args.shop_url})
    resp.raise_for_status()
    violations = resp.json()
    print(f"Found {len(violations)} potential violations")

    for v in violations:
        if args.auto_generate:
            g = requests.post(f"{DMCA_URL}/generate", json={"violation_id": v["id"]})
            g.raise_for_status()
            notice = g.json()["notice"]
            title = v["id"]
            path = os.path.join(args.output_dir, f"dmca_{title}.md")
            with open(path, "w") as f:
                f.write(notice)
            print(f"Saved notice to {path}")


if __name__ == "__main__":
    main()

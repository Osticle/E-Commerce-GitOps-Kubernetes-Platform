#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from ruamel.yaml import YAML

# Preserve YAML layout, indentation, and comments
yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

def sanitize_string(value: str) -> str:
    # Docker tags cannot contain slashes or invalid characters
    return re.sub(r'[^a-zA-Z0-9_.-]', '-', value).lower()

def parse_args():
    parser = argparse.ArgumentParser(description="Lint Helm chart and update image tag")
    parser.add_argument("--chart-dir", required=True, help="Path to Helm chart directory")
    parser.add_argument("--branch-name", default=os.getenv("CI_DEFAULT_BRANCH", "main"))
    parser.add_argument("--short-sha", default=os.getenv("CI_COMMIT_SHORT_SHA", "unknown"))
    parser.add_argument("--tag-version", default=os.getenv("CI_COMMIT_TAG", "v1.0.0"))
    return parser.parse_args()

def update_image_tag(values_file: Path, new_tag: str) -> bool:
    if not values_file.exists():
        print(f"[ERROR] values.yaml not found at: {values_file}")
        return False

    try:
        with open(values_file, "r", encoding="utf-8") as f:
            data = yaml.load(f)
    except Exception as e:
        print(f"[ERROR] Cannot parse YAML: {e}")
        return False

    if "image" not in data or not isinstance(data["image"], dict):
        print("[ERROR] Missing 'image' block in values.yaml")
        return False

    # Prevent deployment with 'latest' tag
    if new_tag.endswith("_latest") or new_tag == "latest":
        print(f"[ERROR] Rejected prohibited tag '{new_tag}'.")
        return False

    old_tag = data["image"].get("tag", "unknown")
    data["image"]["tag"] = new_tag

    try:
        with open(values_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
        print(f"[INFO] Updated image.tag: '{old_tag}' -> '{new_tag}'")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save values.yaml: {e}")
        return False

def lint_chart(chart_dir: Path) -> bool:
    print(f"[INFO] Running 'helm lint {chart_dir}'...")
    res = subprocess.run(["helm", "lint", str(chart_dir)], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Helm lint failed:\n{res.stdout}\n{res.stderr}")
        return False
    print("[INFO] Helm lint passed successfully.")
    return True

def main():
    args = parse_args()
    chart_dir = Path(args.chart_dir)
    values_file = chart_dir / "values.yaml"

    branch = sanitize_string(args.branch_name)
    tag_ver = sanitize_string(args.tag_version)
    computed_tag = f"{branch}_{args.short_sha}_{tag_ver}"

    # Step 1: Update only the image tag in values.yaml
    if not update_image_tag(values_file, computed_tag):
        sys.exit(1)

    # Step 2: Validate the whole chart structure
    if not lint_chart(chart_dir):
        sys.exit(1)

    print("[OK] Quality gate verified.")
    sys.exit(0)

if __name__ == "__main__":
    main()
#!/usr/bin/env bash
# Sync repo-root papers/ → app/assets/papers/ for Gradio runtime serving.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/papers"
DST="$ROOT/app/assets/papers"

if [[ ! -d "$SRC" ]]; then
  echo "Missing source directory: $SRC" >&2
  exit 1
fi

mkdir -p "$DST"
for pdf in "$SRC"/*.pdf; do
  base="$(basename "$pdf")"
  if [[ "$base" == "Aaron's_TOE_Complete.pdf" ]]; then
    cp "$pdf" "$DST/Aarons_TOE_Complete.pdf"
  else
    cp "$pdf" "$DST/$base"
  fi
done
echo "Synced $(ls -1 "$DST"/*.pdf | wc -l) PDFs to $DST"
#!/bin/bash
# pdl.sh - resumable parallel range-request downloader
# usage: pdl.sh URL OUTFILE TOTALSIZE CHUNKSIZE PARALLEL MAXTIME
URL="$1"; OUT="$2"; TOTAL="$3"; CS="$4"; PAR="$5"; MT="$6"
DIR="${OUT}.parts"; mkdir -p "$DIR"
N=$(( (TOTAL + CS - 1) / CS ))
declare -a pids=()
for ((i=0;i<N;i++)); do
  s=$((i*CS)); e=$((s+CS-1)); [ $e -ge $TOTAL ] && e=$((TOTAL-1))
  want=$((e-s+1))
  f="$DIR/part_$(printf %05d $i)"
  have=0; [ -f "$f" ] && have=$(stat -c %s "$f")
  if [ "$have" -ne "$want" ]; then
    curl -sL --max-time "$MT" -r "$s-$e" -o "$f" "$URL" &
    pids+=($!)
    if [ "${#pids[@]}" -ge "$PAR" ]; then wait "${pids[0]}"; pids=("${pids[@]:1}"); fi
  fi
done
wait
missing=0
for ((i=0;i<N;i++)); do
  s=$((i*CS)); e=$((s+CS-1)); [ $e -ge $TOTAL ] && e=$((TOTAL-1))
  want=$((e-s+1)); f="$DIR/part_$(printf %05d $i)"
  have=0; [ -f "$f" ] && have=$(stat -c %s "$f")
  [ "$have" -ne "$want" ] && missing=$((missing+1))
done
echo "chunks_total=$N incomplete=$missing"

#!/usr/bin/env bash
# fleet-tick.sh - Token-free 10-minute fleet check for ringmaster.
#
# Replaces the AGY cron loop. Runs under a systemd user timer; uses no LLM.
#   1. Host health: RAM/swap and ooda-oom-guard.timer state.
#   2. Git safety: snapshot uncommitted work to Forgejo (autosnap.sh) and list
#      repos with commits that are not on their Forgejo remote.
#   3. Panes: auto-resume panes stopped by a reset rate limit; flag idle panes.
# Writes one status line per tick to $LOG and the latest full report to $OUT.
# Only writes $ALERT when a human or agent must act.
set -u
STATE=/Projects/openOODA/.fleet-tick
mkdir -p "$STATE"
LOG=$STATE/ticks.log; OUT=$STATE/latest.txt; ALERT=$STATE/ALERT.txt
PANES="w3:p1 w4:p2 w5:p1 w6:p1 w7:p1 w8:p1 w9:p1 wA:p1"
now=$(date -Is)
alerts=()
{
echo "== fleet-tick $now"

# 1. Host health
read -r _ mt mu _ < <(free -g | awk '/^Mem:/{print $1,$2,$3,$7}')
avail=$(free -g | awk '/^Mem:/{print $7}')
swap=$(free -m | awk '/^Swap:/{print $3}')
oom=$(systemctl --user is-active ooda-oom-guard.timer 2>/dev/null)
echo "host: mem_used=${mu}G avail=${avail}G swap_used=${swap}M oom_guard=$oom"
[ "$oom" = active ] || alerts+=("ooda-oom-guard.timer is $oom")
[ "${avail:-0}" -lt 6 ] && alerts+=("low memory: ${avail}G available")

# 2. Git safety
echo "-- autosnap"
/Projects/openOODA/.autosnap.sh 2>&1 | grep -v '^same' || true
echo "-- commits on no remote branch"
unpushed=0
for g in $(find /Projects -maxdepth 3 -name .git -type d 2>/dev/null); do
  r=$(dirname "$g")
  up=$(git -C "$r" rev-list --count HEAD --not --remotes 2>/dev/null) || continue
  if [ "$up" != 0 ]; then echo "UNPUSHED $up $r"; unpushed=$((unpushed+1)); fi
done
[ "$unpushed" -gt 0 ] && alerts+=("$unpushed repo(s) have commits on no remote branch")

# 3. Panes
echo "-- panes"
idle=0
for p in $PANES; do
  txt=$(herdr pane read "$p" --source visible 2>/dev/null) || { echo "$p: unreadable"; continue; }
  last=$(echo "$txt" | grep -vE '^\s*$|───' | tail -4)
  if echo "$last" | grep -q 'Reached free model rate limit'; then
    reset=$(echo "$last" | grep -oE 'at [0-9]{2}:[0-9]{2} UTC' | grep -oE '[0-9]{2}:[0-9]{2}')
    if [ -n "$reset" ] && [ "$(date -u +%H:%M)" \> "$reset" ]; then
      herdr pane send-text "$p" "continue your current task; follow the git safety rule"
      sleep 0.3; herdr pane send-keys "$p" Enter
      echo "$p: rate limit reset ($reset UTC) -> resumed"
    else
      echo "$p: rate limited until ${reset:-?} UTC"
    fi
  elif echo "$txt" | grep -qE 'Thinking|Running tools|Typing'; then
    echo "$p: working"
  elif echo "$last" | grep -qE '\[y/n\]|\(y/N\)|Press Enter|Continue\?'; then
    echo "$p: WAITING FOR INPUT"; alerts+=("$p is waiting for input")
  else
    echo "$p: idle"; idle=$((idle+1))
  fi
done
[ "$idle" -gt 0 ] && alerts+=("$idle pane(s) idle - ready for new work")
} > "$OUT" 2>&1

if [ ${#alerts[@]} -gt 0 ]; then
  { echo "$now"; printf -- '- %s\n' "${alerts[@]}"; } > "$ALERT"
  echo "$now ALERT ${alerts[*]}" >> "$LOG"
else
  rm -f "$ALERT"
  echo "$now ok" >> "$LOG"
fi
tail -n 2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"

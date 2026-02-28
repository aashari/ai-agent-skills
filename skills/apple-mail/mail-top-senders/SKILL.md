---
name: mail-top-senders
description: Show who sends the most email, communication frequency analysis, and relationship mapping. Use when user asks who emails them most, top contacts, communication patterns, or wants to understand their email social graph. Arguments: optional time range (default: last 90 days), account filter, or "humans only" to exclude automated senders.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
---

# Mail Top Senders — Communication Frequency Analysis

Analysis period: **$ARGUMENTS** (default: last 90 days)

## Step 1: All senders ranked by volume
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"
SINCE=$(($(date +%s) - 7776000))  # 90 days

sqlite3 "$DB" "
SELECT a.address, a.comment as name,
       COUNT(*) as total,
       SUM(CASE WHEN m.read=0 THEN 1 ELSE 0 END) as unread,
       MIN(datetime(m.date_received,'unixepoch','localtime')) as first,
       MAX(datetime(m.date_received,'unixepoch','localtime')) as latest
FROM messages m
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND mb.url NOT LIKE '%Sent%'
GROUP BY a.address
ORDER BY total DESC
LIMIT 50;" 2>/dev/null
```

## Step 2: Separate humans from automated senders
Automated signals: address contains `noreply`, `no-reply`, `notifications@`, `alerts@`, `mailer@`, `bounce`, `system@`, `info@`, `support@`, `newsletter`, `donotreply`, `postmaster`; or name is empty; or sends at very regular intervals

```bash
# Human senders only
sqlite3 "$DB" "
SELECT a.address, a.comment as name, COUNT(*) as cnt
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Sent%'
  AND a.address NOT LIKE '%noreply%'
  AND a.address NOT LIKE '%no-reply%'
  AND a.address NOT LIKE '%notifications%'
  AND a.address NOT LIKE '%newsletter%'
  AND a.address NOT LIKE '%alerts@%'
  AND a.address NOT LIKE '%donotreply%'
  AND a.address NOT LIKE '%mailer%'
GROUP BY a.address ORDER BY cnt DESC LIMIT 20;" 2>/dev/null
```

## Step 3: Domain-level analysis
```bash
sqlite3 "$DB" "
SELECT substr(a.address, instr(a.address,'@')+1) as domain,
       COUNT(*) as cnt
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE}
  AND m.deleted = 0
  AND mb.url NOT LIKE '%Spam%'
GROUP BY domain ORDER BY cnt DESC LIMIT 20;" 2>/dev/null
```

## Step 4: Thread participation (two-way communication)
Find senders you also replied to — true relationships vs. one-way communication:
```bash
sqlite3 "$DB" "
SELECT a.address, COUNT(*) as received
FROM messages m
JOIN addresses a ON m.sender = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.date_received >= ${SINCE} AND m.deleted=0
  AND mb.url NOT LIKE '%Sent%'
GROUP BY a.address
ORDER BY received DESC LIMIT 30;" 2>/dev/null
```

## Output Format
**Top Email Relationships — [PERIOD]**

**Most Frequent Human Contacts:**
| Rank | Name | Address | Emails Received | Unread |
|---|---|---|---|---|

**Top Automated Senders (noise):**
| Service | Count | Type |
|---|---|---|

**Top Domains:**
| Domain | Count |
|---|---|

Insight: note anyone with high unread rate (you receive a lot but don't read → de-prioritize subscription?).
Note anyone with very recent last email who you haven't read → potential missed message.

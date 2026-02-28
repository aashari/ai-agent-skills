#!/usr/bin/env python3
"""
Shared Apple Mail emlx parser utility.
Usage: python3 parser.py <rowid> [rowid2 ...]
Prints JSON: [{rowid, subject, sender, date, body, attachments}]
"""
import sys, os, email, re, json, subprocess

DB = os.path.expanduser("~/Library/Mail/V10/MailData/Envelope Index")

def find_emlx(rowid):
    try:
        result = subprocess.check_output(
            f'find ~/Library/Mail/V10/ -name "{rowid}.emlx" 2>/dev/null | head -1',
            shell=True, text=True
        ).strip()
        return result if result else None
    except:
        return None

def clean_html(text):
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&#\d+;', '', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def parse_emlx(path):
    try:
        with open(path, 'rb') as fh:
            fh.readline()  # skip byte count (emlx-specific first line)
            content = fh.read()
        msg = email.message_from_bytes(content)
        body = ""
        attachments = []
        for part in msg.walk():
            ct = part.get_content_type()
            disp = str(part.get('Content-Disposition', ''))
            fname = part.get_filename()
            if fname:
                attachments.append(fname)
                continue
            if ct in ('text/plain', 'text/html') and 'attachment' not in disp:
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        b = payload.decode('utf-8', errors='replace')
                    except:
                        b = payload.decode('latin-1', errors='replace')
                    if ct == 'text/html':
                        b = clean_html(b)
                    if len(b) > len(body):
                        body = b
        return body.strip(), attachments
    except Exception as e:
        return f"[parse error: {e}]", []

if __name__ == '__main__':
    results = []
    for rowid in sys.argv[1:]:
        path = find_emlx(rowid)
        if path:
            body, atts = parse_emlx(path)
            results.append({"rowid": rowid, "path": path, "body": body[:6000], "attachments": atts})
        else:
            results.append({"rowid": rowid, "path": None, "body": "[not cached locally]", "attachments": []})
    print(json.dumps(results, ensure_ascii=False))

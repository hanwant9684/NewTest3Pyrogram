# Pyrogram Migration Plan

## Overview
Migrating from Telethon to Pyrogram for better concurrent download speeds.
Target: Maintain 10-15MB/s for 10 concurrent users.

## IMPORTANT RULE
**Wait for user approval before starting each batch.**
Do NOT automatically proceed to the next batch.
User must explicitly say "start batch X" or similar.

---

## Batch 1: Setup & Dependencies
**Status:** [x] COMPLETED

**Tasks:**
- [x] Install Pyrogram, TgCrypto via pip
- [x] Create `pyrogram_helpers.py` with InlineKeyboard, Button utilities
- [x] Verify imports work

**Files to create:**
- `pyrogram_helpers.py` (new)

**Verification:**
```bash
python -c "from pyrogram_helpers import InlineKeyboardButton, InlineKeyboardMarkup; print('OK')"
```

---

## Batch 2: Fast Transfer System
**Status:** [ ] Pending

**Tasks:**
- [ ] Create `pyrogram_fast_transfer.py` with parallel download
- [ ] Implement dynamic connection scaling based on active users
- [ ] Use `max_concurrent_transmissions` parameter

**Files to create:**
- `pyrogram_fast_transfer.py` (new)

**Verification:**
```bash
python -c "from pyrogram_fast_transfer import download_media_fast, upload_media_fast; print('OK')"
```

---

## Batch 3: Helper Files
**Status:** [ ] Pending

**Tasks:**
- [ ] Rewrite `helpers/transfer.py` for Pyrogram
- [ ] Rewrite `helpers/msg.py` for Pyrogram
- [ ] Rewrite `helpers/utils.py` for Pyrogram

**Files to modify:**
- `helpers/transfer.py`
- `helpers/msg.py`
- `helpers/utils.py`

**Verification:**
```bash
python -c "from helpers.transfer import download_media_fast; from helpers.msg import getChatMsgID; print('OK')"
```

---

## Batch 4: Session Manager
**Status:** [ ] Pending

**Tasks:**
- [ ] Rewrite `helpers/session_manager.py` for Pyrogram sessions
- [ ] Update session string format (Telethon -> Pyrogram)

**Files to modify:**
- `helpers/session_manager.py`

**Verification:**
```bash
python -c "from helpers.session_manager import session_manager; print('OK')"
```

---

## Batch 5: Access Control & Legal
**Status:** [ ] Pending

**Tasks:**
- [ ] Rewrite `access_control.py` decorators for Pyrogram
- [ ] Rewrite `legal_acceptance.py` callbacks for Pyrogram

**Files to modify:**
- `access_control.py`
- `legal_acceptance.py`

**Verification:**
```bash
python -c "from access_control import admin_only, paid_or_admin_only; print('OK')"
```

---

## Batch 6: Admin & Authentication
**Status:** [ ] Pending

**Tasks:**
- [ ] Rewrite `admin_commands.py` for Pyrogram events
- [ ] Rewrite `phone_auth.py` for Pyrogram client

**Files to modify:**
- `admin_commands.py`
- `phone_auth.py`

**Verification:**
```bash
python -c "from admin_commands import add_admin_command; from phone_auth import PhoneAuthHandler; print('OK')"
```

---

## Batch 7: Main Bot Part 1 (Lines 1-500)
**Status:** [ ] Pending

**Tasks:**
- [ ] Change TelegramClient -> Client (Pyrogram)
- [ ] Update event decorators (@bot.on -> @app.on_message)
- [ ] Rewrite client initialization
- [ ] Update basic command handlers

**Files to modify:**
- `main.py` (lines 1-500)

**Verification:**
- Bot should start without errors
- /start and /help commands should work

---

## Batch 8: Main Bot Part 2 (Lines 500-1000)
**Status:** [ ] Pending

**Tasks:**
- [ ] Rewrite download handlers for Pyrogram
- [ ] Update media processing logic
- [ ] Fix progress callbacks

**Files to modify:**
- `main.py` (lines 500-1000)

**Verification:**
- Download a single file successfully
- Progress updates should display

---

## Batch 9: Main Bot Part 3 (Lines 1000-1774)
**Status:** [ ] Pending

**Tasks:**
- [ ] Rewrite remaining handlers
- [ ] Update callback query handlers
- [ ] Fix any remaining Telethon references

**Files to modify:**
- `main.py` (lines 1000-1774)

**Verification:**
- All bot features should work
- No Telethon imports remaining in main.py

---

## Batch 10: Cleanup & Final Testing
**Status:** [ ] Pending

**Tasks:**
- [ ] Delete old Telethon files: `FastTelethon.py`, `telethon_helpers.py`
- [ ] Update `requirements.txt` (remove Telethon, add Pyrogram)
- [ ] Run full integration test
- [ ] Test with 3-5 concurrent downloads

**Files to delete:**
- `FastTelethon.py`
- `telethon_helpers.py`

**Files to update:**
- `requirements.txt`

**Final Verification:**
- 10 concurrent users downloading
- Each user gets 10-15MB/s speed
- No memory leaks

---

## File Dependency Order

Build files in this order to avoid import errors:

```
1. pyrogram_helpers.py (new, no dependencies)
2. pyrogram_fast_transfer.py (uses pyrogram_helpers)
3. helpers/transfer.py (uses fast_transfer)
4. helpers/msg.py (uses pyrogram)
5. helpers/utils.py (uses pyrogram)
6. helpers/session_manager.py (uses transfer)
7. access_control.py (uses helpers)
8. legal_acceptance.py (uses helpers)
9. admin_commands.py (uses access_control)
10. phone_auth.py (uses session_manager)
11. main.py (uses everything)
```

---

## Key Pyrogram vs Telethon Differences

| Telethon | Pyrogram |
|----------|----------|
| `TelegramClient` | `Client` |
| `@bot.on(events.NewMessage)` | `@app.on_message(filters.command("cmd"))` |
| `event.respond()` | `message.reply()` |
| `event.sender_id` | `message.from_user.id` |
| `event.chat_id` | `message.chat.id` |
| `StringSession` | `Client(..., session_string=...)` |
| `Button.inline()` | `InlineKeyboardButton()` |
| `message.document` | `message.document` (same) |
| `message.video` | `message.video` (same) |

---

## Requirements.txt Changes

**Remove:**
```
Telethon
```

**Add:**
```
Pyrogram
TgCrypto
```

---

## Notes
- Keep old Telethon files until Batch 10 (for reference)
- Test each batch before moving to next
- Check for memory leaks after each download test
- User sessions will need to be re-authenticated (different session format)

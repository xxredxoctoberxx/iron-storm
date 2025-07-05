# Iron-Storm

**Iron-Storm** is a robust, Python-based system of automated Instagram accounts designed for strategic social media defense.

It operates multiple Instagram accounts simultaneously, using:
- Smart engagement patterns
- Automated content interaction
- Anti-detection techniques
- Proxy rotation and human-like behavior simulation

Originally backed by an Israeli proxy provider, Iron-Storm was actively deployed during the early days following the October 7th attacks to amplify pro-Israel messaging and distribute critical information on Instagram.

---

## Getting Started

### Prerequisites
- A `.csv` file of account credentials named `accounts.csv` in the format: `account,password,email,password`
- A `proxy.txt` file with proxy credentials in the format: `user,password,host,port`
- A folder called `accounts_pfps/` populated with varied profile pictures

### Setup Steps

1. Prepare sessions  
   Run:
   ```bash
   python set_session.py accounts.csv
   ```
   This creates `accounts_clean.csv` with successfully logged-in sessions.

2. Assign avatars and user tags  
   Run:
   ```bash
   python avataring.py
   ```
   This outputs `avatared_batch.csv` with updated profile data.

3. Finalize sessions with new avatars  
   Run:
   ```bash
   python set_session.py avatared_batch.csv
   ```
   Produces `avatared_batch_clean.csv` with fully-ready bot sessions.

4. Run the bot army  
   Launch:
   ```bash
   python iron_storm.py
   ```

---

## Folder Structure
```
iron-storm/
├── accounts_pfps/          # Profile images for bots
├── set_session.py          # Initializes sessions for accounts
├── avataring.py            # Generates avatars and human-style usernames
├── iron_storm.py           # Main execution script
├── proxy.txt               # Proxy credential file
├── *.csv                   # Input/output data files
```

---

## Disclaimer
This tool was created for defensive and informational purposes during an ongoing crisis. Please use responsibly and in accordance with local laws and platform policies.

---

## License
Proprietary — for internal or research use only.
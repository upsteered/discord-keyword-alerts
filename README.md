
# Discord Keyword Alert System

A simple Discord keyword monitoring system that watches messages in a server and alerts you when it sees words or phrases you choose.

This project is a small companion utility for **Upsteered**:
https://upsteered.com

---

## What this system does

This system can:

- watch Discord messages in a server
- check them for keywords you choose
- print alerts in the console
- optionally send alerts to a Discord channel

---

## What you need before you start

You need:

- a Discord account
- a Discord server where you are allowed to add a bot
- a computer
- Python installed
- a GitHub account if you want to publish the repo

---

## Files in this project

- `bot.py` — the main system code
- `keywords.txt` — the words or phrases the system should look for
- `requirements.txt` — the Python packages the system needs
- `.gitignore` — tells Git not to upload secret or unwanted files
- `.env.example` — shows what secret settings the system needs
- `README.md` — this guide
- `LICENSE` — the license for the project

---

## Step 1: Install Python

Python is the programming language this system uses.

### How to install it
1. Go to https://python.org
2. Click **Downloads**
3. Download the latest version for your computer
4. Install it
5. On Windows, make sure **Add Python to PATH** is checked

### How to check if Python is installed
Open Terminal or Command Prompt and run:

```bash
python --version
```

or:

```bash
python3 --version
```

If Python is installed, you will see a version number.

---

## Step 2: Create a Discord application

A Discord application is what allows your system to connect to Discord and read messages in servers.

### Do this:

1. Go to the Discord Developer Portal:
   [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application**
3. Give it a name
4. Open the app, then go to **Bot**
5. Click **Add Bot**
6. Copy the token

   * keep this secret
   * do not post it on GitHub
7. In the settings, turn on **Message Content Intent**

---

## Step 3: Invite it to your server

1. In the Developer Portal, go to **OAuth2**
2. Open **URL Generator**
3. Under **Scopes**, check:

   * `bot`
4. Under **Permissions**, check:

   * `Read Messages/View Channels`
   * `Send Messages`
5. Copy the generated invite link
6. Open the link and add it to your server

---

## Step 4: Create the project folder

Put all the files in one folder.

Example:

```txt
discord-keyword-alert-bot/
```

Inside that folder, put:

* `bot.py`
* `keywords.txt`
* `requirements.txt`
* `.gitignore`
* `.env.example`
* `README.md`
* `LICENSE`

---

## Step 5: Install the Python packages

Open Terminal or Command Prompt in the project folder.

Run:

```bash
pip install -r requirements.txt
```

This installs the packages the system needs.

---

## Step 6: Create your `.env` file

The system needs your secret token to log in.

Create a file named `.env` in the project folder.

It should look like this:

```env
TOKEN=your_discord_token_here
```

Important:

* `.env` is for your computer only
* do **not** upload `.env` to GitHub
* keep `.env.example` in the repo instead

---

## Step 7: Edit the keywords

Open `keywords.txt`.

Put one keyword or phrase on each line.

Example:

```txt
pricing
quote
budget
demo
call
lead
proposal
interest
```

The system will alert when it finds one of these in a message.

---

## Step 8: Run it

In the project folder, run:

```bash
python bot.py
```

or:

```bash
python3 bot.py
```

If everything is set up correctly, it will log in and start watching messages.

---

## Step 9: Test it

Send a message in your Discord server that contains one of your keywords.

Example:

```txt
Can I get a demo and pricing?
```

If it sees a keyword, it will print an alert.

---

## Optional: Send alerts to a Discord channel

You can also make it send alerts to a specific channel.

Add this to your `.env` file:

```env
TOKEN=your_discord_token_here
ALERT_CHANNEL_ID=123456789012345678
```

To get the channel ID:

1. Open Discord
2. Turn on Developer Mode in Discord settings
3. Right-click the channel
4. Click **Copy Channel ID**

---

## How this connects to Upsteered

This system is meant to be a simple utility that supports the larger Upsteered ecosystem.

GitHub repo:

* helps people discover the tool
* gives trust through open source
* sends visitors to your main site

Upsteered website:

* explains what Upsteered does and how it works
* is the main entry point to the platform and app

Link to Upsteered here:
[https://upsteered.com](https://upsteered.com)

---

## Do not upload secrets

Never commit these to GitHub:

* your Discord token
* your `.env` file

The files that are safe to upload are:

* `bot.py`
* `keywords.txt`
* `requirements.txt`
* `.env.example`
* `.gitignore`
* `README.md`
* `LICENSE`

---

## License

This project uses the MIT License.

# Telegram bot for sending messages from various users to one channel

The main purpose of this bot is to organize a channel where some users could read reports from their reportee like a news feed but reporters can't see reports of each other.

## Service setup

1. Install requirements: `pip install -r .\requirements.txt`
2. Make file `settings.ini` according to the `settings.example.ini`
3. Specify `BOT_API_KEY` and `TARGET_CHANNEL_ID` in `settings.ini`

## Run service

`python .\run_bot.py`

## Operation

### Make admin

For first launch users can't send messages to the channel.
First of all you need to promote one user to admin level:

1. Open chat with you bot and write `/start`
2. Press `Authorization request to send reports` button
3. Edit `users.json` in project's root dirrectory and manually change level of chosen user from `"level": "pending"` to `"level": "admin"` and then save the file
4. In telegram application press `help` button to update menu
5. Now you are admin

### Make reporter

For now new users can request for authorization to write to channel and admin user can get list or requests and promote promote them to `reporter` status.

- `/display_requests` button:

```text
Requested authorization to send reports:
1. @some_user ID 35XXXX761 - Some User;
```

- `/make_reporter 35XXXX761`

```text
User status changed
```

Now user has `reporter` level and can write messages to the channel.

### Write message to channel

Users with `admin` and `reporter` level can write messages to the channel

1. Press `Send message to the channel`
2. Write the message and add necessary files or images and press send
3. Confirm sending with `Confirm` button

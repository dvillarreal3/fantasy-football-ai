# Troubleshooting

## Common Issues

### ESPN authentication fails
- Verify that `ESPN_S2` and `ESPN_SWID` were copied from an active ESPN browser session.
- Confirm that `ESPN_LEAGUE_ID` is set and belongs to the same account session.
- If cookies recently rotated, update the values in `.env`.

### AI recommendations fall back to placeholder text
- Confirm `AI_PROVIDER` is set to `claude` or `openai`.
- Add the matching API key to `.env`.
- Install dependencies from `requirements.txt` so the provider SDK is available.

### Discord messages are not sent
- Verify `DISCORD_BOT_TOKEN` and `DISCORD_CHANNEL_ID`.
- Make sure the bot is invited to the server and has permission to post in the channel.
- Test a manual run without `--schedule` first to confirm formatting and credentials.

### Scheduled jobs do not start
- Ensure `APScheduler` is installed in the active virtual environment.
- Check that the `--time` argument uses `HH:MM` in 24-hour format.
- Run the process in an environment that stays alive long enough for the job to trigger.

## FAQ

### Does this support 2-QB leagues?
Yes. The initial lineup optimizer reserves two quarterback slots before filling the rest of the lineup.

### Can I use this without Discord?
Yes. Manual CLI runs print reports to stdout, and Discord delivery is optional.

### Does the assistant require live APIs for development?
No. The project includes deterministic fallbacks so imports and unit tests work even when ESPN, AI, or Discord credentials are unavailable.

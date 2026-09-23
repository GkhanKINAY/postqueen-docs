# App screenshots

The Guide pages carry one screenshot each, in `images/app/`. They were taken on 2026-09-23 from app v3.6.81.

## How they were made

- **The app ran locally from a git worktree of `postqueen-app` main.** It used its own ports, and a scratch Postgres database created only for the shots and dropped afterwards. Nobody's real database or account was touched.
- **The workspace was a fictional café, "Harbor Street Café", with a demo user.** Its eight channels were fake Integration rows with placeholder tokens, so nothing could reach a network. The analytics numbers were written to the cache by hand, and the images were generated posters.
- **Capture settings:** light theme, a 1440×900 viewport at 2× scale, and the UTC time zone.
- **Output:** each shot was saved as WebP at quality 90, 1600 px wide, or cropped to its dialog. Each file is under 400 KB (most are under 100 KB).
- **The API key is blurred** in `connections.webp`.

## Rules for a new or retaken shot

- Never photograph a real account, and never use production or the owner's development database.
- A page gets at most one shot. Put it after the page's opening lines, in a `<Frame>` with the `pq-shot` class and alt text that says what the screen shows:

  ```mdx
  <Frame>
    <img className="pq-shot" src="/images/app/calendar-week.webp" alt="The calendar in Week view, with the Posts panel listing scheduled posts on the left" />
  </Frame>
  ```

- Retake a shot when its screen changes. A label in the picture that no longer matches the page text is worse than having no picture.


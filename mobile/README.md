# AthliQ Mobile (React Native / Expo)

Talks to the same FastAPI backend as `../frontend`. Uses Expo Router for
navigation and AsyncStorage for the auth token (there's no browser
localStorage on native).

## Setup

```bash
cd mobile
npm install
cp .env.example .env
# edit EXPO_PUBLIC_API_BASE_URL — "localhost" won't reach your machine from
# a physical device or most emulators; use your machine's LAN IP instead,
# e.g. http://192.168.1.20:8000
npx expo start
```

Then press `i` (iOS simulator), `a` (Android emulator), or scan the QR
code in the Expo Go app on a physical device.

## Structure

```
app/
  (auth)/login.tsx, register.tsx
  student/dashboard.tsx, today.tsx, calendar.tsx, progress.tsx
  coach/dashboard.tsx, students.tsx, upload-csv.tsx
components/ui/     Button, Input, Card (React Native primitives)
lib/api/           same endpoints as frontend/lib/api, using AsyncStorage
lib/types/         mirrors the backend Pydantic schemas
```

## Notes
- `student/` and `coach/` are real route segments (not `(group)` folders) —
  Expo Router strips groups from the URL the same way Next.js does, so two
  groups both containing e.g. `dashboard.tsx` would collide. See the note
  in `../docs/APPROACH.md`.
- CSV upload uses `expo-document-picker`; wire up a native file input for
  each platform target as needed.
- This wasn't run against Expo Go/an emulator in this environment — no
  iOS/Android toolchain available here — but the code has no syntax errors
  and follows the same patterns already build-verified in `../frontend`.

# Frontend

The frontend is a small React/Vite dashboard for querying logs.

## Responsibility

- renders a search form for `service` and `level`
- calls the query-service API
- renders matching log cards or an empty state

## Files

- [src/App.jsx](src/App.jsx): UI and fetch behavior
- [src/main.jsx](src/main.jsx): React bootstrap
- [src/styles.css](src/styles.css): visual styling
- [package.json](package.json): frontend dependencies and scripts
- [vite.config.js](vite.config.js): Vite config
- [Dockerfile](Dockerfile): container build

## API Resolution Behavior

The frontend chooses its API base URL this way:

1. if the page is opened on `localhost` or `127.0.0.1`, it uses `http://localhost:8000`
2. otherwise, if `VITE_QUERY_API_URL` is defined, it uses that
3. otherwise, it falls back to `window.location.origin + /api`

This allows:

- local Compose usage
- Kubernetes port-forward usage
- ingress-based routing

## Expected UX

- initial filters default to `service=auth` and `level=error`
- status text shows loading, success count, or fetch errors
- results render indexed documents with service, level, message, and timestamp

import { StateBlock } from "./StateBlock";

export function ApiUnavailable({ onRetry }: { onRetry?: () => void }) {
  return (
    <StateBlock
      title="API unavailable"
      message="Start the Docker Compose stack, then refresh this page. Expected API URL: http://localhost:8000."
      actions={
        onRetry ? (
          <button className="rounded bg-ink px-3 py-2 text-sm font-medium text-white hover:bg-slate-700" onClick={onRetry} type="button">
            Try again
          </button>
        ) : null
      }
    />
  );
}

import type { ReactNode } from "react";

export function StateBlock({ title, message, actions }: { title: string; message: string; actions?: ReactNode }) {
  return (
    <div className="rounded border border-dashed border-line bg-white p-6 text-center">
      <p className="font-semibold text-ink">{title}</p>
      <p className="mt-1 text-sm text-slate-500">{message}</p>
      {actions ? <div className="mt-4 flex flex-wrap justify-center gap-2">{actions}</div> : null}
    </div>
  );
}

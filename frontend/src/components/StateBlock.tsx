export function StateBlock({ title, message }: { title: string; message: string }) {
  return (
    <div className="rounded border border-dashed border-line bg-white p-6 text-center">
      <p className="font-semibold text-ink">{title}</p>
      <p className="mt-1 text-sm text-slate-500">{message}</p>
    </div>
  );
}

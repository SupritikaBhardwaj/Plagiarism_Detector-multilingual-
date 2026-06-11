export function AuthPage() {
  return (
    <div className="mx-auto max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-panel dark:border-slate-800 dark:bg-slate-900">
      <h2 className="text-xl font-semibold">User Authentication</h2>
      <input className="mt-5 w-full rounded-lg border border-slate-300 bg-transparent px-3 py-2 dark:border-slate-700" placeholder="Email" />
      <input className="mt-3 w-full rounded-lg border border-slate-300 bg-transparent px-3 py-2 dark:border-slate-700" placeholder="Password" type="password" />
      <button className="mt-4 w-full rounded-lg bg-slate-950 px-4 py-2 font-semibold text-white dark:bg-white dark:text-slate-950">Sign in</button>
    </div>
  );
}


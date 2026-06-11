type GraphNode = { id: number; label: string; type?: string; detail?: string | null };
type GraphEdge = { source: number; target: number; type: string };

type Graph = {
  nodes?: GraphNode[];
  edges?: GraphEdge[];
};

const explanations: Record<string, string> = {
  Program: "Entry point of the parsed program structure.",
  Include: "Imports a library or header before the program runs.",
  Function: "Defines a reusable block of logic, such as main or a helper function.",
  Declaration: "Creates a variable or reserves storage for data.",
  Assignment: "Updates a variable with a new value.",
  Call: "Calls another function such as printf, scanf, cout, or a helper.",
  Loop: "Repeats a block of statements.",
  Branch: "Chooses between paths using if, else, or switch.",
  Return: "Exits a function and optionally sends back a value.",
  Statement: "A generic statement that the fallback parser could not classify more specifically."
};

export function GraphViewer({ graph }: { graph?: Graph }) {
  const nodes = graph?.nodes ?? [];
  const edges = graph?.edges ?? [];
  const visibleNodes = nodes.slice(0, 14);
  const visibleIds = new Set(visibleNodes.map((node) => node.id));
  const visibleEdges = edges.filter((edge) => visibleIds.has(edge.source) && visibleIds.has(edge.target)).slice(0, 18);
  const nodeCounts = nodes.reduce<Record<string, number>>((counts, node) => {
    counts[node.label] = (counts[node.label] ?? 0) + 1;
    return counts;
  }, {});

  function nextNodes(id: number) {
    return edges.filter((edge) => edge.source === id).map((edge) => edge.target);
  }

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel dark:border-slate-800 dark:bg-slate-900">
      <div className="mb-4 flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="font-semibold">CFG/PDG Explanation</h2>
          <p className="text-sm text-slate-500">
            A simplified reading of the control-flow graph. Read it from top to bottom as the program structure discovered by the parser.
          </p>
        </div>
        <span className="text-sm text-slate-500">{nodes.length} nodes / {edges.length} edges</span>
      </div>

      {nodes.length === 0 ? (
        <div className="rounded-lg border border-dashed border-slate-300 p-6 text-center text-sm text-slate-500 dark:border-slate-700">
          Run an analysis first to generate a graph explanation.
        </div>
      ) : (
        <div className="space-y-4">
          <div className="grid gap-3 md:grid-cols-3">
            {Object.entries(nodeCounts).map(([label, count]) => (
              <div key={label} className="rounded-lg bg-slate-100 px-3 py-2 text-sm dark:bg-slate-800">
                <span className="font-medium">{label}</span>
                <span className="float-right text-slate-500">{count}</span>
              </div>
            ))}
          </div>

          <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:border-slate-800 dark:bg-slate-950">
            <div className="mb-3 text-sm font-semibold">Readable Program Flow</div>
            <div className="space-y-2">
              {visibleNodes.map((node, index) => {
                const next = nextNodes(node.id);
                const isDecision = node.label === "Loop" || node.label === "Branch";
                return (
                  <div key={node.id} className="rounded-lg border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-900">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-3">
                        <span className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold ${isDecision ? "bg-orange-100 text-orange-700 dark:bg-orange-950 dark:text-orange-200" : "bg-teal-100 text-teal-700 dark:bg-teal-950 dark:text-teal-200"}`}>
                          {index + 1}
                        </span>
                        <div>
                          <div className="font-semibold">{node.label}</div>
                          <div className="text-xs text-slate-500">{node.detail ?? `Node ${node.id}`}</div>
                        </div>
                      </div>
                      <div className="text-xs text-slate-500">
                        {next.length > 0 ? `goes to node ${next.join(", ")}` : "last visible step"}
                      </div>
                    </div>
                    <div className="mt-2 text-sm text-slate-600 dark:text-slate-300">
                      {explanations[node.label] ?? explanations.Statement}
                    </div>
                  </div>
                );
              })}
            </div>
            {nodes.length > visibleNodes.length && (
              <div className="mt-3 text-xs text-slate-500">
                Showing first {visibleNodes.length} nodes. Large programs are summarized to keep this readable.
              </div>
            )}
          </div>

          <details className="rounded-lg bg-slate-100 p-3 text-sm dark:bg-slate-800">
            <summary className="cursor-pointer font-medium">Technical CFG edges</summary>
            <div className="mt-3 grid gap-2 md:grid-cols-2">
              {visibleEdges.map((edge) => (
                <div key={`${edge.source}-${edge.target}-${edge.type}`} className="rounded-md bg-white px-3 py-2 dark:bg-slate-900">
                  Node {edge.source} to Node {edge.target}
                  <span className="ml-2 text-slate-500">({edge.type})</span>
                </div>
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  );
}

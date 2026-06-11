import Editor from "@monaco-editor/react";

type Props = {
  left: string;
  right: string;
  onLeftChange: (value: string) => void;
  onRightChange: (value: string) => void;
};

export function CodeCompare({ left, right, onLeftChange, onRightChange }: Props) {
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-800">
        <Editor height="380px" defaultLanguage="python" theme="vs-dark" value={left} onChange={(value) => onLeftChange(value ?? "")} />
      </div>
      <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-800">
        <Editor height="380px" defaultLanguage="python" theme="vs-dark" value={right} onChange={(value) => onRightChange(value ?? "")} />
      </div>
    </div>
  );
}


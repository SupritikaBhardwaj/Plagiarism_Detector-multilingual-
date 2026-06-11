import { useEffect, useState } from "react";

export function useLiveProgress(active: boolean) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (!active) {
      setProgress(0);
      return;
    }
    const timer = window.setInterval(() => {
      setProgress((value) => Math.min(94, value + 7));
    }, 250);
    return () => window.clearInterval(timer);
  }, [active]);

  return progress;
}


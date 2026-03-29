import React from "react";

import type { TrainingRun } from "../types/domain";

type Props = {
  run?: TrainingRun;
  onResume: (payload: { checkpointPath?: string; extraEpisodes: number }) => void;
};

export function RunResumeDialog({ run, onResume }: Props) {
  const [checkpointPath, setCheckpointPath] = React.useState("");
  const [extraEpisodes, setExtraEpisodes] = React.useState(80);

  React.useEffect(() => {
    setCheckpointPath(run?.latest_checkpoint ?? "");
  }, [run?.latest_checkpoint]);

  return (
    <section className="panel">
      <h2>Run Resume</h2>
      {run ? (
        <>
          <p>Selected run: <strong>{run.run_id}</strong></p>
          <p>Status: {run.status}</p>
          <div className="form-grid">
            <label>
              Checkpoint Path
              <input value={checkpointPath} onChange={(e) => setCheckpointPath(e.target.value)} placeholder="optional; defaults to latest" />
            </label>
            <label>
              Extra Episodes
              <input type="number" value={extraEpisodes} min={1} onChange={(e) => setExtraEpisodes(Number(e.target.value))} />
            </label>
          </div>
          <button onClick={() => onResume({ checkpointPath: checkpointPath || undefined, extraEpisodes })}>Resume This Run</button>
        </>
      ) : (
        <p>Select a run from the run table to resume.</p>
      )}
    </section>
  );
}

import { execFile } from "child_process";

/** Run Claude Code in --print mode. */
export function runClaude(
  prompt: string,
  cwd: string,
  timeoutMs = 120_000
): Promise<string> {
  return new Promise((resolve) => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    const child = execFile(
      "claude",
      ["--print"],
      { cwd, signal: controller.signal, maxBuffer: 10 * 1024 * 1024 },
      (error, stdout, _stderr) => {
        clearTimeout(timer);
        if (error) {
          if (error.name === "AbortError" || (error as NodeJS.ErrnoException).code === "ABORT_ERR") {
            resolve("Response timed out. Try splitting into simpler requests.");
            return;
          }
          if ((error as NodeJS.ErrnoException).code === "ENOENT") {
            resolve("Claude Code is not installed. Check the `claude` command.");
            return;
          }
          resolve(`Error: ${error.message}`);
          return;
        }
        resolve((stdout || "").trim());
      }
    );

    if (child.stdin) {
      child.stdin.write(prompt);
      child.stdin.end();
    }
  });
}

import chalk from "chalk";

export const logger = {
  info(tag: string, message: string) {
    console.log(chalk.dim(`[${tag}]`), message);
  },
  success(message: string) {
    console.log(chalk.green("✓"), message);
  },
  warn(message: string) {
    console.log(chalk.yellow("⚠"), message);
  },
  error(message: string) {
    console.error(chalk.red("✗"), message);
  },
  dim(message: string) {
    console.log(chalk.dim(message));
  },
};

import type { Product } from "../util/config.js";

export interface MessageContext {
  reply(text: string): Promise<void>;
  typing(): Promise<void>;
  _agentLabel: string;
}

export type CommandHandler = (
  userInput: string,
  product: Product,
  ctx: MessageContext
) => Promise<void>;

export interface MessengerAdapter {
  readonly platform: string;
  readonly channelNames: string[];

  /** Start listening for commands. */
  startBot(onCommand: CommandHandler): Promise<void>;

  /** Connect for sending only (scheduler mode). */
  startNotifier(): Promise<void>;

  /** Send a message to a named channel. */
  sendToChannel(
    productConfig: Record<string, unknown>,
    channelName: string,
    text: string,
    title?: string
  ): Promise<boolean>;

  /** Ensure required channels exist. */
  setupChannels(productConfig: Record<string, unknown>): Promise<string[]>;
}

export const DEFAULT_CHANNELS = [
  "daily-brief",
  "experiments",
  "weekly-review",
  "signals",
  "owner-command",
  "errors",
];

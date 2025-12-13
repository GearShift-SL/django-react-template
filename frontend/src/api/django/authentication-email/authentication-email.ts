// @ts-nocheck
import type {
  CodeConfirmRequestRequest,
  CodeConfirmResponse,
  StartAuthRequestRequest,
  StartAuthResponse,
} from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * Use this endpoint to pass along the received one-time "special" login code.
 * @summary Confirm login code
 */
export const authConfirmCode = (
  client: "app" | "browser",
  codeConfirmRequestRequest: CodeConfirmRequestRequest,
  options?: SecondParameter<typeof customAxiosInstance<CodeConfirmResponse>>,
) => {
  return customAxiosInstance<CodeConfirmResponse>(
    {
      url: `/auth/${client}/code/confirm/`,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      data: codeConfirmRequestRequest,
    },
    options,
  );
};
/**
 * If the identifier belongs to an existing user, request a one-time login code. Otherwise, create the user (per your Allauth config) and then proceed.
 * @summary Request login code or sign up
 */
export const authStart = (
  client: "app" | "browser",
  startAuthRequestRequest: StartAuthRequestRequest,
  options?: SecondParameter<typeof customAxiosInstance<StartAuthResponse>>,
) => {
  return customAxiosInstance<StartAuthResponse>(
    {
      url: `/auth/${client}/start/`,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      data: startAuthRequestRequest,
    },
    options,
  );
};
export type AuthConfirmCodeResult = NonNullable<
  Awaited<ReturnType<typeof authConfirmCode>>
>;
export type AuthStartResult = NonNullable<
  Awaited<ReturnType<typeof authStart>>
>;

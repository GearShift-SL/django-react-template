// @ts-nocheck
import type { SessionStatusResponse } from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * Retrieve information about the authentication status for the current session.
 * @summary Get authentication status
 */
export const authSessionStatus = (
  client: "app" | "browser",
  options?: SecondParameter<typeof customAxiosInstance<SessionStatusResponse>>,
) => {
  return customAxiosInstance<SessionStatusResponse>(
    { url: `/auth/${client}/session/`, method: "GET" },
    options,
  );
};
/**
 * Logs out the user from the current session.
 * @summary Logout
 */
export const authLogout = (
  client: "app" | "browser",
  options?: SecondParameter<typeof customAxiosInstance<SessionStatusResponse>>,
) => {
  return customAxiosInstance<SessionStatusResponse>(
    { url: `/auth/${client}/session/`, method: "DELETE" },
    options,
  );
};
export type AuthSessionStatusResult = NonNullable<
  Awaited<ReturnType<typeof authSessionStatus>>
>;
export type AuthLogoutResult = NonNullable<
  Awaited<ReturnType<typeof authLogout>>
>;

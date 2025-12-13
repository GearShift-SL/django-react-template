// @ts-nocheck
import type {
  ProviderTokenRequestRequest,
  ProviderTokenResponse,
  ProvidersListResponse,
} from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * Authenticate using a third-party provider token (e.g., Google). `process=login` logs in (or signs up) the user. `process=connect` links the provider to the currently authenticated user. For mobile (`client=app`), send `X-Session-Token` header from the prior app session bootstrap.
 * @summary Provider token
 */
export const authProviderToken = (
  client: "app" | "browser",
  providerTokenRequestRequest: ProviderTokenRequestRequest,
  options?: SecondParameter<typeof customAxiosInstance<ProviderTokenResponse>>,
) => {
  return customAxiosInstance<ProviderTokenResponse>(
    {
      url: `/auth/${client}/provider/token/`,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      data: providerTokenRequestRequest,
    },
    options,
  );
};
/**
 * Returns enabled Allauth providers and their client IDs.
 * @summary List social providers
 */
export const authProvidersList = (
  options?: SecondParameter<typeof customAxiosInstance<ProvidersListResponse>>,
) => {
  return customAxiosInstance<ProvidersListResponse>(
    { url: `/auth/providers/`, method: "GET" },
    options,
  );
};
export type AuthProviderTokenResult = NonNullable<
  Awaited<ReturnType<typeof authProviderToken>>
>;
export type AuthProvidersListResult = NonNullable<
  Awaited<ReturnType<typeof authProvidersList>>
>;

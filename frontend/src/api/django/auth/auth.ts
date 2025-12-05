// @ts-nocheck
import type {
  CodeConfirmRequestRequest,
  CodeConfirmResponse,
  PatchedUserProfileRequest,
  PatchedUserRequest,
  ProviderTokenRequestRequest,
  ProviderTokenResponse,
  ProvidersListResponse,
  SessionStatusResponse,
  StartAuthRequestRequest,
  StartAuthResponse,
  User,
  UserMe,
  UserProfile,
  UserProfileRequest,
  UserRequest,
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
export const authUserMeRetrieve = (
  options?: SecondParameter<typeof customAxiosInstance<UserMe>>,
) => {
  return customAxiosInstance<UserMe>(
    { url: `/auth/user/me/`, method: "GET" },
    options,
  );
};
export const authUserMeUpdate = (
  userRequest: UserRequest,
  options?: SecondParameter<typeof customAxiosInstance<User>>,
) => {
  return customAxiosInstance<User>(
    {
      url: `/auth/user/me/`,
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      data: userRequest,
    },
    options,
  );
};
export const authUserMePartialUpdate = (
  patchedUserRequest: PatchedUserRequest,
  options?: SecondParameter<typeof customAxiosInstance<User>>,
) => {
  return customAxiosInstance<User>(
    {
      url: `/auth/user/me/`,
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      data: patchedUserRequest,
    },
    options,
  );
};
/**
 * Retrieve or update the current user's profile information including avatar. Use multipart/form-data to upload files.
 * @summary Get or update user profile
 */
export const userProfile = (
  options?: SecondParameter<typeof customAxiosInstance<UserProfile>>,
) => {
  return customAxiosInstance<UserProfile>(
    { url: `/auth/user/me/profile/`, method: "GET" },
    options,
  );
};
/**
 * Retrieve or update the current user's profile information including avatar. Use multipart/form-data to upload files.
 * @summary Get or update user profile
 */
export const userProfile3 = (
  userProfileRequest: UserProfileRequest,
  options?: SecondParameter<typeof customAxiosInstance<UserProfile>>,
) => {
  return customAxiosInstance<UserProfile>(
    {
      url: `/auth/user/me/profile/`,
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      data: userProfileRequest,
    },
    options,
  );
};
/**
 * Retrieve or update the current user's profile information including avatar. Use multipart/form-data to upload files.
 * @summary Get or update user profile
 */
export const userProfile2 = (
  patchedUserProfileRequest: PatchedUserProfileRequest,
  options?: SecondParameter<typeof customAxiosInstance<UserProfile>>,
) => {
  return customAxiosInstance<UserProfile>(
    {
      url: `/auth/user/me/profile/`,
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      data: patchedUserProfileRequest,
    },
    options,
  );
};
export type AuthConfirmCodeResult = NonNullable<
  Awaited<ReturnType<typeof authConfirmCode>>
>;
export type AuthProviderTokenResult = NonNullable<
  Awaited<ReturnType<typeof authProviderToken>>
>;
export type AuthSessionStatusResult = NonNullable<
  Awaited<ReturnType<typeof authSessionStatus>>
>;
export type AuthLogoutResult = NonNullable<
  Awaited<ReturnType<typeof authLogout>>
>;
export type AuthStartResult = NonNullable<
  Awaited<ReturnType<typeof authStart>>
>;
export type AuthProvidersListResult = NonNullable<
  Awaited<ReturnType<typeof authProvidersList>>
>;
export type AuthUserMeRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof authUserMeRetrieve>>
>;
export type AuthUserMeUpdateResult = NonNullable<
  Awaited<ReturnType<typeof authUserMeUpdate>>
>;
export type AuthUserMePartialUpdateResult = NonNullable<
  Awaited<ReturnType<typeof authUserMePartialUpdate>>
>;
export type UserProfileResult = NonNullable<
  Awaited<ReturnType<typeof userProfile>>
>;
export type UserProfile3Result = NonNullable<
  Awaited<ReturnType<typeof userProfile3>>
>;
export type UserProfile2Result = NonNullable<
  Awaited<ReturnType<typeof userProfile2>>
>;

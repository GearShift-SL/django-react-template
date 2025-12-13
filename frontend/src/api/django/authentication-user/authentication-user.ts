// @ts-nocheck
import type { PatchedUserRequest, User, UserMe } from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * ViewSet for managing the current user's profile.
 */
export const authUserMeRetrieve = (
  options?: SecondParameter<typeof customAxiosInstance<UserMe>>,
) => {
  return customAxiosInstance<UserMe>(
    { url: `/auth/user/me/`, method: "GET" },
    options,
  );
};
/**
 * ViewSet for managing the current user's profile.
 */
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
export type AuthUserMeRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof authUserMeRetrieve>>
>;
export type AuthUserMePartialUpdateResult = NonNullable<
  Awaited<ReturnType<typeof authUserMePartialUpdate>>
>;

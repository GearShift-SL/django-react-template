// @ts-nocheck
import type {
  PatchedUserProfileRequest,
  UserProfile,
} from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * ViewSet for managing the current user's profile avatar and other profile data.
 */
export const authProfileMeRetrieve = (
  options?: SecondParameter<typeof customAxiosInstance<UserProfile>>,
) => {
  return customAxiosInstance<UserProfile>(
    { url: `/auth/profile/me/`, method: "GET" },
    options,
  );
};
/**
 * ViewSet for managing the current user's profile avatar and other profile data.
 */
export const authProfileMePartialUpdate = (
  patchedUserProfileRequest: PatchedUserProfileRequest,
  options?: SecondParameter<typeof customAxiosInstance<UserProfile>>,
) => {
  const formData = new FormData();
  if (
    patchedUserProfileRequest.avatar !== undefined &&
    patchedUserProfileRequest.avatar !== null
  ) {
    formData.append(`avatar`, patchedUserProfileRequest.avatar);
  }

  return customAxiosInstance<UserProfile>(
    {
      url: `/auth/profile/me/`,
      method: "PATCH",
      headers: { "Content-Type": "multipart/form-data" },
      data: formData,
    },
    options,
  );
};
export type AuthProfileMeRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof authProfileMeRetrieve>>
>;
export type AuthProfileMePartialUpdateResult = NonNullable<
  Awaited<ReturnType<typeof authProfileMePartialUpdate>>
>;

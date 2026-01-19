// @ts-nocheck
import type {
  AvatarUpload,
  AvatarUploadRequest,
  UserProfile,
} from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * Retrieve the current user's profile. Avatar field is read-only here. Use /auth/profile/avatar/ for avatar uploads.
 * @summary Get user profile
 */
export const profileGet = (
  options?: SecondParameter<typeof customAxiosInstance<UserProfile>>,
) => {
  return customAxiosInstance<UserProfile>(
    { url: `/auth/profile/`, method: "GET" },
    options,
  );
};
/**
 * Update the current user's profile. Avatar field is read-only here. Use /auth/profile/avatar/ for avatar uploads.
 * @summary Update user profile
 */
export const profileUpdate = (
  options?: SecondParameter<typeof customAxiosInstance<UserProfile>>,
) => {
  return customAxiosInstance<UserProfile>(
    { url: `/auth/profile/`, method: "PATCH" },
    options,
  );
};
/**
 * Upload or replace the user's avatar. Expects multipart/form-data.
 * @summary Upload or replace avatar
 */
export const profileAvatarUpload = (
  avatarUploadRequest: AvatarUploadRequest,
  options?: SecondParameter<typeof customAxiosInstance<AvatarUpload>>,
) => {
  const formData = new FormData();
  if (
    avatarUploadRequest.avatar !== undefined &&
    avatarUploadRequest.avatar !== null
  ) {
    formData.append(`avatar`, avatarUploadRequest.avatar);
  }

  return customAxiosInstance<AvatarUpload>(
    {
      url: `/auth/profile/avatar/`,
      method: "PUT",
      headers: { "Content-Type": "multipart/form-data" },
      data: formData,
    },
    options,
  );
};
/**
 * Delete the user's avatar.
 * @summary Delete avatar
 */
export const profileAvatarDelete = (
  options?: SecondParameter<typeof customAxiosInstance<void>>,
) => {
  return customAxiosInstance<void>(
    { url: `/auth/profile/avatar/`, method: "DELETE" },
    options,
  );
};
export type ProfileGetResult = NonNullable<
  Awaited<ReturnType<typeof profileGet>>
>;
export type ProfileUpdateResult = NonNullable<
  Awaited<ReturnType<typeof profileUpdate>>
>;
export type ProfileAvatarUploadResult = NonNullable<
  Awaited<ReturnType<typeof profileAvatarUpload>>
>;
export type ProfileAvatarDeleteResult = NonNullable<
  Awaited<ReturnType<typeof profileAvatarDelete>>
>;

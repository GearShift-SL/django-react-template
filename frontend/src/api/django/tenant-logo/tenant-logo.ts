// @ts-nocheck
import type { TenantLogo, TenantLogoRequest } from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * Upload or replace the tenant's logo. Expects multipart/form-data.
 * @summary Upload or replace tenant logo
 */
export const tenantLogoUpload = (
  tenantLogoRequest: TenantLogoRequest,
  options?: SecondParameter<typeof customAxiosInstance<TenantLogo>>,
) => {
  const formData = new FormData();
  formData.append(`image`, tenantLogoRequest.image);

  return customAxiosInstance<TenantLogo>(
    {
      url: `/tenants/me/logo/`,
      method: "PUT",
      headers: { "Content-Type": "multipart/form-data" },
      data: formData,
    },
    options,
  );
};
/**
 * Delete the tenant's logo.
 * @summary Delete tenant logo
 */
export const tenantLogoDelete = (
  options?: SecondParameter<typeof customAxiosInstance<void>>,
) => {
  return customAxiosInstance<void>(
    { url: `/tenants/me/logo/`, method: "DELETE" },
    options,
  );
};
export type TenantLogoUploadResult = NonNullable<
  Awaited<ReturnType<typeof tenantLogoUpload>>
>;
export type TenantLogoDeleteResult = NonNullable<
  Awaited<ReturnType<typeof tenantLogoDelete>>
>;

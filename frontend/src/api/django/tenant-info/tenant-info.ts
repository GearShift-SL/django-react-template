// @ts-nocheck
import type {
  PatchedTenantRequest,
  Tenant,
  TenantLogo,
  TenantLogoRequest,
} from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * Retrieve the current user's tenant information. Logo field is read-only here. Use /tenant/logo/ for logo uploads.
 * @summary Get tenant information
 */
export const tenantGet = (
  options?: SecondParameter<typeof customAxiosInstance<Tenant>>,
) => {
  return customAxiosInstance<Tenant>(
    { url: `/tenants/info/`, method: "GET" },
    options,
  );
};
/**
 * Update the current user's tenant information. Logo field is read-only here. Use /tenant/logo/ for logo uploads.
 * @summary Update tenant information
 */
export const tenantUpdate = (
  patchedTenantRequest: PatchedTenantRequest,
  options?: SecondParameter<typeof customAxiosInstance<Tenant>>,
) => {
  return customAxiosInstance<Tenant>(
    {
      url: `/tenants/info/`,
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      data: patchedTenantRequest,
    },
    options,
  );
};
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
      url: `/tenants/info/logo/`,
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
    { url: `/tenants/info/logo/`, method: "DELETE" },
    options,
  );
};
export type TenantGetResult = NonNullable<
  Awaited<ReturnType<typeof tenantGet>>
>;
export type TenantUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantUpdate>>
>;
export type TenantLogoUploadResult = NonNullable<
  Awaited<ReturnType<typeof tenantLogoUpload>>
>;
export type TenantLogoDeleteResult = NonNullable<
  Awaited<ReturnType<typeof tenantLogoDelete>>
>;

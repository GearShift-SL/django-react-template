// @ts-nocheck
import type { PatchedTenantRequest, Tenant } from "../djangoAPI.schemas";

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
    { url: `/tenants/me/`, method: "GET" },
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
      url: `/tenants/me/`,
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      data: patchedTenantRequest,
    },
    options,
  );
};
export type TenantGetResult = NonNullable<
  Awaited<ReturnType<typeof tenantGet>>
>;
export type TenantUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantUpdate>>
>;

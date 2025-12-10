// @ts-nocheck
import type { Tenant, TenantRequest } from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

export const tenantsTenantMeRetrieve = (
  options?: SecondParameter<typeof customAxiosInstance<Tenant>>,
) => {
  return customAxiosInstance<Tenant>(
    { url: `/tenants/tenant/me/`, method: "GET" },
    options,
  );
};
export const tenantsTenantMeUpdate = (
  tenantRequest: TenantRequest,
  options?: SecondParameter<typeof customAxiosInstance<Tenant>>,
) => {
  return customAxiosInstance<Tenant>(
    {
      url: `/tenants/tenant/me/`,
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      data: tenantRequest,
    },
    options,
  );
};
export type TenantsTenantMeRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantMeRetrieve>>
>;
export type TenantsTenantMeUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantMeUpdate>>
>;

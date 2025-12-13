// @ts-nocheck
import type { TenantLogo, TenantLogoRequest } from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

export const tenantsTenantLogoRetrieve = (
  options?: SecondParameter<typeof customAxiosInstance<TenantLogo>>,
) => {
  return customAxiosInstance<TenantLogo>(
    { url: `/tenants/tenant-logo/`, method: "GET" },
    options,
  );
};
export const tenantsTenantLogoCreate = (
  tenantLogoRequest: TenantLogoRequest,
  options?: SecondParameter<typeof customAxiosInstance<TenantLogo>>,
) => {
  const formData = new FormData();
  formData.append(`image`, tenantLogoRequest.image);

  return customAxiosInstance<TenantLogo>(
    {
      url: `/tenants/tenant-logo/`,
      method: "POST",
      headers: { "Content-Type": "multipart/form-data" },
      data: formData,
    },
    options,
  );
};
export const tenantsTenantLogoDestroy = (
  options?: SecondParameter<typeof customAxiosInstance<void>>,
) => {
  return customAxiosInstance<void>(
    { url: `/tenants/tenant-logo/`, method: "DELETE" },
    options,
  );
};
export type TenantsTenantLogoRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantLogoRetrieve>>
>;
export type TenantsTenantLogoCreateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantLogoCreate>>
>;
export type TenantsTenantLogoDestroyResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantLogoDestroy>>
>;

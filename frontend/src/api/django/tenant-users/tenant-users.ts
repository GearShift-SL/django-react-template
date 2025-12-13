// @ts-nocheck
import type {
  TenantUserList,
  TenantUserUpdate,
  TenantUserUpdateRequest,
} from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * List, Update and Destroy viewset for the TenantUser model.
 */
export const tenantsTenantUsersList = (
  options?: SecondParameter<typeof customAxiosInstance<TenantUserList[]>>,
) => {
  return customAxiosInstance<TenantUserList[]>(
    { url: `/tenants/tenant-users/`, method: "GET" },
    options,
  );
};
/**
 * List, Update and Destroy viewset for the TenantUser model.
 */
export const tenantsTenantUsersUpdate = (
  id: number,
  tenantUserUpdateRequest: TenantUserUpdateRequest,
  options?: SecondParameter<typeof customAxiosInstance<TenantUserUpdate>>,
) => {
  return customAxiosInstance<TenantUserUpdate>(
    {
      url: `/tenants/tenant-users/${id}/`,
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      data: tenantUserUpdateRequest,
    },
    options,
  );
};
/**
 * List, Update and Destroy viewset for the TenantUser model.
 */
export const tenantsTenantUsersDestroy = (
  id: number,
  options?: SecondParameter<typeof customAxiosInstance<void>>,
) => {
  return customAxiosInstance<void>(
    { url: `/tenants/tenant-users/${id}/`, method: "DELETE" },
    options,
  );
};
export type TenantsTenantUsersListResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersList>>
>;
export type TenantsTenantUsersUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersUpdate>>
>;
export type TenantsTenantUsersDestroyResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersDestroy>>
>;

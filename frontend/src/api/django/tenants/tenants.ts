// @ts-nocheck
import type {
  Invitation,
  InvitationRequest,
  PatchedTenantRequest,
  PatchedTenantUserUpdateRequest,
  Tenant,
  TenantLogo,
  TenantLogoRequest,
  TenantRequest,
  TenantUserDetail,
  TenantUserList,
  TenantUserUpdateRequest,
} from "../djangoAPI.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * A viewset that provides the `create` and `list` actions.
 */
export const tenantsInvitationsList = (
  options?: SecondParameter<typeof customAxiosInstance<Invitation[]>>,
) => {
  return customAxiosInstance<Invitation[]>(
    { url: `/tenants/invitations/`, method: "GET" },
    options,
  );
};
/**
 * A viewset that provides the `create` and `list` actions.
 */
export const tenantsInvitationsCreate = (
  invitationRequest: InvitationRequest,
  options?: SecondParameter<typeof customAxiosInstance<Invitation>>,
) => {
  return customAxiosInstance<Invitation>(
    {
      url: `/tenants/invitations/`,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      data: invitationRequest,
    },
    options,
  );
};
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
/**
 * List, Retrieve and Update viewset for the TenantUser model.
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
 * List, Retrieve and Update viewset for the TenantUser model.
 */
export const tenantsTenantUsersRetrieve = (
  id: number,
  options?: SecondParameter<typeof customAxiosInstance<TenantUserDetail>>,
) => {
  return customAxiosInstance<TenantUserDetail>(
    { url: `/tenants/tenant-users/${id}/`, method: "GET" },
    options,
  );
};
/**
 * List, Retrieve and Update viewset for the TenantUser model.
 */
export const tenantsTenantUsersUpdate = (
  id: number,
  tenantUserUpdateRequest: TenantUserUpdateRequest,
  options?: SecondParameter<typeof customAxiosInstance<TenantUserDetail>>,
) => {
  return customAxiosInstance<TenantUserDetail>(
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
 * List, Retrieve and Update viewset for the TenantUser model.
 */
export const tenantsTenantUsersPartialUpdate = (
  id: number,
  patchedTenantUserUpdateRequest: PatchedTenantUserUpdateRequest,
  options?: SecondParameter<typeof customAxiosInstance<TenantUserDetail>>,
) => {
  return customAxiosInstance<TenantUserDetail>(
    {
      url: `/tenants/tenant-users/${id}/`,
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      data: patchedTenantUserUpdateRequest,
    },
    options,
  );
};
/**
 * List, Retrieve and Update viewset for the TenantUser model.
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
/**
 * List, Retrieve and Update viewset for the TenantUser model.
 */
export const tenantsTenantUsersMeRetrieve = (
  options?: SecondParameter<typeof customAxiosInstance<TenantUserDetail>>,
) => {
  return customAxiosInstance<TenantUserDetail>(
    { url: `/tenants/tenant-users/me/`, method: "GET" },
    options,
  );
};
/**
 * List, Retrieve and Update viewset for the TenantUser model.
 */
export const tenantsTenantUsersMeUpdate = (
  tenantUserUpdateRequest: TenantUserUpdateRequest,
  options?: SecondParameter<typeof customAxiosInstance<TenantUserDetail>>,
) => {
  return customAxiosInstance<TenantUserDetail>(
    {
      url: `/tenants/tenant-users/me/`,
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      data: tenantUserUpdateRequest,
    },
    options,
  );
};
/**
 * List, Retrieve and Update viewset for the TenantUser model.
 */
export const tenantsTenantUsersMePartialUpdate = (
  patchedTenantUserUpdateRequest: PatchedTenantUserUpdateRequest,
  options?: SecondParameter<typeof customAxiosInstance<TenantUserDetail>>,
) => {
  return customAxiosInstance<TenantUserDetail>(
    {
      url: `/tenants/tenant-users/me/`,
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      data: patchedTenantUserUpdateRequest,
    },
    options,
  );
};
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
export const tenantsTenantMePartialUpdate = (
  patchedTenantRequest: PatchedTenantRequest,
  options?: SecondParameter<typeof customAxiosInstance<Tenant>>,
) => {
  return customAxiosInstance<Tenant>(
    {
      url: `/tenants/tenant/me/`,
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      data: patchedTenantRequest,
    },
    options,
  );
};
export type TenantsInvitationsListResult = NonNullable<
  Awaited<ReturnType<typeof tenantsInvitationsList>>
>;
export type TenantsInvitationsCreateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsInvitationsCreate>>
>;
export type TenantsTenantLogoRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantLogoRetrieve>>
>;
export type TenantsTenantLogoCreateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantLogoCreate>>
>;
export type TenantsTenantLogoDestroyResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantLogoDestroy>>
>;
export type TenantsTenantUsersListResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersList>>
>;
export type TenantsTenantUsersRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersRetrieve>>
>;
export type TenantsTenantUsersUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersUpdate>>
>;
export type TenantsTenantUsersPartialUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersPartialUpdate>>
>;
export type TenantsTenantUsersDestroyResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersDestroy>>
>;
export type TenantsTenantUsersMeRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersMeRetrieve>>
>;
export type TenantsTenantUsersMeUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersMeUpdate>>
>;
export type TenantsTenantUsersMePartialUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantUsersMePartialUpdate>>
>;
export type TenantsTenantMeRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantMeRetrieve>>
>;
export type TenantsTenantMeUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantMeUpdate>>
>;
export type TenantsTenantMePartialUpdateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsTenantMePartialUpdate>>
>;

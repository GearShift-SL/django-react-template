// @ts-nocheck
import type { Invitation, InvitationRequest } from "../djangoAPI.schemas";

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
export type TenantsInvitationsListResult = NonNullable<
  Awaited<ReturnType<typeof tenantsInvitationsList>>
>;
export type TenantsInvitationsCreateResult = NonNullable<
  Awaited<ReturnType<typeof tenantsInvitationsCreate>>
>;

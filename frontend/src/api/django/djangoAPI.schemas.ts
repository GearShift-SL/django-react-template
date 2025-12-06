// @ts-nocheck
export interface CodeConfirmError {
  code: string;
  detail: string;
}

export interface CodeConfirmRequestRequest {
  /** @minLength 1 */
  code: string;
}

export type CodeConfirmResponseUser = { [key: string]: unknown };

export interface CodeConfirmResponse {
  user: CodeConfirmResponseUser;
}

export interface Invitation {
  /** @maxLength 254 */
  email: string;
  readonly invited_by: number;
  /** @nullable */
  readonly code: string | null;
  readonly is_accepted: boolean;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface InvitationRequest {
  /**
   * @minLength 1
   * @maxLength 254
   */
  email: string;
}

export interface PatchedTenantRequest {
  /**
   * @minLength 1
   * @maxLength 100
   */
  name?: string;
  logo?: Blob;
  /** @maxLength 200 */
  website?: string;
}

export interface PatchedTenantUserUpdateRequest {
  role?: RoleEnum;
}

export interface PatchedUserRequest {
  /** @maxLength 30 */
  first_name?: string;
  /** @maxLength 30 */
  last_name?: string;
}

/**
 * * `login` - login
 * `connect` - connect
 */
export type ProcessEnum = (typeof ProcessEnum)[keyof typeof ProcessEnum];

// eslint-disable-next-line @typescript-eslint/no-redeclare
export const ProcessEnum = {
  login: "login",
  connect: "connect",
} as const;

export interface Provider {
  provider: string;
  client_id?: string;
}

export interface ProviderTokenError {
  code: string;
  detail: string;
}

export type ProviderTokenRequestRequestToken = { [key: string]: unknown };

export interface ProviderTokenRequestRequest {
  /** @minLength 1 */
  provider: string;
  process: ProcessEnum;
  token: ProviderTokenRequestRequestToken;
}

export type ProviderTokenResponseUser = { [key: string]: unknown };

export interface ProviderTokenResponse {
  user: ProviderTokenResponseUser;
}

export interface ProvidersListResponse {
  providers: Provider[];
}

/**
 * * `owner` - Owner
 * `admin` - Admin
 * `user` - User
 */
export type RoleEnum = (typeof RoleEnum)[keyof typeof RoleEnum];

// eslint-disable-next-line @typescript-eslint/no-redeclare
export const RoleEnum = {
  owner: "owner",
  admin: "admin",
  user: "user",
} as const;

export interface SessionStatusError {
  code: string;
  detail: string;
}

export type SessionStatusResponseUser = { [key: string]: unknown };

export interface SessionStatusResponse {
  user?: SessionStatusResponseUser;
  is_authenticated?: boolean;
}

export interface SimpleTenant {
  readonly pk: number;
  /** @maxLength 100 */
  name: string;
  /**
   * @maxLength 100
   * @pattern ^[-a-zA-Z0-9_]+$
   */
  slug?: string;
}

export interface StartAuthError {
  code: string;
  detail: string;
}

export interface StartAuthRequestRequest {
  /** @minLength 1 */
  email?: string;
  /** @minLength 1 */
  phone?: string;
}

export type StartAuthResponseUser = { [key: string]: unknown };

/**
 * Shape this to reflect your actual auth success payload (user, tokens, etc.).
This is only for documentation; the real response comes from Allauth.
 */
export interface StartAuthResponse {
  user: StartAuthResponseUser;
}

export interface Tenant {
  readonly pk: number;
  /** @maxLength 100 */
  name: string;
  /** @pattern ^[-a-zA-Z0-9_]+$ */
  readonly slug: string;
  logo?: string;
  /** @maxLength 200 */
  website?: string;
  readonly tenant_users: readonly TenantUserList[];
  readonly created_at: string;
  readonly updated_at: string;
}

export interface TenantLogo {
  image: string;
  readonly created_at: string;
}

export interface TenantLogoRequest {
  image: Blob;
}

export interface TenantRequest {
  /**
   * @minLength 1
   * @maxLength 100
   */
  name: string;
  logo?: Blob;
  /** @maxLength 200 */
  website?: string;
}

export interface TenantUserDetail {
  readonly pk: number;
  readonly role: RoleEnum;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface TenantUserList {
  readonly pk: number;
  readonly role: RoleEnum;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface TenantUserSimple {
  readonly pk: number;
  role?: RoleEnum;
}

export interface TenantUserUpdateRequest {
  role?: RoleEnum;
}

export interface User {
  readonly pk: number;
  readonly email: string;
  /** @maxLength 30 */
  first_name?: string;
  /** @maxLength 30 */
  last_name?: string;
  readonly profile: UserProfile;
}

export interface UserMe {
  readonly pk: number;
  readonly email: string;
  /** @maxLength 30 */
  first_name?: string;
  /** @maxLength 30 */
  last_name?: string;
  readonly tenant: SimpleTenant;
  readonly tenant_user: TenantUserSimple;
  readonly profile: UserProfile;
}

export interface UserProfile {
  /** @nullable */
  avatar?: string | null;
}

export interface UserProfileRequest {
  /** @nullable */
  avatar?: Blob | null;
}

export interface UserRequest {
  /** @maxLength 30 */
  first_name?: string;
  /** @maxLength 30 */
  last_name?: string;
}

import { create } from "zustand";

import type { Tenant } from "@/api/django/djangoAPI.schemas";

interface TenantStoreState {
  tenant: Tenant | undefined;
  setTenant: (tenant: Tenant) => void;
  clearTenant: () => void;
}

export const useTenantStore = create<TenantStoreState>((set) => ({
  tenant: undefined,
  setTenant: (tenant) => set({ tenant }),
  clearTenant: () => set({ tenant: undefined })
}));

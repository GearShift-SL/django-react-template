import { create } from "zustand";

import type { UserMe } from "@/api/django/djangoAPI.schemas";

interface UserStore {
  user: (UserMe & { full_name?: string }) | undefined;
  setUser: (user: UserMe & { full_name?: string }) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: undefined,
  setUser: (user) =>
    set({
      user: {
        ...user,
        full_name:
          user.full_name ??
          ([user.first_name, user.last_name].filter(Boolean).join(" ").trim() ||
            undefined)
      }
    }),
  clearUser: () => set({ user: undefined })
}));

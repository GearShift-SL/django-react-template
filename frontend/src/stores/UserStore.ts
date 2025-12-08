import { create } from "zustand";

import type { UserMe } from "@/api/django/djangoAPI.schemas";

interface UserStore {
  user: (UserMe & { full_name?: string }) | undefined;
  setUser: (user: UserMe & { full_name?: string }) => void;
  updateAvatar: (avatar: string | null) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set, get) => ({
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
  updateAvatar: (avatar) => {
    const currentUser = get().user;
    console.debug("Updating avatar with:", avatar);
    console.debug("Current user:", currentUser);
    if (currentUser) {
      console.debug("Updating user store...");
      set({
        user: {
          ...currentUser,
          profile: {
            ...currentUser.profile,
            avatar
          }
        }
      });
    }
  },
  clearUser: () => set({ user: undefined })
}));
